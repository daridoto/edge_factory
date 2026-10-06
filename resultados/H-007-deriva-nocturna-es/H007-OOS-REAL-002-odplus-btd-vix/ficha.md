# H-007 · Dentro del núcleo OD+ · BtD, ¿rinde más el ES las noches con VIX previo > 20?

**OOS de H007-IS-REAL-004 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-OOS-REAL-002-odplus-btd-vix.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2): 0,62 pb/operación (256 sesiones frente a 407); mediana VIX > 20 2,56 pb/operación. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-03 → 2026-05-28 · ES 15min · experimento H007-OOS-REAL-002 · variante **OD+ BtD VIX**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones VIX > 20 | 256 sesiones |
| Sesiones VIX ≤ 20 | 407 sesiones |
| Retorno medio VIX > 20 | 0,73 pb/operación |
| Retorno medio VIX ≤ 20 | 0,11 pb/operación |
| Diferencia VIX > 20 − VIX ≤ 20 | 0,62 pb/operación |
| Mediana VIX > 20 | 2,56 pb/operación |
| t de la media VIX > 20 (sin bloques) | 0,32 t |
| **Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2)** | **0,62 pb/operación** |
| Intervalo bootstrap 95 % | [-4,40; 5,24] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones conservan la dependencia de corto plazo y los regímenes de VIX. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 6 años**.
- Quitando un año cada vez: entre **-1,22 y 2,87 pb/operación**.
- **Cambia de signo al excluir 2021, 2025.**
- PnL de la simulación con costes ×2: -133,00 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/operación | 3,20 | 1,71 | -1,35 | -10,24 | 10,76 | 1,58 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET, lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET.
- **Tamaño:** 1 unidad del índice; 2 unidades si el VIX al cierre de la sesión previa es > 20. Referencia al 100 % del capital (×2 = 200 %) aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa y unidad: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 663 |
| PnL neto | 96,75 USD |
| Resultado medio por operación | 0,15 USD |
| Tasa de acierto | 51,73 % |
| Rentabilidad sobre 10.000 USD | 0,97 % |
| Máximo drawdown (tamaño del plan) | 8,79 % |
| Sharpe | 0,08 |
| Costes | 229,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **19,40 %** |
| Pico → valle | 2022-05-10 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1262 |
| Rentabilidad total | -1,42 % |
| Rentabilidad anual | -0,21 % |
| Sharpe | -0,02 |

## Sensibilidad del tamaño por serie (se informa, no se elige)

Al 100 % del capital por unidad de tamaño (multiplicador > 1 = apalancamiento). La diferencia es el retorno bruto medio por operación sobre el umbral menos el resto y no depende del multiplicador.

| Umbral | Ops sobre umbral | Diferencia (pb) | × | Rentabilidad total | Máx. drawdown | Sharpe |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 544 | 2,31 | 1,5 | -0,93 % | 14,60 % | -0,02 |
| 15 | 544 | 2,31 | 2,0 | -0,64 % | 18,62 % | 0,01 |
| 15 | 544 | 2,31 | 3,0 | -0,37 % | 26,22 % | 0,03 |
| 20 | 256 | 0,62 | 1,5 | -1,33 % | 15,01 % | -0,04 |
| 20 | 256 | 0,62 | 2,0 | -1,42 % | 19,40 % | -0,02 |
| 20 | 256 | 0,62 | 3,0 | -1,87 % | 27,59 % | -0,01 |
| 25 | 108 | -1,12 | 1,5 | -2,09 % | 14,20 % | -0,08 |
| 25 | 108 | -1,12 | 2,0 | -2,92 % | 17,84 % | -0,09 |
| 25 | 108 | -1,12 | 3,0 | -4,72 % | 24,73 % | -0,09 |
| 30 | 37 | 8,95 | 1,5 | 0,09 % | 12,03 % | 0,02 |
| 30 | 37 | 8,95 | 2,0 | 1,48 % | 13,63 % | 0,08 |
| 30 | 37 | 8,95 | 3,0 | 4,19 % | 16,78 % | 0,15 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Los de H007-IS-REAL-003.
- VIX: cierre diario de la sesión previa (16:15 ET), conocido antes de la entrada.
- Al 100 % con ×2 la exposición es del 200 % del capital (apalancamiento).
- Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout.
