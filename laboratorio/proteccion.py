"""Bloqueo OOS por defecto. Única fuente de las fechas IS; ninguna bandera concede permiso OOS.

Hay una muestra IS por mercado. La clásica (ETF y futuros de EE. UU.) vale para cualquier hipótesis.
Las demás solo valen para las hipótesis cuya autorización literal del usuario consta en
conocimiento/<hipótesis>.md; cualquier otra hipótesis necesita su propia autorización.
"""
from datetime import date

MUESTRAS = {
    "clasica": (date(2009, 9, 27), date(2020, 12, 31)),
    # Todo el histórico de RAY y DefiLlama disponible el 2026-09-30; lo posterior es seguimiento en tiempo real (OOS).
    "cripto": (date(2021, 8, 10), date(2026, 9, 29)),
}
AUTORIZADAS = {"cripto": {"H-PROPIA-001"}}
INICIO_IS, FIN_IS = MUESTRAS["clasica"]
BLOQUEO = "OOS/holdout BLOQUEADO: se requiere un mensaje explícito del usuario para ese uso; esta versión solo procesa IS"


def exigir_is(inicio, fin, muestra="clasica", hipotesis=None):
    """Rechaza cualquier intervalo que se salga de la IS de su mercado. Admite fechas o texto ISO."""
    if muestra != "clasica" and hipotesis not in AUTORIZADAS.get(muestra, ()):
        raise ValueError(f"{BLOQUEO} (muestra '{muestra}' no autorizada para {hipotesis})")
    inicio_is, fin_is = MUESTRAS[muestra]
    inicio, fin = (d if isinstance(d, date) else date.fromisoformat(d) for d in (inicio, fin))
    if inicio > fin:
        raise ValueError("Fechas de muestra invertidas")
    if not inicio_is <= inicio <= fin <= fin_is:
        raise ValueError(BLOQUEO)
