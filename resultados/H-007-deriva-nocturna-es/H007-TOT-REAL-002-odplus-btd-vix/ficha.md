# H-007 · Dentro del núcleo OD+ · BtD, ¿rinde más el ES las noches con VIX previo > 20?

**Total de H007-IS-REAL-004 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-TOT-REAL-002-odplus-btd-vix.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2): 4,54 pb/operación (641 sesiones frente a 1268); mediana VIX > 20 5,31 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2026-05-28 · ES 15min · experimento H007-TOT-REAL-002 · variante **OD+ BtD VIX**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones VIX > 20 | 641 sesiones |
| Sesiones VIX ≤ 20 | 1.268 sesiones |
| Retorno medio VIX > 20 | 5,72 pb/operación |
| Retorno medio VIX ≤ 20 | 1,19 pb/operación |
| Diferencia VIX > 20 − VIX ≤ 20 | 4,54 pb/operación |
| Mediana VIX > 20 | 5,31 pb/operación |
| t de la media VIX > 20 (sin bloques) | 3,61 t |
| Años sin comparación posible (un lado vacío) | 1 años |
| **Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2)** | **4,54 pb/operación** |
| Intervalo bootstrap 95 % | [1,58; 7,63] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones conservan la dependencia de corto plazo y los regímenes de VIX. El intervalo **no incluye cero**.

## Robustez

- Positivo en **14 de 17 años**.
- Quitando un año cada vez: entre **3,69 y 6,21 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 714,50 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 13,47 | -1,44 | 6,37 | 11,92 | 32,90 | 10,38 | 12,39 | 1,42 | 13,47 | 13,09 | 6,97 | 3,20 | 1,71 | -1,35 | -10,24 | 10,76 | 1,58 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET, lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET.
- **Tamaño:** 1 unidad del índice; 2 unidades si el VIX al cierre de la sesión previa es > 20. Referencia al 100 % del capital (×2 = 200 %) aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa y unidad: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1909 |
| PnL neto | 1.352,00 USD |
| Resultado medio por operación | 0,71 USD |
| Tasa de acierto | 51,91 % |
| Rentabilidad sobre 10.000 USD | 13,52 % |
| Máximo drawdown (tamaño del plan) | 7,84 % |
| Sharpe | 0,46 |
| Costes | 637,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **19,40 %** |
| Pico → valle | 2022-05-10 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1262 |
| Rentabilidad total | 79,18 % |
| Rentabilidad anual | 2,88 % |
| Sharpe | 0,63 |

## Sensibilidad del tamaño por serie (se informa, no se elige)

Al 100 % del capital por unidad de tamaño (multiplicador > 1 = apalancamiento). La diferencia es el retorno bruto medio por operación sobre el umbral menos el resto y no depende del multiplicador.

| Umbral | Ops sobre umbral | Diferencia (pb) | × | Rentabilidad total | Máx. drawdown | Sharpe |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 1314 | 3,22 | 1,5 | 59,84 % | 14,60 % | 0,62 |
| 15 | 1314 | 3,22 | 2,0 | 87,70 % | 18,62 % | 0,64 |
| 15 | 1314 | 3,22 | 3,0 | 156,44 % | 26,22 % | 0,65 |
| 20 | 641 | 4,54 | 1,5 | 56,13 % | 15,01 % | 0,62 |
| 20 | 641 | 4,54 | 2,0 | 79,18 % | 19,40 % | 0,63 |
| 20 | 641 | 4,54 | 3,0 | 134,21 % | 27,59 % | 0,64 |
| 25 | 301 | 5,34 | 1,5 | 47,85 % | 14,20 % | 0,58 |
| 25 | 301 | 5,34 | 2,0 | 60,76 % | 17,84 % | 0,56 |
| 25 | 301 | 5,34 | 3,0 | 88,98 % | 24,73 % | 0,53 |
| 30 | 127 | 11,37 | 1,5 | 45,93 % | 12,03 % | 0,59 |
| 30 | 127 | 11,37 | 2,0 | 56,70 % | 13,63 % | 0,58 |
| 30 | 127 | 11,37 | 3,0 | 79,91 % | 16,78 % | 0,55 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Los de H007-IS-REAL-003.
- VIX: cierre diario de la sesión previa (16:15 ET), conocido antes de la entrada.
- Al 100 % con ×2 la exposición es del 200 % del capital (apalancamiento).
- Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout.
