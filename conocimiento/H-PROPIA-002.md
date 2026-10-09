---
hipotesis: H-PROPIA-002
nombre: EURUSD · recubrimiento de divisa a fin de mes
experimentos: []
papers: [propia]
---
# H-PROPIA-002 · EURUSD el último día hábil según Europa − EE. UU. en el mes

**Idea** (pegada por el usuario, 2026-10-09): los fondos con acciones extranjeras cubiertas ajustan la cobertura a fin de mes. Si Europa sube más que EE. UU., los fondos estadounidenses venden euros y el EURUSD cae el último día hábil; si sube más EE. UU., el EURUSD sube. Predicción: relación negativa entre la señal (Euro Stoxx 50 − S&P 500, desde el cierre del mes anterior hasta S = T − 2 sesiones) y el retorno de EURUSD de T−1 a T. Criterios fijados de antemano en el encargo (β < 0 con t < −2; t de T más extremo que el 95 % de los placebo T−5…T−15; β < 0 en los subperiodos).

## Muestra y forma
- **Decisión del usuario (2026-10-09):** «Solo IS». El encargo pedía 2005 → hoy; se recorta a la IS clásica 2009-09-27 → 2020-12-31 (fechas de `laboratorio/proteccion.py`) antes de descargar. Subperiodos 2009–2012, 2013–2016 y 2017–2020; el criterio 3 («≥ 3 de 4») pasa a exigir los 3. Sin OOS.
- Contraste independiente fuera del lab: `contrastes/eurusd-cobertura-fin-de-mes/validar.py`, datos de Yahoo (`^STOXX50E`, `^GSPC`, `EURUSD=X`). El Euro Stoxx 50 no está en `data/`. La hora de cierre del EURUSD en Yahoo no está definida (limitación del MVP).

## Resultado IS (2026-10-09)
- **Fuente:** salida de consola de `validar.py` y `salida/meses.csv`; 134 meses (2009-11 → 2020-12). El primer mes se comprobó a mano (señal −4,92, resultado +0,32 %).
- **B:** β = +0,025, t HC3 = 0,92, R² = 0,006. Signo contrario al predicho.
- **A:** «gana Europa» +0,119 % (13,4 pips, n 61) frente a «gana EE. UU.» +0,066 % (7,8 pips, n 73). Welch t 0,59, p 0,56. La diferencia, +5,5 pips, va en sentido opuesto.
- **C:** el t de T queda en el percentil 82 de los 11 placebo (rango −1,42 a +1,80).
- **D:** permutación de una cola (negativa), p 0,82.
- **E/F:** β positiva en los 3 subperiodos (t entre 0,19 y 0,60); en fin de trimestre, β ≈ 0 (t 0,06).
- **Criterios:** no se cumple ninguno de los tres. Veredicto del MVP: DESCARTADA (exploratorio, solo IS). Queda pendiente de la palabra del usuario según [[veredicto]].
- **2026-10-09 · Script borrado por el usuario:** la carpeta `contrastes/eurusd-cobertura-fin-de-mes/` se eliminó («no me interesa tener un folder solo para algo asi»). Las cifras de arriba quedan como cálculo en conversación, no guardado.
