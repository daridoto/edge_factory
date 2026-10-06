# H-001 · ¿Rinde más QQQ en el cambio de mes que el resto de sesiones?

**Total de H001-IS-REAL-006 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-TOT-REAL-001-qqq-tom.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (TOM): 1,58 pb/día. El intervalo incluye cero: en Total no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2026-04-30 · QQQ 1d · experimento H001-TOT-REAL-001 · variante **QQQ · TOM**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones TOM | 796 sesiones |
| Sesiones resto | 3.374 sesiones |
| Retorno medio TOM | 9,08 pb/día |
| Retorno medio resto | 7,51 pb/día |
| **Diferencia ventana − resto (TOM)** | **1,58 pb/día** |
| Intervalo bootstrap 95 % | [-6,73; 10,13] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos. El intervalo **incluye cero**.

## Robustez

- Positivo en **10 de 18 años**.
- Quitando un año cada vez: entre **-0,81 y 3,05 pb/día**.
- **Cambia de signo al excluir 2020.**
- PnL de la simulación con costes ×2: 2.152,82 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -60,01 | 22,65 | 7,03 | 18,03 | 8,80 | -11,23 | -10,31 | -15,68 | -0,78 | 8,94 | -2,86 | 38,88 | -16,29 | 7,75 | 0,13 | -21,33 | 1,23 | 19,09 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la penúltima sesión de cada mes completo en IS.
- **Salida:** Vender al cierre de la tercera sesión del mes siguiente.
- **Tamaño:** 30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 198 |
| PnL neto | 2.259,69 USD |
| Resultado medio por operación | 11,41 USD |
| Tasa de acierto | 57,58 % |
| Rentabilidad sobre 10.000 USD | 22,60 % |
| Máximo drawdown (tamaño del plan) | 4,51 % |
| Sharpe | 0,48 |
| Costes | 106,88 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **14,47 %** |
| Pico → valle | 2021-04-05 → 2022-04-29 |
| Recuperación | 2024-07-03 |
| Sesiones bajo el agua | 817 |
| Rentabilidad total | 89,55 % |
| Rentabilidad anual | 3,94 % |
| Sharpe | 0,48 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- TOM = última sesión del mes y tres primeras del siguiente; resto = demás sesiones del mes.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- Calendario observado conocido de antemano, incluidos cierres no programados (C5).
- Solo meses completos dentro de la muestra; mayo de 2026 queda fuera (último dato 2026-05-28).
- QQQ se eligió como candidato tras ver el IS de cuatro ETF: el Total mide si sobrevive a esa elección.
- Las métricas de cuenta se leen en la referencia al 100 %; el 30 % del plan solo se conserva por identidad con la base.
- Sin comisiones adicionales, impacto ni ejecución intradía.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario qué hacer con H-001 a la vista del OOS.
