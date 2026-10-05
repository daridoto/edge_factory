"""Ejecutor único: lee la especificación del plan (bloque ```toml) y produce resultados/<ID>/.

    .venv/bin/python -m laboratorio ejecutar experimentos/<ID>.md
"""
from datetime import date
import json
import math
from pathlib import Path
import re
import statistics as st
import tomllib

from . import catalogo, datos, eventos, motor, variantes
from .backtest import backtest
from .contratos import (Componente, Conclusiones, Evidencia, Experimento, Ficheros, Intento, Procedencia, Reglas,
                        Resumen, Robustez, Variantes)
from .presentacion import n
from .proteccion import FIN_IS, INICIO_IS
from .robustez import bateria

NOMBRES = {"media_ventana": "Retorno medio en la ventana", "media_vs_resto": "Diferencia ventana − resto"}
PERIODOS = {"1d": ("Sesiones", "pb/día"), "1h": ("Horas", "pb/hora")}
FRACCION_REF = 0.999  # referencia al 100 % del capital; al 100 % exacto no cabe la comisión de entrada
FICHEROS_100 = Ficheros(equity_100="equity_100.csv", operaciones_100="operaciones_100.csv")


def leer_plan(ruta):
    bloques = re.findall(r"```toml\n(.*?)```", Path(ruta).read_text(), re.S)
    if len(bloques) != 1:
        raise ValueError("El plan debe tener exactamente un bloque ```toml con la especificación")
    return tomllib.loads(bloques[0])


def historial(hipotesis, id_actual, fecha, cambio, resultados=motor.RESULTADOS):
    previos = []
    for f in sorted(Path(resultados).glob("*/resumen.json")):
        r = json.loads(f.read_text())
        if r["experimento"]["hipotesis"] == hipotesis and r["experimento"]["id"] != id_actual:
            previos.append(Intento(id=r["experimento"]["id"], fecha=r["experimento"]["fecha"], cambio=r["historial"][-1]["cambio"]))
    return sorted(previos, key=lambda i: i.fecha) + [Intento(id=id_actual, fecha=fecha, cambio=cambio)]


def tabla_variantes(spec, barras, dataset, inicio, fin, serie=None):
    """(Variantes, filas) si el plan tiene [variantes]; si no, (None, None). `serie` inyecta la serie en tests."""
    if "variantes" not in spec:
        return None, None
    va = spec["variantes"]
    if serie is None and va.get("serie"):
        serie = datos.cargar_serie(va["serie"], inicio, fin)
    filas = variantes.tabla(barras, dataset["frecuencia"], va["ventanas"], va.get("senal"), serie)
    return Variantes(ventanas=va["ventanas"], base=va["base"], senal=va.get("senal"), serie=va.get("serie"),
                     coste_lado=spec["operativa"]["coste_lado"], filas=len(filas)), filas


def ejecutar(spec, plan, barras=None, hoy=None, inicio=INICIO_IS, fin=FIN_IS, **sinteticos):
    """Devuelve (Resumen, sesiones, operaciones, (sesiones, operaciones) al 100 %, filas de variantes o None).
    `barras` (y `serie`) permiten inyectar datos sintéticos en tests.
    Un plan con [senal] usa la operativa por eventos (eventos.py) en lugar de ventana + estadístico."""
    if "senal" in spec:
        return ejecutar_eventos(spec, plan, barras=barras, hoy=hoy, **sinteticos)
    d, v, es, op, bs, cc = (spec[k] for k in ("datos", "ventana", "estadistico", "operativa", "bootstrap", "conclusiones"))
    dataset = datos.DATASETS[d["dataset"]]
    sintetico = barras is not None
    barras = barras if sintetico else datos.cargar(d["dataset"], inicio, fin)
    periodos = datos.periodos(barras, d["periodo"], d.get("excluir_horas", ()))
    obs = catalogo.VENTANAS[v["tipo"]](periodos, v["valores"], inicio, fin, bs["unidad"])
    estadistico = catalogo.ESTADISTICOS[es["tipo"]]
    g = catalogo.grupos(obs)
    n_v, s_v, n_r, s_r = catalogo._sumas(g.values())
    sesiones, operaciones = backtest(obs, len(v["valores"]), op["capital"], op["coste_lado"], op.get("fraccion"))
    m, motivos, por_anio = motor.metricas(op["capital"], sesiones, operaciones)
    al_100 = backtest(obs, len(v["valores"]), op["capital"], op["coste_lado"], FRACCION_REF)
    ref = motor.referencia(op["capital"], *al_100, FRACCION_REF, dataset.get("periodos_por_anio", 252))
    robustez = Robustez(**bateria(g, estadistico, unidad=bs["unidad"], bloque=bs["bloque"], motivo=bs["motivo"],
                                  pnl_costes_x2=m.pnl_neto - m.costes))
    valor = estadistico(list(g.values()))
    nombre_periodo, unidad = PERIODOS[d["periodo"]]
    ventana = v["nombre"]
    desglose = catalogo.desglose(obs) if es.get("desglose") else {}
    b = robustez.bootstrap
    lectura = f"{NOMBRES[es['tipo']]} ({ventana}): {n(valor)} {unidad}. " + (
        "El intervalo incluye cero: en IS no se distingue de no tener efecto." if b.incluye_cero
        else "El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.")
    if desglose and len(v["valores"]) == 1:
        orden = sorted(desglose, key=desglose.get, reverse=True)
        lectura += f" En el desglose, {ventana} ocupa el puesto {orden.index(str(v['valores'][0])) + 1} de {len(orden)}."
    meta, filas = tabla_variantes(spec, barras, dataset, inicio, fin, sinteticos.get("serie"))
    fuentes = [dataset["ruta"]] + ([datos.SERIES[meta.serie]["ruta"]] if meta and meta.serie else [])
    hoy = hoy or date.today()
    return Resumen(
        experimento=Experimento(
            id=spec["id"], hipotesis=spec["hipotesis"], version=spec["version"], fecha=hoy, sintetico=sintetico,
            pregunta=spec["pregunta"], muestra="IS", inicio=sesiones[0].fecha, fin=sesiones[-1].fecha,
            instrumento=dataset["instrumento"], frecuencia=dataset["frecuencia"], moneda="USD", capital_inicial=op["capital"],
            reglas=Reglas(entrada=op["entrada"], salida=op["salida"], tamano=op["tamano"], costes=op["costes"]),
            receta=spec["receta"], plan=str(plan), fuente_datos=" + ".join(fuentes)),
        evidencia=Evidencia(
            estadistico=f"{NOMBRES[es['tipo']]} ({ventana})", unidad=unidad, valor=valor, desglose=desglose,
            componentes=[Componente(nombre=f"{nombre_periodo} {ventana}", valor=n_v, unidad=nombre_periodo.lower()),
                         Componente(nombre=f"{nombre_periodo} resto", valor=n_r, unidad=nombre_periodo.lower()),
                         Componente(nombre=f"Retorno medio {ventana}", valor=s_v / n_v * catalogo.PB, unidad=unidad),
                         Componente(nombre="Retorno medio resto", valor=s_r / n_r * catalogo.PB, unidad=unidad)]),
        robustez=robustez, metricas=m, referencia=ref, variantes=meta, no_calculables=motivos, operaciones_por_anio=por_anio,
        conclusiones=Conclusiones(lectura=lectura, supuestos=cc["supuestos"], limites=cc["limites"],
                                  siguiente_comprobacion=cc["siguiente"]),
        procedencia=Procedencia(motor_sha256=motor.huella_motor(),
                                datos_sha256=motor.digest(json.dumps([(str(x.ts), x.close, x.precio) for x in barras]
                                                                     + [f.model_dump(mode="json") for f in filas or []]).encode()),
                                plan_sha256=motor.digest(Path(motor.RAIZ / plan).read_bytes()) if (motor.RAIZ / plan).exists() else "sin plan",
                                periodos_por_anio=dataset.get("periodos_por_anio", 252)),
        historial=historial(spec["hipotesis"], spec["id"], hoy, spec["cambio"]),
        ficheros=FICHEROS_100.model_copy(update={"variantes": "variantes.csv" if meta else None})), sesiones, operaciones, al_100, filas


def ejecutar_eventos(spec, plan, barras=None, serie=None, referencia=None, hoy=None, inicio=None, fin=None):
    """Operativa por eventos: señal sobre una serie auxiliar, tenencia fija con stop y placebo.
    Sin datos inyectados, lee toda la IS del mercado del dataset (con la autorización de la hipótesis)."""
    d, sn, es, op, pl, bs, cc = (spec[k] for k in ("datos", "senal", "estadistico", "operativa", "placebo", "bootstrap", "conclusiones"))
    dataset = datos.DATASETS[d["dataset"]]
    h = spec["hipotesis"]
    sintetico = barras is not None
    if not sintetico:
        barras = datos.cargar(d["dataset"], inicio, fin, hipotesis=h)
        serie = datos.cargar_serie(d["serie"], inicio, fin, hipotesis=h)
        referencia = datos.cargar_serie(d["referencia"], inicio, fin, hipotesis=h) if d.get("referencia") else None
    # La simulación empieza el primer día con dato de la serie de señal: antes la estrategia no puede existir.
    barras = [b for b in barras if b.ts.date() >= next(iter(serie))]
    dias = eventos.SENALES[sn["tipo"]](serie, sn["corta"], sn["larga"], sn["umbral"])
    usados = eventos.aplicar_enfriamiento(dias, sn["enfriamiento"])
    args = (op["tenencia"], op["stop"])
    sesiones, operaciones, detalle = eventos.simular(barras, usados, *args, op["capital"], op["coste_pct"], op["fraccion"])
    abiertas = [t for t in usados if not eventos.salida(barras, t, *args)]
    m, motivos, por_anio = motor.metricas(op["capital"], sesiones, operaciones, dataset.get("periodos_por_anio", 252))
    al_100 = eventos.simular(barras, usados, *args, op["capital"], op["coste_pct"], FRACCION_REF)[:2]
    ref = motor.referencia(op["capital"], *al_100, FRACCION_REF, dataset.get("periodos_por_anio", 252))
    x2 = eventos.simular(barras, usados, *args, op["capital"], 2 * op["coste_pct"], op["fraccion"])[0][-1].equity - op["capital"]
    retornos = [r for _, _, r in detalle]
    if len(retornos) < 2:
        raise ValueError("Menos de dos operaciones cerradas: no hay estadístico")
    g = {t.isoformat(): [1, r, 0, 0] for t, _, r in detalle}
    estadistico = catalogo.ESTADISTICOS[es["tipo"]]
    robustez = Robustez(**bateria(g, estadistico, unidad=bs["unidad"], bloque=bs["bloque"], motivo=bs["motivo"], pnl_costes_x2=x2))
    valor = estadistico(list(g.values()))
    primera = list(serie)[sn["larga"] - 1]
    medias = eventos.placebo(barras, [b.ts.date() for b in barras if b.ts.date() >= primera], len(retornos), *args,
                             op["coste_pct"], sn["enfriamiento"], pl["sorteos"], pl["semilla"])
    percentil = sum(x < valor / 100 for x in medias) / len(medias) * 100
    p95 = sorted(medias)[int(.95 * len(medias))] * 100
    t_stat = st.mean(retornos) / (st.stdev(retornos) / len(retornos) ** .5)
    componentes = [
        Componente(nombre="Operaciones cerradas", valor=len(retornos), unidad="operaciones"),
        Componente(nombre="Sorteos placebo", valor=len(medias), unidad="sorteos"),
        Componente(nombre="Retorno neto medio por operación", valor=valor, unidad=es["unidad"]),
        Componente(nombre="Media del placebo", valor=st.mean(medias) * 100, unidad=es["unidad"]),
        Componente(nombre="Mediana por operación", valor=st.median(retornos) * 100, unidad="%"),
        Componente(nombre="t de la media", valor=t_stat, unidad="t"),
        Componente(nombre="Percentil 95 del placebo", valor=p95, unidad=es["unidad"]),
        Componente(nombre="Percentil del resultado en el placebo", valor=percentil, unidad="%"),
        Componente(nombre="Señales sin cerrar al final de la muestra", valor=len(abiertas), unidad="operaciones"),
    ]
    if referencia:
        # Referencia del cierre del día de señal (≈ apertura de entrada, mercado 24 h) al cierre del día de salida.
        exceso = [(r - (referencia[f] / referencia[t] - 1)) * 100 for t, s, r in detalle
                  if t in referencia and (f := barras[s.i_salida].ts.date()) in referencia]
        componentes.append(Componente(nombre=f"Exceso medio frente a {d['referencia'].split()[0]}", valor=st.mean(exceso), unidad="%"))
    b = robustez.bootstrap
    lectura = (f"Retorno neto medio por operación ({sn['nombre']}): {n(valor)} {es['unidad']} en {len(retornos)} operaciones; "
               f"mediana {n(st.median(retornos) * 100)} %, t {n(t_stat)}. Placebo: percentil {n(percentil, 0)} "
               f"(p95 {n(p95)} %). " + ("El intervalo incluye cero: en IS no se distingue de no tener efecto." if b.incluye_cero
               else "El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura."))
    hoy = hoy or date.today()
    mercado = dataset.get("mercado", "clasica")
    return Resumen(
        experimento=Experimento(
            id=spec["id"], hipotesis=h, version=spec["version"], fecha=hoy, sintetico=sintetico, pregunta=spec["pregunta"],
            muestra="IS", mercado=mercado, inicio=sesiones[0].fecha, fin=sesiones[-1].fecha,
            instrumento=dataset["instrumento"], frecuencia=dataset["frecuencia"], moneda=op.get("moneda", "USD"),
            capital_inicial=op["capital"],
            reglas=Reglas(entrada=op["entrada"], salida=op["salida"], tamano=op["tamano"], costes=op["costes"]),
            receta=spec["receta"], plan=str(plan),
            fuente_datos=" + ".join([dataset["ruta"]] + [datos.SERIES[d[k]]["ruta"] for k in ("serie", "referencia") if d.get(k)])),
        evidencia=Evidencia(estadistico=f"Retorno neto medio por operación ({sn['nombre']})", unidad=es["unidad"], valor=valor,
                            componentes=componentes),
        robustez=robustez, metricas=m, referencia=ref, no_calculables=motivos, operaciones_por_anio=por_anio,
        conclusiones=Conclusiones(lectura=lectura, supuestos=cc["supuestos"], limites=cc["limites"],
                                  siguiente_comprobacion=cc["siguiente"]),
        procedencia=Procedencia(motor_sha256=motor.huella_motor(),
                                datos_sha256=motor.digest(json.dumps([[str(x.ts), x.open, x.low, x.close] for x in barras]
                                                                     + sorted((str(k), v) for k, v in serie.items())).encode()),
                                plan_sha256=motor.digest(Path(motor.RAIZ / plan).read_bytes()) if (motor.RAIZ / plan).exists() else "sin plan",
                                periodos_por_anio=dataset.get("periodos_por_anio", 252)),
        historial=historial(h, spec["id"], hoy, spec["cambio"]), ficheros=FICHEROS_100), sesiones, operaciones, al_100, None


def anadir_referencia(directorio):
    """Añade `referencia` y su simulación al 100 % a un experimento guardado. Reejecuta su plan y exige mismos datos,
    mismo plan y la misma equity sesión a sesión; no cambia equity.csv ni operaciones.csv."""
    directorio = Path(directorio)
    resumen, sesiones, operaciones = motor.cargar(directorio)
    e = resumen.experimento
    nuevo, repetidas, _, al_100, _ = ejecutar(leer_plan(motor.RAIZ / e.plan), Path(e.plan), hoy=e.fecha)
    p, q = resumen.procedencia, nuevo.procedencia
    if (p.datos_sha256, p.plan_sha256) != (q.datos_sha256, q.plan_sha256):
        raise ValueError(f"{e.id}: datos o plan distintos de los de la ejecución original")
    if len(repetidas) != len(sesiones) or any(a.fecha != b.fecha or not math.isclose(a.equity, b.equity, rel_tol=1e-9)
                                              for a, b in zip(sesiones, repetidas)):
        raise ValueError(f"{e.id}: la reejecución no reproduce la equity guardada")
    actualizado = Resumen.model_validate({**resumen.model_dump(mode="json"), "version_esquema": "2.1",
                                          "referencia": nuevo.referencia.model_dump(mode="json"),
                                          "ficheros": FICHEROS_100.model_dump(mode="json")})
    motor.validar_referencia(actualizado, *al_100)
    motor.escribir(directorio, actualizado, sesiones, operaciones, al_100)
    return actualizado


def main(plan):
    plan = Path(plan).resolve().relative_to(motor.RAIZ)
    spec = leer_plan(motor.RAIZ / plan)
    resumen, sesiones, operaciones, al_100, filas = ejecutar(spec, plan)
    salida = motor.RESULTADOS / spec["id"]
    motor.guardar(salida, resumen, sesiones, operaciones, al_100, filas)
    motor.reconstruir_indice()
    return salida
