# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET?

**Total de H007-IS-REAL-005 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-TOT-REAL-003-odplus.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+): 1,78 pb/operación (4299 sesiones); mediana operadas 1,24 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2026-05-28 · ES 15min · experimento H007-TOT-REAL-003 · variante **OD+**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 4.299 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 1,78 pb/operación |
| Mediana operadas | 1,24 pb/operación |
| t de la media operadas (sin bloques) | 4,76 t |
| **Retorno bruto medio por operación (OD+)** | **1,78 pb/operación** |
| Intervalo bootstrap 95 % | [0,99; 2,65] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **15 de 18 años**.
- Quitando un año cada vez: entre **1,45 y 1,99 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -586,75 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 7,13 | 2,31 | 3,71 | 1,74 | 2,26 | 0,99 | 3,87 | 2,76 | 0,76 | 1,88 | 0,36 | 6,95 | 0,28 | -1,44 | -0,75 | -0,23 | 1,78 | 1,40 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 4299 |
| PnL neto | 488,00 USD |
| Resultado medio por operación | 0,11 USD |
| Tasa de acierto | 49,06 % |
| Rentabilidad sobre 10.000 USD | 4,88 % |
| Máximo drawdown (tamaño del plan) | 6,99 % |
| Sharpe | 0,22 |
| Costes | 1.074,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **15,59 %** |
| Pico → valle | 2022-04-13 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1284 |
| Rentabilidad total | 32,59 % |
| Rentabilidad anual | 1,38 % |
| Sharpe | 0,41 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria, no se opera esa noche.
- Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout.
