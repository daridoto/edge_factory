"""Validación contable, métricas descriptivas y entrada/salida de resultados/<ID>/."""
from collections import Counter
import csv
from datetime import date
import hashlib
import math
from pathlib import Path
import statistics as st

from .contratos import Metricas, Operacion, Resumen, Sesion
from .presentacion import render
from .proteccion import exigir_is

RAIZ = Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "resultados"
COLUMNAS_INDICE = ["id", "hipotesis", "fecha", "instrumento", "frecuencia", "inicio", "fin",
                   "estadistico", "unidad", "valor", "ic_inf", "ic_sup", "incluye_cero",
                   "anios_positivos", "anios", "operaciones", "pnl_neto", "sharpe", "max_drawdown"]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def huella_motor():
    ficheros = sorted(Path(__file__).parent.glob("*.py"))
    return digest(b"".join(p.name.encode() + b"\0" + p.read_bytes() for p in ficheros))


def validar_contabilidad(capital, inicio, fin, sesiones, operaciones, mercado="clasica", hipotesis=None):
    """La equity debe cubrir la muestra, conciliar sesión a sesión y cuadrar con el libro de operaciones."""
    exigir_is(inicio, fin, mercado, hipotesis)
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


def _csv(ruta, filas, modelo):
    columnas = list(modelo.model_fields)
    with ruta.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(columnas)
        for fila in filas:
            d = fila.model_dump(mode="json")
            w.writerow([d[c] for c in columnas])


def _leer_csv(ruta, modelo):
    with ruta.open(newline="") as f:
        return [modelo.model_validate(fila) for fila in csv.DictReader(f)]


def guardar(directorio, resumen, sesiones, operaciones):
    """Escribe resumen.json, equity.csv, operaciones.csv y ficha.md en un directorio nuevo."""
    e = resumen.experimento
    validar_contabilidad(e.capital_inicial, e.inicio, e.fin, sesiones, operaciones, e.mercado, e.hipotesis)
    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=False)
    (directorio / "resumen.json").write_text(resumen.model_dump_json(indent=2) + "\n")
    _csv(directorio / "equity.csv", sesiones, Sesion)
    _csv(directorio / "operaciones.csv", operaciones, Operacion)
    (directorio / "ficha.md").write_text(render(resumen))


def cargar(directorio):
    """Lee y valida un experimento guardado. Devuelve (Resumen, sesiones, operaciones)."""
    directorio = Path(directorio)
    resumen = Resumen.model_validate_json((directorio / "resumen.json").read_text())
    sesiones = _leer_csv(directorio / "equity.csv", Sesion)
    operaciones = _leer_csv(directorio / "operaciones.csv", Operacion)
    e = resumen.experimento
    validar_contabilidad(e.capital_inicial, e.inicio, e.fin, sesiones, operaciones, e.mercado, e.hipotesis)
    return resumen, sesiones, operaciones


def fila_indice(resumen):
    e, ev, b, m = resumen.experimento, resumen.evidencia, resumen.robustez.bootstrap, resumen.metricas
    anios = resumen.robustez.por_anio
    return dict(id=e.id, hipotesis=e.hipotesis, fecha=e.fecha.isoformat(), instrumento=e.instrumento,
                frecuencia=e.frecuencia, inicio=e.inicio.isoformat(), fin=e.fin.isoformat(),
                estadistico=ev.estadistico, unidad=ev.unidad, valor=ev.valor, ic_inf=b.ic_inf, ic_sup=b.ic_sup,
                incluye_cero=b.incluye_cero, anios_positivos=sum(v > 0 for v in anios.values()), anios=len(anios),
                operaciones=m.operaciones, pnl_neto=m.pnl_neto, sharpe=m.sharpe, max_drawdown=m.max_drawdown)


def reconstruir_indice(resultados=RESULTADOS):
    """resultados/indice.csv: una fila por experimento, con las cifras clave para comparar."""
    resultados = Path(resultados)
    filas = [fila_indice(cargar(d)[0]) for d in sorted(resultados.iterdir()) if (d / "resumen.json").exists()]
    with (resultados / "indice.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS_INDICE)
        w.writeheader()
        w.writerows(filas)
    return filas
