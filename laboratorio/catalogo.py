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


def meses(periodos, valores, inicio, fin, unidad):
    """Mes del año del periodo (1-12): p. ej. [11, 12, 1, 2, 3, 4] es el semestre de invierno."""
    return [Obs(p, p.fin.ts.month, p.fin.ts.month in valores, UNIDADES[unidad](p.fin.ts)) for p in periodos]


def festivos(periodos, valores, inicio, fin, unidad):
    """Víspera de festivo de NYSE (festivos.py): la última sesión antes de cada festivo de `valores`; etiqueta, el
    festivo (o "resto"). Una operación por víspera."""
    from .festivos import vispera
    v = vispera({p.fin.ts.date() for p in periodos}, valores)
    return [Obs(p, v.get(p.fin.ts.date(), "resto"), p.fin.ts.date() in v, UNIDADES[unidad](p.fin.ts)) for p in periodos]


def solo_vispera(obs, nombres):
    """Filtro de cualquier ventana: deja solo los periodos que terminan en una víspera de festivo (calendario por regla)."""
    from .festivos import vispera_regla
    if not obs:
        return obs
    fechas = [o.periodo.fin.ts.date() for o in obs]
    dias = vispera_regla(min(fechas), max(fechas), nombres)
    return [o for o, f in zip(obs, fechas) if f in dias]


VENTANAS = {"dias_de_mes": dias_de_mes, "hora": hora, "meses": meses, "festivos": festivos}
# ventanas cuyas operaciones tienen tantos periodos como valores; en las demás, una operación por tramo continuo
LONGITUD_FIJA = {"dias_de_mes", "hora"}


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
    """Media de la ventana; no necesita resto (p. ej. operativa por sesión sin filtro)."""
    n_v, s_v = sum(g[0] for g in gs), sum(g[1] for g in gs)
    if not n_v:
        raise ValueError("Ventana sin observaciones")
    return s_v / n_v * PB


def media_vs_resto(gs):
    n_v, s_v, n_r, s_r = _sumas(gs)
    return (s_v / n_v - s_r / n_r) * PB


def media_operacion(gs):
    """Retorno neto medio por operación, en %. Grupos [1, retorno, 0, 0], uno por operación (operativa por eventos)."""
    n, s = sum(g[0] for g in gs), sum(g[1] for g in gs)
    if not n:
        raise ValueError("Sin operaciones")
    return s / n * 100


ESTADISTICOS = {"media_ventana": media_ventana, "media_vs_resto": media_vs_resto, "media_operacion": media_operacion}


def _mco(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    beta = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - beta * mx, beta, mx, sxx


def prediccion(xs, ys, meses, arranque=60):
    """Regresión y = α + β·x (MCO) con t de Newey-West (retardo floor(4·(T/100)^(2/9)), pesos de Bartlett), R² y
    R²_OS recursivo: desde el mes `arranque` (contado desde el primero), cada mes se estima con los meses anteriores
    y se predice; R²_OS = 1 - Σ(y - pred)² / Σ(y - media histórica)². `meses`: "AAAA-MM" de cada observación, en orden."""
    alfa, beta, mx, sxx = _mco(xs, ys)
    e = [y - alfa - beta * x for x, y in zip(xs, ys)]
    u = [(x - mx) * r for x, r in zip(xs, e)]
    T = len(xs)
    L = int(4 * (T / 100) ** (2 / 9))
    s = sum(v * v for v in u) + 2 * sum((1 - l / (L + 1)) * sum(u[t] * u[t - l] for t in range(l, T)) for l in range(1, L + 1))
    my = sum(ys) / T
    r2 = 1 - sum(r * r for r in e) / sum((y - my) ** 2 for y in ys)
    orden = sorted(set(meses))
    sse = sse_media = 0.0
    for m in orden[arranque:]:
        antes = [i for i, mm in enumerate(meses) if mm < m]
        a, b, _, _ = _mco([xs[i] for i in antes], [ys[i] for i in antes])
        media = sum(ys[i] for i in antes) / len(antes)
        for i, mm in enumerate(meses):
            if mm == m:
                sse += (ys[i] - a - b * xs[i]) ** 2
                sse_media += (ys[i] - media) ** 2
    r2_os = 1 - sse / sse_media if sse_media else None
    return dict(beta=beta, t_nw=beta / (s / sxx ** 2) ** .5, retardo=L, r2=r2, r2_os=r2_os,
                desde=orden[arranque] if len(orden) > arranque else None)


def desglose(obs):
    """Retorno medio por etiqueta, en pb, ordenado por etiqueta."""
    acc = defaultdict(list)
    for o in obs:
        acc[o.etiqueta].append(retorno(o))
    return {str(k): sum(v) / len(v) * PB for k, v in sorted(acc.items())}
