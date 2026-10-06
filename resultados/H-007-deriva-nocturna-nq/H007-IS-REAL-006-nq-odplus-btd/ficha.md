# H-007 · ¿Rinde el NQ entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-IS-REAL-006-nq-odplus-btd.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · BtD): 3,66 pb/operación (1264 sesiones frente a 1635); mediana operadas 1,83 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · NQ 15min · experimento H007-IS-REAL-006 · variante **NQ · OD+ BtD**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 1.264 sesiones |
| Sesiones descartadas por el filtro | 1.635 sesiones |
| Retorno medio operadas | 3,66 pb/operación |
| Retorno medio descartadas por el filtro | 1,80 pb/operación |
| Diferencia operadas − descartadas por el filtro | 1,86 pb/operación |
| Mediana operadas | 1,83 pb/operación |
| t de la media operadas (sin bloques) | 4,60 t |
| **Retorno bruto medio por operación (OD+ · BtD)** | **3,66 pb/operación** |
| Intervalo bootstrap 95 % | [2,17; 5,25] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **12 de 12 años**.
- Quitando un año cada vez: entre **3,00 y 3,93 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 1.569,00 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 10,86 | 3,25 | 5,91 | 1,30 | 3,56 | 0,87 | 5,01 | 3,41 | 0,66 | 2,60 | 0,68 | 10,50 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1264 |
| PnL neto | 1.885,00 USD |
| Resultado medio por operación | 1,49 USD |
| Tasa de acierto | 52,29 % |
| Rentabilidad sobre 10.000 USD | 18,85 % |
| Máximo drawdown (tamaño del plan) | 2,29 % |
| Sharpe | 0,85 |
| Costes | 316,00 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **3,53 %** |
| Pico → valle | 2018-11-19 → 2019-06-03 |
| Recuperación | 2020-02-28 |
| Sesiones bajo el agua | 399 |
| Rentabilidad total | 44,69 % |
| Rentabilidad anual | 2,69 % |
| Sharpe | 1,00 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Núcleo elegido tras ver el IS del ES; en el NQ no se ha mirado nada antes de congelar este plan.
- El NQ se mueve muy parecido al ES: no es una muestra independiente.
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6).
- Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del IS; el OOS del NQ no está autorizado.
