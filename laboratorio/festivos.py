"""Festivos de NYSE calculados por regla (no hay calendario en los datos; los huecos de sesión mezclan
festivos con cierres no programados como el huracán Sandy o funerales de Estado).

Reglas de cierre observado de NYSE:
- Año Nuevo (1-ene): en domingo pasa al lunes; en sábado no se cierra (NYSE no cierra el 31-dic).
- Independencia (4-jul) y Navidad (25-dic): en sábado pasan al viernes; en domingo, al lunes.
- Presidentes: 3.er lunes de febrero · Memorial: último lunes de mayo · Trabajo: 1.er lunes de septiembre ·
  Acción de Gracias: 4.º jueves de noviembre · Viernes Santo: dos días antes de Pascua (gregoriana).
Solo los ocho festivos de W2943226912; Martin Luther King y Juneteenth no están.
"""
from datetime import date, timedelta

FESTIVOS = ("ano_nuevo", "presidentes", "viernes_santo", "memorial", "independencia", "trabajo", "accion_gracias", "navidad")


def pascua(anio):
    """Domingo de Pascua gregoriano (algoritmo anónimo de Meeus/Jones/Butcher)."""
    a, b, c = anio % 19, anio // 100, anio % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes, dia = divmod(h + l - 7 * m + 114, 31)
    return date(anio, mes, dia + 1)


def _enesimo(anio, mes, dia_semana, n):
    """n-ésimo día de la semana (0 = lunes) del mes; n = -1, el último."""
    if n > 0:
        d = date(anio, mes, 1)
        return d + timedelta((dia_semana - d.weekday()) % 7 + 7 * (n - 1))
    d = date(anio + mes // 12, mes % 12 + 1, 1) - timedelta(1)
    return d - timedelta((d.weekday() - dia_semana) % 7)


def _observado(d, sabado_al_viernes=True):
    if d.weekday() == 6:
        return d + timedelta(1)
    if d.weekday() == 5:
        return d - timedelta(1) if sabado_al_viernes else None
    return d


def festivos(anio):
    """{festivo: fecha de cierre observado} del año; Año Nuevo en sábado no aparece (no hay cierre)."""
    f = {
        "ano_nuevo": _observado(date(anio, 1, 1), sabado_al_viernes=False),
        "presidentes": _enesimo(anio, 2, 0, 3),
        "viernes_santo": pascua(anio) - timedelta(2),
        "memorial": _enesimo(anio, 5, 0, -1),
        "independencia": _observado(date(anio, 7, 4)),
        "trabajo": _enesimo(anio, 9, 0, 1),
        "accion_gracias": _enesimo(anio, 11, 3, 4),
        "navidad": _observado(date(anio, 12, 25)),
    }
    return {k: v for k, v in f.items() if v is not None}


def vispera(sesiones, nombres=FESTIVOS):
    """{sesión: festivo} con la última sesión anterior a cada festivo observado. Exige que el festivo no sea sesión
    (si lo fuera, la regla o los datos están mal) y que la sesión anterior esté en la lista."""
    dias = sorted(sesiones)
    if not dias:
        return {}
    conjunto, out = set(dias), {}
    for anio in range(dias[0].year, dias[-1].year + 2):
        for nombre, d in festivos(anio).items():
            if nombre not in nombres or not dias[0] < d <= dias[-1]:
                continue
            if d in conjunto:
                raise ValueError(f"{nombre} {d} figura como sesión en los datos")
            previas = [x for x in dias if x < d]
            out[previas[-1]] = nombre
    return out


def vispera_regla(inicio, fin, nombres=FESTIVOS):
    """Como `vispera`, pero sin lista de sesiones (p. ej. futuros, que cotizan en algunos festivos): las sesiones son
    los días laborables que no son ninguno de los 8 festivos. Devuelve las vísperas entre `inicio` y `fin`."""
    todos = {d for a in range(inicio.year - 1, fin.year + 2) for d in festivos(a).values()}
    dias, d = set(), inicio - timedelta(10)
    while d <= fin + timedelta(10):
        if d.weekday() < 5 and d not in todos:
            dias.add(d)
        d += timedelta(1)
    return {k: v for k, v in vispera(dias, nombres).items() if inicio <= k <= fin}
