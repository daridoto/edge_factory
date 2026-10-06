"""Validación contable, métricas descriptivas y entrada/salida de resultados/<H-NNN-nombre>/<ID>-<variante>/."""
from collections import Counter
import csv
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import statistics as st

from .contratos import Metricas, Operacion, Referencia, Resumen, Sesion, Variante
from .presentacion import render, render_indice
from .proteccion import exigir_muestra

RAIZ = Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "resultados"
COLUMNAS_INDICE = ["id", "ruta", "hipotesis", "variante", "muestra", "fecha", "instrumento", "frecuencia", "inicio", "fin",
                   "estadistico", "unidad", "valor", "ic_inf", "ic_sup", "incluye_cero",
                   "anios_positivos", "anios", "operaciones", "pnl_neto", "sharpe", "max_drawdown", "max_drawdown_100"]


def ruta_resultado(plan):
    """Carpeta espejo del plan: experimentos/<H>/<nombre>.md -> resultados/<H>/<nombre>/."""
    plan = Path(plan)
    if plan.parent.parent.name != "experimentos":
        raise ValueError(f"El plan debe estar en experimentos/<H-NNN-nombre>/: {plan}")
    return RESULTADOS / plan.parent.name / plan.stem


def guardados(resultados=RESULTADOS):
    """Directorios de experimentos guardados, en orden de ruta."""
    return sorted(f.parent for f in Path(resultados).glob("*/*/resumen.json"))


def buscar(id_experimento, resultados=RESULTADOS):
    """Directorio del experimento con ese ID (la carpeta empieza por el ID)."""
    hallados = [d for d in Path(resultados).glob(f"*/{id_experimento}*") if (d / "resumen.json").exists()
                and json.loads((d / "resumen.json").read_text())["experimento"]["id"] == id_experimento]
    if len(hallados) != 1:
        raise ValueError(f"No existe (o está repetido) el experimento {id_experimento}")
    return hallados[0]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def huella_motor():
    ficheros = sorted(Path(__file__).parent.glob("*.py"))
    return digest(b"".join(p.name.encode() + b"\0" + p.read_bytes() for p in ficheros))


def validar_contabilidad(capital, inicio, fin, sesiones, operaciones, mercado="clasica", hipotesis=None, muestra="IS", base=None):
    """La equity debe cubrir la muestra, conciliar sesión a sesión y cuadrar con el libro de operaciones."""
    exigir_muestra(inicio, fin, muestra, mercado, hipotesis, base)
    inicio, fin = (d if isinstance(d, date) else date.fromisoformat(d) for d in (inicio, fin))
    fechas = [s.fecha for s in sesiones]
    if not fechas or fechas != sorted(set(fechas)) or fechas[0] != inicio or fechas[-1] != fin:
        raise ValueError("Equity: fechas únicas, ordenadas y que cubran ambos límites")
    previa = capital
    for s in sesiones:
        if not math.isclose(previa + s.pnl_bruto - s.coste, s.equity, rel_tol=1e-10, abs_tol=1e-8):
            raise ValueError(f"Equity no concilia con PnL bruto menos costes en {s.fecha}")
        previa = s.equity
    if len({o.id for o in operaciones}) != len(operaciones):
        raise ValueError("Operación duplicada")
    dias = set(fechas)
    coste_dia = Counter()
    for o in operaciones:
        if o.entrada not in dias or o.salida not in dias:
            raise ValueError(f"Operación {o.id} fuera de la muestra o sin valoración")
        coste_dia[o.entrada] += o.coste_entrada
        coste_dia[o.salida] += o.coste_salida
    for campo, total in (("pnl_bruto", sum(o.pnl_bruto for o in operaciones)),
                         ("coste", sum(o.coste_entrada + o.coste_salida for o in operaciones))):
        if not math.isclose(sum(getattr(s, campo) for s in sesiones), total, rel_tol=1e-10, abs_tol=1e-8):
            raise ValueError(f"Libro de operaciones y equity no concilian: {campo}")
    if any(not math.isclose(s.coste, coste_dia[s.fecha], abs_tol=1e-8) for s in sesiones):
        raise ValueError("Los costes deben cargarse en la fecha de cada lado")


def metricas(capital, sesiones, operaciones, periodos=252):
    """Devuelve (Metricas, no_calculables, operaciones_por_anio)."""
    neto = [o.pnl_neto for o in operaciones]
    ganan, pierden = [x for x in neto if x > 0], [x for x in neto if x < 0]
    equity = [capital] + [s.equity for s in sesiones]
    r = [b / a - 1 for a, b in zip(equity, equity[1:])]
    motivos = {}

    def si(condicion, valor, clave, motivo):
        if condicion:
            return valor()
        motivos[clave] = motivo
        return None

    media = st.mean(r)
    sd = st.stdev(r) if len(r) > 1 else 0
    abajo = math.sqrt(st.mean([min(x, 0) ** 2 for x in r]))
    pico, i_pico, max_dd, recuperaciones, bajo_agua = equity[0], 0, 0.0, [], False
    for i, valor in enumerate(equity[1:], 1):
        max_dd = max(max_dd, 1 - valor / pico)
        if valor >= pico:
            if bajo_agua:
                recuperaciones.append(i - i_pico)
            pico, i_pico, bajo_agua = valor, i, False
        else:
            bajo_agua = True
    costes = sum(s.coste for s in sesiones)
    bruto_abs = sum(abs(o.pnl_bruto) for o in operaciones)
    por_anio = Counter(o.salida.isoformat()[:4] for o in operaciones)
    rho = None
    if len(r) >= 3 and st.pstdev(r[:-1]) and st.pstdev(r[1:]):
        rho = st.correlation(r[:-1], r[1:])
    else:
        motivos["autocorrelacion"] = "Menos de tres retornos o varianza cero"
    m = Metricas(
        operaciones=len(neto),
        pnl_neto=equity[-1] - capital,
        esperanza=si(neto, lambda: st.mean(neto), "esperanza", "Sin operaciones"),
        tasa_acierto=si(neto, lambda: len(ganan) / len(neto), "tasa_acierto", "Sin operaciones"),
        payoff=si(ganan and pierden, lambda: st.mean(ganan) / abs(st.mean(pierden)), "payoff", "Requiere ganancias y pérdidas"),
        profit_factor=si(pierden, lambda: sum(ganan) / abs(sum(pierden)), "profit_factor", "Sin pérdidas: denominador cero"),
        rentabilidad_total=equity[-1] / equity[0] - 1,
        rentabilidad_anual=si(len(sesiones) >= periodos, lambda: math.expm1(math.log(equity[-1] / equity[0]) * periodos / len(sesiones)),
                              "rentabilidad_anual", "Menos de un año de sesiones; no se extrapola"),
        sharpe=si(sd > 0, lambda: math.sqrt(periodos) * media / sd, "sharpe", "Volatilidad cero o menos de dos observaciones"),
        sortino=si(abajo > 0, lambda: math.sqrt(periodos) * media / abajo, "sortino", "Sin retornos negativos"),
        max_drawdown=max_dd,
        max_recuperacion=si(not bajo_agua, lambda: max(recuperaciones, default=0), "max_recuperacion",
                            "Drawdown abierto al cierre: recuperación censurada"),
        drawdown_abierto=len(sesiones) - i_pico if bajo_agua else 0,
        exposicion=st.mean(s.exposicion for s in sesiones),
        rotacion=sum(s.nocional / e for s, e in zip(sesiones, equity)),
        costes=costes,
        peso_costes=si(bruto_abs, lambda: costes / bruto_abs, "peso_costes", "PnL bruto absoluto cero"),
        concentracion_anual=si(operaciones, lambda: max(por_anio.values()) / len(operaciones), "concentracion_anual", "Sin operaciones"),
        autocorrelacion=rho,
    )
    return m, motivos, dict(sorted(por_anio.items()))


def referencia(capital, sesiones, operaciones, fraccion, periodos=252):
    """Referencia: métricas de riesgo y el episodio del drawdown máximo de una simulación al 100 % del capital."""
    m, _, _ = metricas(capital, sesiones, operaciones, periodos)
    fechas = [s.fecha for s in sesiones]
    equity = [s.equity for s in sesiones]
    pico, i_pico, peor = capital, 0, (0.0, 0, 0)
    for i, valor in enumerate(equity):
        if valor >= pico:
            pico, i_pico = valor, i
        elif 1 - valor / pico > peor[0]:
            peor = (1 - valor / pico, i_pico, i)
    _, i_pico, i_valle = peor
    i_rec = next((i for i in range(i_valle, len(equity)) if equity[i] >= equity[i_pico]), None) if peor[0] else None
    return Referencia(fraccion=fraccion, rentabilidad_total=m.rentabilidad_total, rentabilidad_anual=m.rentabilidad_anual,
                      sharpe=m.sharpe, max_drawdown=m.max_drawdown, pico=fechas[i_pico], valle=fechas[i_valle],
                      recuperacion=None if i_rec is None else fechas[i_rec],
                      sesiones_bajo_agua=((len(equity) - 1 if i_rec is None else i_rec) - i_pico) if peor[0] else 0,
                      motor_sha256=huella_motor())


def _csv(ruta, filas, modelo):
    columnas = list(modelo.model_fields)
    with ruta.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(columnas)
        for fila in filas:
            d = fila.model_dump(mode="json")
            w.writerow([d[c] for c in columnas])


def _leer_csv(ruta, modelo):
    """Una celda vacía es null (solo en campos opcionales; en los demás, el modelo la rechaza)."""
    with ruta.open(newline="") as f:
        return [modelo.model_validate({k: (None if v == "" else v) for k, v in fila.items()}) for fila in csv.DictReader(f)]


def validar_referencia(resumen, sesiones, operaciones):
    """La simulación al 100 % concilia como cualquier otra y su resumen sale de ella."""
    e, r = resumen.experimento, resumen.referencia
    validar_contabilidad(e.capital_inicial, e.inicio, e.fin, sesiones, operaciones, e.mercado, e.hipotesis, e.muestra, e.base)
    calculada = referencia(e.capital_inicial, sesiones, operaciones, r.fraccion, resumen.procedencia.periodos_por_anio)
    if calculada.model_dump(exclude={"motor_sha256"}) != r.model_dump(exclude={"motor_sha256"}):
        raise ValueError("`referencia` no coincide con equity_100.csv y operaciones_100.csv")


def validar_variantes(resumen, operaciones, filas):
    """La tabla cuadra con su descripción y su ventana base reproduce el libro: mismas sesiones de entrada y, en cada
    operación, pnl_bruto = unidades × (salida - entrada), con unidades = coste de entrada / coste por lado."""
    v = resumen.variantes
    if len(filas) != v.filas or {f.ventana for f in filas} - set(v.ventanas):
        raise ValueError("variantes.csv no cuadra con `variantes` (filas o ventanas)")
    claves = [(f.fecha, f.ventana) for f in filas]
    if claves != sorted(set(claves)):
        raise ValueError("variantes.csv: (fecha, ventana) únicas y ordenadas")
    e = resumen.experimento
    if any(not (e.inicio <= f.fecha <= e.fin and f.previa < f.fecha) for f in filas):
        raise ValueError("variantes.csv: fechas fuera de la muestra o sesión previa posterior")
    base = {f.fecha: f for f in filas if f.ventana == v.base}
    if sorted(base) != sorted(o.entrada for o in operaciones):
        raise ValueError("La ventana base no tiene las mismas sesiones que operaciones.csv")
    if v.coste_lado:
        for o in operaciones:
            f = base[o.entrada]
            if not math.isclose(o.pnl_bruto, o.coste_entrada / v.coste_lado * (f.salida - f.entrada), rel_tol=1e-9, abs_tol=1e-9):
                raise ValueError(f"Operación {o.id}: la ventana base no reproduce su PnL bruto")


def guardar(directorio, resumen, sesiones, operaciones, referencia_100=None, variantes=None):
    """Escribe resumen.json, equity.csv, operaciones.csv y ficha.md en un directorio nuevo; con `referencia`,
    también equity_100.csv y operaciones_100.csv (`referencia_100` = (sesiones, operaciones) al 100 %);
    con `variantes` (filas Variante), variantes.csv."""
    e = resumen.experimento
    validar_contabilidad(e.capital_inicial, e.inicio, e.fin, sesiones, operaciones, e.mercado, e.hipotesis, e.muestra, e.base)
    if (resumen.referencia is None) != (referencia_100 is None):
        raise ValueError("`referencia` necesita su simulación al 100 %, y viceversa")
    if referencia_100:
        validar_referencia(resumen, *referencia_100)
    if (resumen.variantes is None) != (variantes is None):
        raise ValueError("`variantes` necesita su tabla, y viceversa")
    if variantes:
        validar_variantes(resumen, operaciones, variantes)
        if referencia_100:
            validar_variantes(resumen, referencia_100[1], variantes)
    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=False)
    escribir(directorio, resumen, sesiones, operaciones, referencia_100, variantes)


def escribir(directorio, resumen, sesiones, operaciones, referencia_100=None, variantes=None):
    (directorio / "resumen.json").write_text(resumen.model_dump_json(indent=2) + "\n")
    _csv(directorio / "equity.csv", sesiones, Sesion)
    _csv(directorio / "operaciones.csv", operaciones, Operacion)
    if referencia_100:
        _csv(directorio / "equity_100.csv", referencia_100[0], Sesion)
        _csv(directorio / "operaciones_100.csv", referencia_100[1], Operacion)
    if variantes:
        _csv(directorio / "variantes.csv", variantes, Variante)
    (directorio / "ficha.md").write_text(render(resumen))


def cargar(directorio):
    """Lee y valida un experimento guardado. Devuelve (Resumen, sesiones, operaciones)."""
    directorio = Path(directorio)
    resumen = Resumen.model_validate_json((directorio / "resumen.json").read_text())
    sesiones = _leer_csv(directorio / "equity.csv", Sesion)
    operaciones = _leer_csv(directorio / "operaciones.csv", Operacion)
    e = resumen.experimento
    validar_contabilidad(e.capital_inicial, e.inicio, e.fin, sesiones, operaciones, e.mercado, e.hipotesis, e.muestra, e.base)
    if resumen.ficheros.equity_100:
        validar_referencia(resumen, _leer_csv(directorio / resumen.ficheros.equity_100, Sesion),
                           _leer_csv(directorio / resumen.ficheros.operaciones_100, Operacion))
    if resumen.ficheros.variantes:
        validar_variantes(resumen, operaciones, _leer_csv(directorio / resumen.ficheros.variantes, Variante))
    return resumen, sesiones, operaciones


def fila_indice(resumen, directorio, resultados=RESULTADOS):
    e, ev, b, m = resumen.experimento, resumen.evidencia, resumen.robustez.bootstrap, resumen.metricas
    anios = resumen.robustez.por_anio
    return dict(id=e.id, ruta=Path(directorio).relative_to(resultados).as_posix(), hipotesis=e.hipotesis,
                variante=e.variante or "", muestra=e.muestra, fecha=e.fecha.isoformat(), instrumento=e.instrumento,
                frecuencia=e.frecuencia, inicio=e.inicio.isoformat(), fin=e.fin.isoformat(),
                estadistico=ev.estadistico, unidad=ev.unidad, valor=ev.valor, ic_inf=b.ic_inf, ic_sup=b.ic_sup,
                incluye_cero=b.incluye_cero, anios_positivos=sum(v > 0 for v in anios.values()), anios=len(anios),
                operaciones=m.operaciones, pnl_neto=m.pnl_neto, sharpe=m.sharpe, max_drawdown=m.max_drawdown,
                max_drawdown_100=resumen.referencia.max_drawdown if resumen.referencia else None)


def reconstruir_indice(resultados=RESULTADOS, indice_md=None):
    """resultados/indice.csv (para el dashboard) e INDICE.md (para leer): una fila por experimento, validándolos todos.
    INDICE.md solo se escribe en la raíz si se reconstruye resultados/ del repo (o si se pasa `indice_md`)."""
    resultados = Path(resultados)
    if indice_md is None and resultados.resolve() == RESULTADOS.resolve():
        indice_md = RAIZ / "INDICE.md"
    guardados_ = [(d, cargar(d)[0]) for d in guardados(resultados)]
    filas = [fila_indice(r, d, resultados) for d, r in guardados_]
    if indice_md:
        Path(indice_md).write_text(render_indice([(d.relative_to(resultados.parent).as_posix(), r) for d, r in guardados_], RAIZ))
    with (resultados / "indice.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS_INDICE)
        w.writeheader()
        w.writerows(filas)
    return filas
