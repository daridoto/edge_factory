"""Tabla de variantes: una fila por sesión y ventana alternativa, con las covariables que el dashboard usa
para filtrar o dimensionar en vivo (toggles). No decide ni puntúa nada: deja los precios y las condiciones.

Para cada día lun-vie e con precios en una ventana [entrada, salida] (horas de reloj del día e):
- entrada / salida: precio a esa hora = cierre de la barra que termina a esa hora (la que empieza `paso` antes).
- previa: día lun-vie anterior a e (viernes -> lunes).
- senal: retorno entre dos horas de la sesión previa (p. ej. 15:15 -> 16:15); vacío si falta alguna barra.
- serie: valor de una serie diaria (p. ej. VIX) en la sesión previa; vacío si no hay dato.
- desfase: e cae entre los cambios de hora de EE. UU. y de Europa (la apertura europea se mueve una hora en ET).

Todo lo usado para decidir (senal, serie) se conoce al cierre de la sesión previa, antes de la entrada.
"""
from datetime import date, datetime, time, timedelta

from .contratos import Variante

PASOS = {"15min": timedelta(minutes=15), "1h": timedelta(hours=1)}


def _domingo(anio, mes, n):
    """n-ésimo domingo del mes (n = -1: el último)."""
    if n > 0:
        d = date(anio, mes, 1)
        return d + timedelta((6 - d.weekday()) % 7 + 7 * (n - 1))
    d = date(anio, mes + 1, 1) - timedelta(1)
    return d - timedelta((d.weekday() - 6) % 7)


def desfase(d):
    """True si en d EE. UU. y Europa tienen distinto horario de verano (reglas de EE. UU. desde 2007 y de la UE)."""
    a = d.year
    ee = (_domingo(a, 3, 2), _domingo(a, 11, 1))
    ue = (_domingo(a, 3, -1), _domingo(a, 10, -1))
    return ee[0] <= d < ue[0] or ue[1] <= d < ee[1]


def previa(e):
    return e - timedelta(3 if e.weekday() == 0 else 1)


def tabla(barras, frecuencia, ventanas, senal=None, serie=None):
    """Filas Variante ordenadas por (fecha, ventana). `ventanas`: {nombre: ["HH:MM", "HH:MM"]}; `senal`: ["HH:MM", "HH:MM"]."""
    paso = PASOS[frecuencia]
    precio = {b.ts: b.close for b in barras}

    def a_la_hora(dia, hhmm):
        return precio.get(datetime.combine(dia, time.fromisoformat(hhmm)) - paso)

    filas = []
    for e in sorted({b.ts.date() for b in barras}):
        if e.weekday() > 4:
            continue
        d = previa(e)
        s0, s1 = (a_la_hora(d, h) for h in senal) if senal else (None, None)
        valor_senal = s1 / s0 - 1 if s0 and s1 else None
        valor_serie = serie.get(d) if serie else None
        for nombre, (h_in, h_out) in ventanas.items():
            p_in, p_out = a_la_hora(e, h_in), a_la_hora(e, h_out)
            if p_in is None or p_out is None:
                continue
            filas.append(Variante(fecha=e, previa=d, ventana=nombre, entrada=p_in, salida=p_out,
                                  senal=valor_senal, serie=valor_serie, desfase=desfase(e)))
    return filas
