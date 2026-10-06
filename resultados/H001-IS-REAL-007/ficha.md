# H-001 · ¿Rinde más IWM en el cambio de mes que el resto de sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-001.md) → [plan](../../experimentos/H001-IS-REAL-007.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (TOM): -3,55 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · IWM 1d · experimento H001-IS-REAL-007. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones TOM | 540 sesiones |
| Sesiones resto | 2.293 sesiones |
| Retorno medio TOM | 2,83 pb/día |
| Retorno medio resto | 6,38 pb/día |
| **Diferencia ventana − resto (TOM)** | **-3,55 pb/día** |
| Intervalo bootstrap 95 % | [-15,78; 8,59] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos. El intervalo **incluye cero**.

## Robustez

- Positivo en **3 de 12 años**.
- Quitando un año cada vez: entre **-6,02 y -2,49 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 325,41 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -45,71 | 21,78 | -4,59 | 14,65 | -7,34 | -12,06 | -7,03 | -13,53 | -14,47 | 3,80 | -4,19 | -5,38 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la penúltima sesión de cada mes completo en IS.
- **Salida:** Vender al cierre de la tercera sesión del mes siguiente.
- **Tamaño:** 30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 134 |
| PnL neto | 404,42 USD |
| Resultado medio por operación | 3,02 USD |
| Tasa de acierto | 55,97 % |
| Rentabilidad sobre 10.000 USD | 4,04 % |
| Máximo drawdown (tamaño del plan) | 7,71 % |
| Sharpe | 0,14 |
| Costes | 79,01 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **24,83 %** |
| Pico → valle | 2013-03-28 → 2020-05-01 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1955 |
| Rentabilidad total | 10,29 % |
| Rentabilidad anual | 0,87 % |
| Sharpe | 0,14 |

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
