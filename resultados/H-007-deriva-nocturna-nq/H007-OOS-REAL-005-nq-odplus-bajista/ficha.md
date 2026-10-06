# H-007 · ¿Rinde el NQ entre las 01:30 y las 03:30 ET cuando está por debajo de su media de 200 sesiones?

**OOS de H007-IS-REAL-008 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-OOS-REAL-005-nq-odplus-bajista.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · bajista): 1,13 pb/operación (305 sesiones frente a 1030); mediana operadas 0,00 pb/operación. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-03 → 2026-05-28 · NQ 15min · experimento H007-OOS-REAL-005 · variante **NQ · OD+ bajista**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 305 sesiones |
| Sesiones descartadas por el filtro | 1.030 sesiones |
| Retorno medio operadas | 1,13 pb/operación |
| Retorno medio descartadas por el filtro | 0,39 pb/operación |
| Diferencia operadas − descartadas por el filtro | 0,74 pb/operación |
| Mediana operadas | 0 pb/operación |
| t de la media operadas (sin bloques) | 0,46 t |
| Años sin comparación posible (un lado vacío) | 2 años |
| **Retorno bruto medio por operación (OD+ · bajista)** | **1,13 pb/operación** |
| Intervalo bootstrap 95 % | [-3,28; 5,73] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **2 de 4 años**.
- Quitando un año cada vez: entre **-1,28 y 8,60 pb/operación**.
- **Cambia de signo al excluir 2025.**
- PnL de la simulación con costes ×2: 834,75 USD.

| Año | 2022 | 2023 | 2025 | 2026 |
|---|---:|---:|---:|---:|
| pb/operación | -1,26 | -3,27 | 15,39 | 1,51 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el precio de las 16:15 de la sesión previa está en o por debajo de su media de 200 sesiones.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 305 |
| PnL neto | 911,00 USD |
| Resultado medio por operación | 2,99 USD |
| Tasa de acierto | 49,18 % |
| Rentabilidad sobre 10.000 USD | 9,11 % |
| Máximo drawdown (tamaño del plan) | 13,36 % |
| Sharpe | 0,33 |
| Costes | 76,25 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,73 %** |
| Pico → valle | 2022-04-13 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1284 |
| Rentabilidad total | 2,62 % |
| Rentabilidad anual | 0,39 % |
| Sharpe | 0,15 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Parámetros elegidos tras ver el IS (y conociendo el OOS del ES): el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout del NQ.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout del NQ.
