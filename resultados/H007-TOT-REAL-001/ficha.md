# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?

**Total de H007-IS-REAL-003 · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-007.md) → [plan](../../experimentos/H007-TOT-REAL-001.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · BtD): 2,71 pb/operación (1909 sesiones frente a 2390); mediana operadas 2,09 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2026-05-28 · ES 15min · experimento H007-TOT-REAL-001. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 1.909 sesiones |
| Sesiones descartadas por el filtro | 2.390 sesiones |
| Retorno medio operadas | 2,71 pb/operación |
| Retorno medio descartadas por el filtro | 1,04 pb/operación |
| Diferencia operadas − descartadas por el filtro | 1,67 pb/operación |
| Mediana operadas | 2,09 pb/operación |
| t de la media operadas (sin bloques) | 4,45 t |
| **Retorno bruto medio por operación (OD+ · BtD)** | **2,71 pb/operación** |
| Intervalo bootstrap 95 % | [1,53; 3,94] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **16 de 18 años**.
- Quitando un año cada vez: entre **2,27 y 3,06 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 182,25 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 10,72 | 3,43 | 5,86 | 2,79 | 4,53 | 2,54 | 4,72 | 3,35 | 0,67 | 2,36 | 1,45 | 9,17 | 0,87 | -2,34 | 1,07 | -0,56 | 1,35 | 3,61 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1909 |
| PnL neto | 659,50 USD |
| Resultado medio por operación | 0,35 USD |
| Tasa de acierto | 51,91 % |
| Rentabilidad sobre 10.000 USD | 6,59 % |
| Máximo drawdown (tamaño del plan) | 4,38 % |
| Sharpe | 0,40 |
| Costes | 477,25 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,42 %** |
| Pico → valle | 2022-05-10 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1262 |
| Rentabilidad total | 35,70 % |
| Rentabilidad anual | 1,49 % |
| Sharpe | 0,59 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Ventana y filtro elegidos tras ver el IS (H007-IS-REAL-002): el OOS mide si sobrevive a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario si se lleva a OOS el núcleo con VIX (004); necesita su propia autorización.
