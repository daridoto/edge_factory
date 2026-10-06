---
id: H-019
---

# H019-IS-REAL-002 · Plan anterior al cálculo

Réplica de [H019-IS-REAL-001](H019-IS-REAL-001-spy.md) en QQQ, con la misma especificación; solo cambia el dataset. Pedida por el usuario el 2026-10-06. Muestra IS. OOS no autorizado.

## Especificación ejecutable

```toml
id = "H019-IS-REAL-002"
hipotesis = "H-019"
variante = "QQQ · Nov-Abr"
version = "real-is-v1"
pregunta = "¿Rinde más QQQ de noviembre a abril que de mayo a octubre?"
receta = "estrategias/H-019.md"
cambio = "Misma especificación que H019-IS-REAL-001 en QQQ."

[datos]
dataset = "QQQ 1d"
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
siguiente = "Comparar los cuatro ETF con el usuario. OOS bloqueado."
```
