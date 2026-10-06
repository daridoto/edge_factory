---
id: H-001
---

# H001-OOS-REAL-001 · Plan anterior al cálculo

Base: [H001-IS-REAL-006](H001-IS-REAL-006-qqq-30pct.md) (TOM en QQQ). Receta: [estrategias/H-001.md](../../estrategias/H-001.md).

## Muestra y autorización
- **OOS 2021-01-01 → 2026-05-28** (mismo OOS que H-007; último dato del ES). Los datos de QQQ siguen hasta 2026-07-15: ese mes y medio queda sin usar, no es holdout útil.
- **Autorización literal del usuario (2026-10-06):** «probemos esto en OOS y vemos que tal» (TOM en QQQ), con OOS «2021-01-01 → 2026-05-28» elegido en la pregunta del periodo, y «si es sobre acciones usa el 100% de la cuenta, no por realismo si no por simplicidad, las metricas que observo serian sobre la cuenta en si». Vale solo para TOM en QQQ (base H001-IS-REAL-006); SPY, IWM y DIA no están autorizados.
- **Tamaño:** el plan repite el de la base (30 % de la equity), porque el ejecutor exige especificación idéntica. Las métricas que mira el usuario son las de la referencia al 100 % de la cuenta (`referencia` en `resumen.json`, 99,9 % para que quepa la comisión), que es lo que pinta el dashboard.
- El ejecutor exige que la especificación sea idéntica a la de 006 (salvo identidad y conclusiones) y solo admite fechas dentro de la muestra OOS de `proteccion.py`.

## Criterios
Sin criterios previos fijados por el usuario: se mira el resultado y se decide en la conversación. Refutación de la hipótesis (H-001): que la media TOM no supere a la del resto fuera de la muestra del paper.

## Referencia IS (006)
+4,30 pb/día (TOM − resto), IC 95 % [−4,83; 13,86], 6/12 años positivos; único ETF positivo al quitar cualquier año.

## Especificación ejecutable

```toml
id = "H001-OOS-REAL-001"
muestra = "OOS"
base = "H001-IS-REAL-006"
hipotesis = "H-001"
variante = "QQQ · TOM"
version = "real-oos-v1"
pregunta = "¿Rinde más QQQ en el cambio de mes que el resto de sesiones?"
receta = "estrategias/H-001.md"
cambio = "OOS 2021-01-01 → 2026-05-28 de H001-IS-REAL-006, sin cambiar nada de su especificación."

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
fraccion = 0.30
entrada = "Comprar al cierre de la penúltima sesión de cada mes completo en IS."
salida = "Vender al cierre de la tercera sesión del mes siguiente."
tamano = "30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento."
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
  "Solo meses completos dentro de la muestra; mayo de 2026 queda fuera (último dato 2026-05-28).",
]
limites = [
  "QQQ se eligió como candidato tras ver el IS de cuatro ETF: el OOS mide si sobrevive a esa elección.",
  "Las métricas de cuenta se leen en la referencia al 100 %; el 30 % del plan solo se conserva por identidad con la base.",
  "Sin comisiones adicionales, impacto ni ejecución intradía.",
]
siguiente = "Decidir con el usuario qué hacer con H-001 a la vista del OOS."
```
