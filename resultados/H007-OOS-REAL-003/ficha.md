# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET?

**OOS de H007-IS-REAL-005 · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-007.md) → [plan](../../experimentos/H007-OOS-REAL-003.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+): 0,03 pb/operación (1396 sesiones); mediana operadas 1,10 pb/operación. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-03 → 2026-05-28 · ES 15min · experimento H007-OOS-REAL-003. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 1.396 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 0,03 pb/operación |
| Mediana operadas | 1,10 pb/operación |
| t de la media operadas (sin bloques) | 0,06 t |
| **Retorno bruto medio por operación (OD+)** | **0,03 pb/operación** |
| Intervalo bootstrap 95 % | [-1,08; 1,13] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **3 de 6 años**.
- Quitando un año cada vez: entre **-0,36 y 0,37 pb/operación**.
- **Cambia de signo al excluir 2021, 2025, 2026.**
- PnL de la simulación con costes ×2: -577,50 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/operación | 0,28 | -1,44 | -0,75 | -0,23 | 1,78 | 1,40 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1396 |
| PnL neto | -228,50 USD |
| Resultado medio por operación | -0,16 USD |
| Tasa de acierto | 51,36 % |
| Rentabilidad sobre 10.000 USD | -2,29 % |
| Máximo drawdown (tamaño del plan) | 7,48 % |
| Sharpe | -0,20 |
| Costes | 349,00 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **15,59 %** |
| Pico → valle | 2022-04-13 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1284 |
| Rentabilidad total | -6,85 % |
| Rentabilidad anual | -1,06 % |
| Sharpe | -0,31 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria, no se opera esa noche.
- Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout.
