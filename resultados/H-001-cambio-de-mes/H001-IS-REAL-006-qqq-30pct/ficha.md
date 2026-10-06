# H-001 · ¿Rinde más QQQ en el cambio de mes que el resto de sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-IS-REAL-006-qqq-30pct.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (TOM): 4,30 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · QQQ 1d · experimento H001-IS-REAL-006 · variante **QQQ · 30 %**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones TOM | 540 sesiones |
| Sesiones resto | 2.293 sesiones |
| Retorno medio TOM | 11,72 pb/día |
| Retorno medio resto | 7,43 pb/día |
| **Diferencia ventana − resto (TOM)** | **4,30 pb/día** |
| Intervalo bootstrap 95 % | [-4,83; 13,86] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos. El intervalo **incluye cero**.

## Robustez

- Positivo en **6 de 12 años**.
- Quitando un año cada vez: entre **0,92 y 6,24 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 1.913,49 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -60,01 | 22,65 | 7,03 | 18,03 | 8,80 | -11,23 | -10,31 | -15,68 | -0,78 | 8,94 | -2,86 | 38,88 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la penúltima sesión de cada mes completo en IS.
- **Salida:** Vender al cierre de la tercera sesión del mes siguiente.
- **Tamaño:** 30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 134 |
| PnL neto | 2.008,57 USD |
| Resultado medio por operación | 14,99 USD |
| Tasa de acierto | 58,21 % |
| Rentabilidad sobre 10.000 USD | 20,09 % |
| Máximo drawdown (tamaño del plan) | 3,39 % |
| Sharpe | 0,66 |
| Costes | 95,09 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **11,02 %** |
| Pico → valle | 2014-07-29 → 2015-09-01 |
| Recuperación | 2018-12-03 |
| Sesiones bajo el agua | 1096 |
| Rentabilidad total | 79,52 % |
| Rentabilidad anual | 5,34 % |
| Sharpe | 0,66 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- TOM = última sesión del mes y tres primeras del siguiente; resto = demás sesiones del mes.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- Calendario observado conocido de antemano, incluidos cierres no programados (C5).
- Septiembre de 2009 excluido por incompleto.
- La simulación usa el 30 % de la equity: rentabilidad y drawdown dependen de ese tamaño, no miden el edge.
- El intervalo no corrige la exploración histórica previa de esta hipótesis.
- Sin comisiones adicionales, impacto ni ejecución intradía.

## Siguiente comprobación (propuesta, sin ejecutar)

En IS, sensibilidad al calendario y a bloques de 1 y 6 meses con la regla fija. OOS sigue bloqueado.
