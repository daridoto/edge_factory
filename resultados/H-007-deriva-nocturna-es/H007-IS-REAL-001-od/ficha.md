# H-007 · ¿Rinde más el ES entre las 2:00 y las 3:00 ET que en cualquier otra hora?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-001-od.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno medio en la ventana (02:00-03:00): 1,63 pb/hora. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura. En el desglose, 02:00-03:00 ocupa el puesto 1 de 23.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H007-IS-REAL-001 · variante **OD**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Horas 02:00-03:00 | 2.903 horas |
| Horas resto | 62.615 horas |
| Retorno medio 02:00-03:00 | 1,63 pb/hora |
| Retorno medio resto | 0,19 pb/hora |
| **Retorno medio en la ventana (02:00-03:00)** | **1,63 pb/hora** |
| Intervalo bootstrap 95 % | [1,01; 2,29] pb/hora |

Bootstrap por bloques circulares (bloque = 5 × día, 5.000 réplicas, semilla 7301). Observaciones diarias; bloques de 5 días (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

| Desglose | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/hora | 0,66 | 0,38 | 1,63 | 0,32 | 0,19 | 0,43 | 0,48 | -0,07 | -0,10 | 0,21 | -0,04 | 0,64 | 0,86 | -0,50 | 0,26 | 0,25 | 0,21 | -0,86 | 0,68 | -0,26 | 0,26 | -0,05 | -0,09 |

## Robustez

- Positivo en **11 de 12 años**.
- Quitando un año cada vez: entre **1,38 y 1,84 pb/hora**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -578,25 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/hora | 1,38 | 2,86 | 2,16 | 1,11 | 0,98 | 0,98 | 2,59 | 1,84 | 0,44 | 1,30 | -0,50 | 4,20 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la barra de 01:45 ET (precio de las 02:00), de lunes a viernes.
- **Salida:** Vender al cierre de la barra de 02:45 ET (precio de las 03:00).
- **Tamaño:** 1 unidad del índice (1 USD por punto, no el multiplicador de 50 USD del contrato); sin apalancamiento.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2903 |
| PnL neto | 147,50 USD |
| Resultado medio por operación | 0,05 USD |
| Tasa de acierto | 43,02 % |
| Rentabilidad sobre 10.000 USD | 1,48 % |
| Máximo drawdown (tamaño del plan) | 1,93 % |
| Sharpe | 0,21 |
| Costes | 725,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **6,55 %** |
| Pico → valle | 2018-04-15 → 2020-02-25 |
| Recuperación | 2020-03-24 |
| Sesiones bajo el agua | 607 |
| Rentabilidad total | 7,38 % |
| Rentabilidad anual | 0,51 % |
| Sharpe | 0,23 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes como el paper: hay rebote bid-ask.
- Precios sin ajustar por roll; la ventana 02:00-03:00 no cruza la barra del domingo 18:00.
- Si falta una barra necesaria, no se opera ni se mide esa hora.
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6); no afecta a la ventana, sí a horas del domingo.
- La simulación usa 1 unidad del índice: la rentabilidad de cuenta no mide el edge.
- No se ejecutan la t con Bonferroni, las submuestras por día de la semana ni la prueba de desfase horario.

## Siguiente comprobación (propuesta, sin ejecutar)

En IS, submuestras por día de la semana y prueba de las semanas de desfase horario (parte C de la receta). OOS sigue bloqueado.
