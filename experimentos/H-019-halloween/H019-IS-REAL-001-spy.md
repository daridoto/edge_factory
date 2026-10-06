---
id: H-019
---

# H019-IS-REAL-001 · Plan anterior al cálculo

Receta: [estrategias/H-019.md](../../estrategias/H-019.md). Muestra IS 2009-09-27 → 2020-12-31. OOS no autorizado.

## Qué se mide
- **Estadístico:** retorno diario medio de SPY de noviembre a abril menos el de mayo a octubre, en pb/día. Retornos close-to-close ajustados por dividendos.
- **Operativa:** largo 1 acción del cierre de la última sesión de octubre al cierre de la última sesión de abril; fuera el resto. Coste 0,01 USD por acción y lado. Referencia al 100 % del capital.
- **Robustez:** bootstrap por bloques de 12 meses; estadístico por año natural y sin cada año; costes ×2.
- **Referencia:** W2943226912, S&P 500 1999-2017: 4-8 pb/día, no significativo.

## Piezas nuevas del lab (genéricas, con test)
- Ventana `meses` (valores = meses del año) y operaciones de longitud variable: una operación por tramo continuo de la ventana.

## Especificación ejecutable

```toml
id = "H019-IS-REAL-001"
hipotesis = "H-019"
variante = "SPY · Nov-Abr"
version = "real-is-v1"
pregunta = "¿Rinde más SPY de noviembre a abril que de mayo a octubre?"
receta = "estrategias/H-019.md"
cambio = "Primer ensayo: semestre de invierno frente a verano en SPY."

[datos]
dataset = "SPY 1d"
periodo = "1d"

[ventana]
tipo = "meses"
valores = [11, 12, 1, 2, 3, 4]
nombre = "Nov-Abr"

[estadistico]
tipo = "media_vs_resto"

[operativa]
capital = 10000.0
coste_lado = 0.01
entrada = "Comprar al cierre de la última sesión de octubre."
salida = "Vender al cierre de la última sesión de abril (o de la muestra)."
tamano = "1 acción por semestre; referencia al 100 % del capital aparte."
costes = "0,01 USD por acción y lado; sin comisión adicional ni impacto."

[bootstrap]
unidad = "mes"
bloque = 12
motivo = "La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia."

[conclusiones]
supuestos = [
  "Invierno = sesiones de noviembre a abril; verano = mayo a octubre.",
  "Retornos close-to-close ajustados por dividendos, antes de costes.",
  "El invierno 2020-21 queda cortado el 31-12-2020: cuenta en el estadístico y la operación se cierra ahí.",
]
limites = [
  "Solo 11 inviernos completos en la IS: el intervalo será ancho.",
  "El intervalo no corrige la exploración previa de esta hipótesis en la literatura.",
  "Sin comisiones adicionales, impacto ni dividendos fuera de posición.",
]
siguiente = "Según el resultado: repetir en QQQ, IWM y DIA con la misma especificación, en IS."
```
