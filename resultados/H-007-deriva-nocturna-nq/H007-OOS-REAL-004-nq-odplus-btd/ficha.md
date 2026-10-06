# H-007 · ¿Rinde el NQ entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?

**OOS de H007-IS-REAL-006 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-OOS-REAL-004-nq-odplus-btd.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · BtD): 0,99 pb/operación (646 sesiones frente a 750); mediana operadas 2,55 pb/operación. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-03 → 2026-05-28 · NQ 15min · experimento H007-OOS-REAL-004 · variante **NQ · OD+ BtD**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 646 sesiones |
| Sesiones descartadas por el filtro | 750 sesiones |
| Retorno medio operadas | 0,99 pb/operación |
| Retorno medio descartadas por el filtro | 0,03 pb/operación |
| Diferencia operadas − descartadas por el filtro | 0,96 pb/operación |
| Mediana operadas | 2,55 pb/operación |
| t de la media operadas (sin bloques) | 0,86 t |
| **Retorno bruto medio por operación (OD+ · BtD)** | **0,99 pb/operación** |
| Intervalo bootstrap 95 % | [-1,30; 3,29] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **5 de 6 años**.
- Quitando un año cada vez: entre **0,27 y 2,21 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 1.212,25 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/operación | 3,96 | -4,00 | 0,78 | 1,12 | 1,47 | 5,79 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 646 |
| PnL neto | 1.373,75 USD |
| Resultado medio por operación | 2,13 USD |
| Tasa de acierto | 55,42 % |
| Rentabilidad sobre 10.000 USD | 13,74 % |
| Máximo drawdown (tamaño del plan) | 11,76 % |
| Sharpe | 0,45 |
| Costes | 161,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **9,97 %** |
| Pico → valle | 2022-04-21 → 2023-07-20 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1278 |
| Rentabilidad total | 5,24 % |
| Rentabilidad anual | 0,77 % |
| Sharpe | 0,28 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Parámetros elegidos tras ver el IS (y conociendo el OOS del ES): el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout del NQ.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout del NQ.
