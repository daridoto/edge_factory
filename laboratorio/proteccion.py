"""Bloqueo OOS por defecto. Única fuente de las fechas IS; ninguna bandera concede permiso OOS.

Hay una muestra IS por mercado. La clásica (ETF y futuros de EE. UU.) vale para cualquier hipótesis.
Las demás solo valen para las hipótesis cuya autorización literal del usuario consta en
conocimiento/<hipótesis>.md; cualquier otra hipótesis necesita su propia autorización.

OOS: solo para los experimentos IS listados en AUTORIZADAS_OOS (autorización literal en conocimiento/<hipótesis>.md).
Un plan OOS nombra su experimento `base` y debe repetir su especificación sin cambios (ejecutar.exigir_mismo_plan).
"""
from datetime import date

MUESTRAS = {
    "clasica": (date(2009, 9, 27), date(2020, 12, 31)),
    # Todo el histórico de RAY y DefiLlama disponible el 2026-09-30; lo posterior es seguimiento en tiempo real (OOS).
    "cripto": (date(2021, 8, 10), date(2026, 9, 29)),
}
AUTORIZADAS = {"cripto": {"H-PROPIA-001"}}
INICIO_IS, FIN_IS = MUESTRAS["clasica"]
# Todo lo posterior a la IS clásica con datos del ES (último dato 2026-05-28): no queda holdout.
OOS = {"clasica": (date(2021, 1, 1), date(2026, 5, 28))}
AUTORIZADAS_OOS = {"clasica": {"H007-IS-REAL-003", "H007-IS-REAL-004", "H007-IS-REAL-005", "H007-IS-REAL-006", "H007-IS-REAL-008",  # 2026-10-06, conocimiento/H-007.md
                               "H001-IS-REAL-006"}}  # 2026-10-06, conocimiento/H-001.md
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


def limites_muestra(muestra, mercado="clasica"):
    """(inicio, fin) de IS, OOS o Total (IS + OOS seguidas)."""
    return {"IS": MUESTRAS[mercado], "OOS": OOS[mercado], "Total": (MUESTRAS[mercado][0], OOS[mercado][1])}[muestra]


def exigir_muestra(inicio, fin, muestra="IS", mercado="clasica", hipotesis=None, base=None):
    """IS como exigir_is; OOS y Total (IS + OOS) solo si el experimento base está autorizado y las fechas caen dentro."""
    if muestra == "IS":
        return exigir_is(inicio, fin, mercado, hipotesis)
    if muestra not in ("OOS", "Total") or base not in AUTORIZADAS_OOS.get(mercado, ()):
        raise ValueError(f"{BLOQUEO} (OOS no autorizada para {base})")
    inicio_oos, fin_oos = limites_muestra(muestra, mercado)
    inicio, fin = (d if isinstance(d, date) else date.fromisoformat(d) for d in (inicio, fin))
    if inicio > fin or not inicio_oos <= inicio <= fin <= fin_oos:
        raise ValueError(f"Fechas fuera de la muestra autorizada ({inicio_oos} → {fin_oos})")
