# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?

**OOS de H007-IS-REAL-003 · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-007.md) → [plan](../../experimentos/H007-OOS-REAL-001.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · BtD): 0,35 pb/operación (663 sesiones frente a 733); mediana operadas 1,26 pb/operación. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-03 → 2026-05-28 · ES 15min · experimento H007-OOS-REAL-001. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 663 sesiones |
| Sesiones descartadas por el filtro | 733 sesiones |
| Retorno medio operadas | 0,35 pb/operación |
| Retorno medio descartadas por el filtro | -0,25 pb/operación |
| Diferencia operadas − descartadas por el filtro | 0,60 pb/operación |
| Mediana operadas | 1,26 pb/operación |
| t de la media operadas (sin bloques) | 0,35 t |
| **Retorno bruto medio por operación (OD+ · BtD)** | **0,35 pb/operación** |
| Intervalo bootstrap 95 % | [-1,44; 2,25] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 6 años**.
- Quitando un año cada vez: entre **0,09 y 0,97 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -153,75 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/operación | 0,87 | -2,34 | 1,07 | -0,56 | 1,35 | 3,61 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 663 |
| PnL neto | 12,00 USD |
| Resultado medio por operación | 0,02 USD |
| Tasa de acierto | 51,73 % |
| Rentabilidad sobre 10.000 USD | 0,12 % |
| Máximo drawdown (tamaño del plan) | 4,65 % |
| Sharpe | 0,02 |
| Costes | 165,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,42 %** |
| Pico → valle | 2022-05-10 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1262 |
| Rentabilidad total | -1,32 % |
| Rentabilidad anual | -0,20 % |
| Sharpe | -0,07 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Ventana y filtro elegidos tras ver el IS (H007-IS-REAL-002): el OOS mide si sobrevive a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.
- La primera noche OOS no tiene señal previa cargada (2020-12-31 es IS) y no opera.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario si se lleva a OOS el núcleo con VIX (004); necesita su propia autorización.
