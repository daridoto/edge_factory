"""Bloqueo OOS por defecto. Única fuente de las fechas IS; ninguna bandera concede permiso OOS."""
from datetime import date

INICIO_IS = date(2009, 9, 27)
FIN_IS = date(2020, 12, 31)
BLOQUEO = "OOS/holdout BLOQUEADO: se requiere un mensaje explícito del usuario para ese uso; esta versión solo procesa IS"


def exigir_is(inicio, fin):
    """Rechaza cualquier intervalo que se salga de IS. Admite fechas o texto ISO."""
    inicio, fin = (d if isinstance(d, date) else date.fromisoformat(d) for d in (inicio, fin))
    if inicio > fin:
        raise ValueError("Fechas de muestra invertidas")
    if not INICIO_IS <= inicio <= fin <= FIN_IS:
        raise ValueError(BLOQUEO)
