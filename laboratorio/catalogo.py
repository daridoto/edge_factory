"""Catálogo de ventanas y estadísticos. Una hipótesis nueva elige piezas de aquí en su plan;
solo se programa algo cuando aparece un tipo que aún no existe, y queda para las siguientes.

Una observación es un periodo con: etiqueta (hora, día del mes…), si cae en la ventana y su unidad de
remuestreo (mes, día). Las ventanas devuelven observaciones; los estadísticos resumen grupos por unidad.
"""
from collections import defaultdict, namedtuple
import calendar

Obs = namedtuple("Obs", "periodo etiqueta en_ventana unidad")
PB = 10000
UNIDADES = {"mes": lambda ts: ts.strftime("%Y-%m"), "día": lambda ts: ts.strftime("%Y-%m-%d")}


# ---------- ventanas ----------

def dias_de_mes(periodos, valores, inicio, fin, unidad):
    """Sesiones por posición en el mes: +1, +2… desde el principio; -1, -2… desde el final.
    Solo meses completos dentro de la muestra."""
    meses = defaultdict(list)
    for p in periodos:
        meses[p.fin.ts.strftime("%Y-%m")].append(p)
    fuera = set()
    if inicio.day != 1:
        fuera.add(inicio.strftime("%Y-%m"))
    if fin.day != calendar.monthrange(fin.year, fin.month)[1]:
        fuera.add(fin.strftime("%Y-%m"))
    obs = []
    for mes, ps in meses.items():
        if mes in fuera:
            continue
        for k, p in enumerate(ps, 1):
            etiqueta = k if k <= len(ps) // 2 else k - len(ps) - 1
            obs.append(Obs(p, etiqueta, etiqueta in valores, UNIDADES[unidad](p.fin.ts)))
    return obs


def hora(periodos, valores, inicio, fin, unidad):
    """Hora de reloj del periodo (h = h:00 a h+1:00)."""
    return [Obs(p, p.fin.ts.hour, p.fin.ts.hour in valores, UNIDADES[unidad](p.fin.ts)) for p in periodos]


VENTANAS = {"dias_de_mes": dias_de_mes, "hora": hora}


# ---------- estadísticos (sobre grupos [n ventana, suma ventana, n resto, suma resto], en pb) ----------

def retorno(o):
    return o.periodo.fin.close / o.periodo.inicio.close - 1


def grupos(obs):
    g = {}
    for o in obs:
        acc = g.setdefault(o.unidad, [0, 0.0, 0, 0.0])
        i = 0 if o.en_ventana else 2
        acc[i] += 1
        acc[i + 1] += retorno(o)
    return g


def _sumas(gs):
    n_v, s_v, n_r, s_r = (sum(g[i] for g in gs) for i in range(4))
    if not n_v or not n_r:
        raise ValueError("Comparación sin observaciones")
    return n_v, s_v, n_r, s_r


def media_ventana(gs):
    n_v, s_v, _, _ = _sumas(gs)
    return s_v / n_v * PB


def media_vs_resto(gs):
    n_v, s_v, n_r, s_r = _sumas(gs)
    return (s_v / n_v - s_r / n_r) * PB


ESTADISTICOS = {"media_ventana": media_ventana, "media_vs_resto": media_vs_resto}


def desglose(obs):
    """Retorno medio por etiqueta, en pb, ordenado por etiqueta."""
    acc = defaultdict(list)
    for o in obs:
        acc[o.etiqueta].append(retorno(o))
    return {str(k): sum(v) / len(v) * PB for k, v in sorted(acc.items())}
