# H-001 · ¿Rinde más QQQ en el cambio de mes que el resto de sesiones?

**OOS de H001-IS-REAL-006 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-OOS-REAL-001-qqq-tom.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (TOM): -4,16 pb/día. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-04 → 2026-04-30 · QQQ 1d · experimento H001-OOS-REAL-001 · variante **QQQ · TOM**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones TOM | 256 sesiones |
| Sesiones resto | 1.081 sesiones |
| Retorno medio TOM | 3,52 pb/día |
| Retorno medio resto | 7,68 pb/día |
| **Diferencia ventana − resto (TOM)** | **-4,16 pb/día** |
| Intervalo bootstrap 95 % | [-20,70; 11,94] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). La hipótesis es mensual; bloques de 3 meses conservan la dependencia entre meses vecinos. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 6 años**.
- Quitando un año cada vez: entre **-6,91 y -0,18 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 253,06 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/día | -16,29 | 7,75 | 0,13 | -21,33 | 1,23 | 19,09 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la penúltima sesión de cada mes completo en IS.
- **Salida:** Vender al cierre de la tercera sesión del mes siguiente.
- **Tamaño:** 30 % de la equity al cierre de entrada, acciones fraccionarias; resto en efectivo sin remunerar; dividendos reinvertidos implícitamente; sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 63 |
| PnL neto | 262,73 USD |
| Resultado medio por operación | 4,17 USD |
| Tasa de acierto | 57,14 % |
| Rentabilidad sobre 10.000 USD | 2,63 % |
| Máximo drawdown (tamaño del plan) | 4,51 % |
| Sharpe | 0,18 |
| Costes | 9,68 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **14,47 %** |
| Pico → valle | 2021-04-05 → 2022-04-29 |
| Recuperación | 2024-07-03 |
| Sesiones bajo el agua | 817 |
| Rentabilidad total | 7,45 % |
| Rentabilidad anual | 1,36 % |
| Sharpe | 0,19 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- TOM = última sesión del mes y tres primeras del siguiente; resto = demás sesiones del mes.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- Calendario observado conocido de antemano, incluidos cierres no programados (C5).
- Solo meses completos dentro de la muestra; mayo de 2026 queda fuera (último dato 2026-05-28).
- QQQ se eligió como candidato tras ver el IS de cuatro ETF: el OOS mide si sobrevive a esa elección.
- Las métricas de cuenta se leen en la referencia al 100 %; el 30 % del plan solo se conserva por identidad con la base.
- Sin comisiones adicionales, impacto ni ejecución intradía.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario qué hacer con H-001 a la vista del OOS.
