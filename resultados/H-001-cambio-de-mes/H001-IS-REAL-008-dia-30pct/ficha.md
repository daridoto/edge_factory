# H-001 · ¿Rinde más DIA en el cambio de mes que el resto de sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-IS-REAL-008-dia-30pct.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (TOM): 0,05 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · DIA 1d · experimento H001-IS-REAL-008 · variante **DIA · 30 %**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones TOM | 540 sesiones |
| Sesiones resto | 2.293 sesiones |
| Retorno medio TOM | 5,62 pb/día |
| Retorno medio resto | 5,56 pb/día |
| **Diferencia ventana − resto (TOM)** | **0,05 pb/día** |
| Intervalo bootstrap 95 % | [-8,55; 9,13] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 12 años**.
- Quitando un año cada vez: entre **-2,94 y 1,26 pb/día**.
- **Cambia de signo al excluir 2010, 2012, 2017, 2020.**
- PnL de la simulación con costes ×2: 836,03 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -46,92 | 23,92 | -6,98 | 11,41 | -9,07 | -9,17 | -6,89 | -8,31 | 2,93 | -3,87 | -12,27 | 30,73 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la penúltima sesión de cada mes completo en IS.
- **Salida:** Vender al cierre de la tercera sesión del mes siguiente.
- **Tamaño:** 30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 134 |
| PnL neto | 886,40 USD |
| Resultado medio por operación | 6,61 USD |
| Tasa de acierto | 60,45 % |
| Rentabilidad sobre 10.000 USD | 8,86 % |
| Máximo drawdown (tamaño del plan) | 3,98 % |
| Sharpe | 0,37 |
| Costes | 50,37 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **12,82 %** |
| Pico → valle | 2011-05-31 → 2011-11-01 |
| Recuperación | 2013-01-02 |
| Sesiones bajo el agua | 400 |
| Rentabilidad total | 30,30 % |
| Rentabilidad anual | 2,38 % |
| Sharpe | 0,37 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

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
