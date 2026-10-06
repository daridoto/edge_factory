---
id: H-001
---

# H001-IS-REAL-002 · Plan anterior al cálculo

Receta: [estrategias/H-001.md](../../estrategias/H-001.md). Plan fijado el 2026-09-24, antes de calcular. Réplica exacta de [H001-IS-REAL-001](H001-IS-REAL-001-spy-1-accion.md) en QQQ (Nasdaq 100): solo cambia el instrumento. La hipótesis habla de renta variable en general y la receta ya proponía otros índices.

**Autorización de la muestra:** el usuario pidió replicar H-001 en QQQ, IWM y DIA con «recuerda que es importante la clasificacion de muestras para usar unicamente IS y qeu no haya contaminacion». Muestra: IS 2009-09-27 a 2020-12-31. OOS no está autorizado.

## Qué se mide
- **Estadístico:** retorno diario medio de QQQ en TOM (última sesión del mes y tres primeras del siguiente) menos el del resto de sesiones del mes, en pb/día. Retornos close-to-close ajustados por dividendos.
- **Operativa:** largo 1 acción del cierre de la sesión −2 al cierre de la +3, solo si ambos meses están completos en IS. Coste 0,01 USD por acción y lado (C3); capital 10.000 USD, efectivo sin remunerar (C4).
- **Robustez:** bootstrap por bloques circulares de 3 meses; estadístico por año y sin cada año; costes ×2.
- Septiembre de 2009 se excluye por incompleto. Calendario observado conocido de antemano (C5). Datos inválidos o duplicados en IS: detener, no interpolar.

## Qué no se hace en este ensayo
- La comparación alternativa (−10…−2 y +4…+10), las exclusiones de cambio de año y fin de trimestre, el recorte del 1 % y las ventanas alternativas.

## Especificación ejecutable

```toml
id = "H001-IS-REAL-002"
hipotesis = "H-001"
version = "real-is-v1"
pregunta = "¿Rinde más QQQ en el cambio de mes que el resto de sesiones?"
receta = "estrategias/H-001.md"
cambio = "Misma especificación que H001-IS-REAL-001 con QQQ en lugar de SPY."

[datos]
dataset = "QQQ 1d"
periodo = "1d"

[ventana]
tipo = "dias_de_mes"
valores = [-1, 1, 2, 3]
nombre = "TOM"

[estadistico]
tipo = "media_vs_resto"

[operativa]
capital = 10000.0
coste_lado = 0.01
entrada = "Comprar al cierre de la penúltima sesión de cada mes completo en IS."
salida = "Vender al cierre de la tercera sesión del mes siguiente."
tamano = "1 acción por ventana (no el capital entero); dividendos reinvertidos implícitamente; sin apalancamiento."
costes = "0,01 USD por acción y lado; sin comisión adicional ni impacto."

[bootstrap]
unidad = "mes"
bloque = 3
motivo = "La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos."

[conclusiones]
supuestos = [
  "TOM = última sesión del mes y tres primeras del siguiente; resto = demás sesiones del mes.",
  "Retornos close-to-close ajustados por dividendos, antes de costes.",
  "Calendario observado conocido de antemano, incluidos cierres no programados (C5).",
  "Septiembre de 2009 excluido por incompleto.",
]
limites = [
  "La simulación usa 1 acción: rentabilidad y drawdown de cuenta dependen de ese tamaño, no miden el edge.",
  "El intervalo no corrige la exploración histórica previa de esta hipótesis.",
  "Sin comisiones adicionales, impacto ni ejecución intradía.",
]
siguiente = "En IS, sensibilidad al calendario y a bloques de 1 y 6 meses con la regla fija. OOS sigue bloqueado."
```
