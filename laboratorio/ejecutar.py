"""Ejecutor único: lee la especificación del plan (bloque ```toml) y produce resultados/<ID>/.

    .venv/bin/python -m laboratorio ejecutar experimentos/<ID>.md
"""
from datetime import date
import json
from pathlib import Path
import re
import tomllib

from . import catalogo, datos, motor
from .backtest import backtest
from .contratos import (Componente, Conclusiones, Evidencia, Experimento, Intento, Procedencia, Reglas,
                        Resumen, Robustez)
from .presentacion import n
from .proteccion import FIN_IS, INICIO_IS
from .robustez import bateria

NOMBRES = {"media_ventana": "Retorno medio en la ventana", "media_vs_resto": "Diferencia ventana − resto"}
PERIODOS = {"1d": ("Sesiones", "pb/día"), "1h": ("Horas", "pb/hora")}


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


def ejecutar(spec, plan, barras=None, hoy=None, inicio=INICIO_IS, fin=FIN_IS):
    """Devuelve (Resumen, sesiones, operaciones). `barras` permite inyectar datos sintéticos en tests."""
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
    hoy = hoy or date.today()
    return Resumen(
        experimento=Experimento(
            id=spec["id"], hipotesis=spec["hipotesis"], version=spec["version"], fecha=hoy, sintetico=sintetico,
            pregunta=spec["pregunta"], muestra="IS", inicio=sesiones[0].fecha, fin=sesiones[-1].fecha,
            instrumento=dataset["instrumento"], frecuencia=dataset["frecuencia"], moneda="USD", capital_inicial=op["capital"],
            reglas=Reglas(entrada=op["entrada"], salida=op["salida"], tamano=op["tamano"], costes=op["costes"]),
            receta=spec["receta"], plan=str(plan), fuente_datos=dataset["ruta"]),
        evidencia=Evidencia(
            estadistico=f"{NOMBRES[es['tipo']]} ({ventana})", unidad=unidad, valor=valor, desglose=desglose,
            componentes=[Componente(nombre=f"{nombre_periodo} {ventana}", valor=n_v, unidad=nombre_periodo.lower()),
                         Componente(nombre=f"{nombre_periodo} resto", valor=n_r, unidad=nombre_periodo.lower()),
                         Componente(nombre=f"Retorno medio {ventana}", valor=s_v / n_v * catalogo.PB, unidad=unidad),
                         Componente(nombre="Retorno medio resto", valor=s_r / n_r * catalogo.PB, unidad=unidad)]),
        robustez=robustez, metricas=m, no_calculables=motivos, operaciones_por_anio=por_anio,
        conclusiones=Conclusiones(lectura=lectura, supuestos=cc["supuestos"], limites=cc["limites"],
                                  siguiente_comprobacion=cc["siguiente"]),
        procedencia=Procedencia(motor_sha256=motor.huella_motor(),
                                datos_sha256=motor.digest(json.dumps([(str(x.ts), x.close, x.precio) for x in barras]).encode()),
                                plan_sha256=motor.digest(Path(motor.RAIZ / plan).read_bytes()) if (motor.RAIZ / plan).exists() else "sin plan",
                                periodos_por_anio=252),
        historial=historial(spec["hipotesis"], spec["id"], hoy, spec["cambio"])), sesiones, operaciones


def main(plan):
    plan = Path(plan).resolve().relative_to(motor.RAIZ)
    spec = leer_plan(motor.RAIZ / plan)
    resumen, sesiones, operaciones = ejecutar(spec, plan)
    salida = motor.RESULTADOS / spec["id"]
    motor.guardar(salida, resumen, sesiones, operaciones)
    motor.reconstruir_indice()
    return salida
