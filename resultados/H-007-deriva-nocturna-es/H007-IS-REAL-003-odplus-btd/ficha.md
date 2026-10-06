# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-003-odplus-btd.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · BtD): 3,97 pb/operación (1246 sesiones frente a 1657); mediana operadas 2,69 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H007-IS-REAL-003 · variante **OD+ BtD**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 1.246 sesiones |
| Sesiones descartadas por el filtro | 1.657 sesiones |
| Retorno medio operadas | 3,97 pb/operación |
| Retorno medio descartadas por el filtro | 1,61 pb/operación |
| Diferencia operadas − descartadas por el filtro | 2,36 pb/operación |
| Mediana operadas | 2,69 pb/operación |
| t de la media operadas (sin bloques) | 5,17 t |
| **Retorno bruto medio por operación (OD+ · BtD)** | **3,97 pb/operación** |
| Intervalo bootstrap 95 % | [2,42; 5,50] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **12 de 12 años**.
- Quitando un año cada vez: entre **3,40 y 4,28 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 336,00 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 10,72 | 3,43 | 5,86 | 2,79 | 4,53 | 2,54 | 4,72 | 3,35 | 0,67 | 2,36 | 1,45 | 9,17 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1246 |
| PnL neto | 647,50 USD |
| Resultado medio por operación | 0,52 USD |
| Tasa de acierto | 52,01 % |
| Rentabilidad sobre 10.000 USD | 6,48 % |
| Máximo drawdown (tamaño del plan) | 1,07 % |
| Sharpe | 0,87 |
| Costes | 311,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **3,93 %** |
| Pico → valle | 2018-04-17 → 2019-06-03 |
| Recuperación | 2020-02-28 |
| Sesiones bajo el agua | 585 |
| Rentabilidad total | 37,52 % |
| Rentabilidad anual | 2,32 % |
| Sharpe | 0,91 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Ventana y filtro elegidos tras ver el IS en el dashboard (H007-IS-REAL-002): sesgo de selección.
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6).
- Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).

## Siguiente comprobación (propuesta, sin ejecutar)

H007-IS-REAL-004: añadir el tamaño por VIX sobre este núcleo. OOS sigue bloqueado.
