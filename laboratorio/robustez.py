"""Batería de robustez común a todas las hipótesis.

Cada hipótesis aporta sus observaciones agrupadas por unidad (clave que empieza por el año,
p. ej. '2015-03' o '2015-03-02') y su estadístico: una función de una lista de observaciones
a un número. El procedimiento es siempre el mismo; solo cambian unidad, bloque y estadístico.
"""
import random

from .contratos import Bootstrap


def bootstrap(observaciones, estadistico, bloque, replicas=5000, semilla=7301, nivel=.95):
    """Intervalo percentil del estadístico remuestreando bloques circulares de unidades consecutivas."""
    n = len(observaciones)
    if n < bloque or bloque < 1 or replicas < 2:
        raise ValueError("Bootstrap insuficiente")
    rng = random.Random(semilla)
    valores = []
    for _ in range(replicas):
        ids = []
        while len(ids) < n:
            primero = rng.randrange(n)
            ids.extend((primero + j) % n for j in range(bloque))
        valores.append(estadistico([observaciones[i] for i in ids[:n]]))
    valores.sort()

    def percentil(p):
        pos = (len(valores) - 1) * p
        izq = int(pos)
        return valores[izq] + (valores[min(izq + 1, len(valores) - 1)] - valores[izq]) * (pos - izq)
    cola = (1 - nivel) / 2
    return percentil(cola), percentil(1 - cola)


def _calculables(anios, estadistico, seleccion):
    """Estadístico por año; omite los años en los que no se puede calcular (p. ej. comparación con un lado vacío)."""
    out = {}
    for a in anios:
        try:
            out[a] = estadistico(seleccion(a))
        except ValueError:
            continue
    return out


def por_anio(grupos, estadistico):
    anios = sorted({clave[:4] for clave in grupos})
    return _calculables(anios, estadistico, lambda a: [v for k, v in grupos.items() if k.startswith(a)])


def sin_cada_anio(grupos, estadistico):
    anios = sorted({clave[:4] for clave in grupos})
    if len(anios) < 2:
        return {}
    return _calculables(anios, estadistico, lambda a: [v for k, v in grupos.items() if not k.startswith(a)])


def bateria(grupos, estadistico, unidad, bloque, motivo, pnl_costes_x2, replicas=5000, semilla=7301, nivel=.95):
    """Devuelve el bloque `robustez` de resumen.json. `grupos` debe venir en orden cronológico."""
    ic_inf, ic_sup = bootstrap(list(grupos.values()), estadistico, bloque, replicas, semilla, nivel)
    return dict(
        bootstrap=Bootstrap(unidad=unidad, bloque=bloque, replicas=replicas, semilla=semilla, nivel=nivel,
                            ic_inf=ic_inf, ic_sup=ic_sup, incluye_cero=ic_inf <= 0 <= ic_sup, motivo=motivo),
        por_anio=por_anio(grupos, estadistico), sin_cada_anio=sin_cada_anio(grupos, estadistico),
        pnl_costes_x2=pnl_costes_x2)
