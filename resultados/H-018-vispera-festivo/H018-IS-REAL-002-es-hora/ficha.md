# H-018 · ¿Se concentra la subida de la víspera de festivo en la última hora de la sesión (15:00-16:00 ET)?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-018.md) → [plan](../../../experimentos/H-018-vispera-festivo/H018-IS-REAL-002-es-hora.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (15:00-16:00): 1,57 pb/hora. El intervalo incluye cero: en IS no se distingue de no tener efecto. En el desglose, 15:00-16:00 ocupa el puesto 5 de 16.

**Muestra:** 2009-11-25 → 2020-12-31 · ES 15min · experimento H018-IS-REAL-002 · variante **ES · última hora de la víspera**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Horas 15:00-16:00 | 76 horas |
| Horas resto | 1.322 horas |
| Retorno medio 15:00-16:00 | 2,21 pb/hora |
| Retorno medio resto | 0,64 pb/hora |
| **Diferencia ventana − resto (15:00-16:00)** | **1,57 pb/hora** |
| Intervalo bootstrap 95 % | [-4,21; 7,32] pb/hora |

Bootstrap por bloques circulares (bloque = 1 × día, 5.000 réplicas, semilla 7301). Las vísperas distan semanas entre sí: sin dependencia que conservar entre días. El intervalo **incluye cero**.

| Desglose | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/hora | 0,53 | 2,04 | 2,91 | 0,00 | 0,33 | -0,21 | 1,52 | -0,63 | 2,32 | 0,26 | -1,20 | 2,72 | -0,73 | -2,80 | 2,33 | 2,21 |

## Robustez

- Positivo en **7 de 12 años**.
- Quitando un año cada vez: entre **0,06 y 2,83 pb/hora**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -9,00 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/hora | -44,82 | 13,79 | 5,24 | 1,36 | 7,48 | -8,22 | -3,59 | 14,36 | -7,80 | 1,13 | 5,58 | -0,74 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la barra de 14:45 ET (precio de las 15:00) de cada víspera.
- **Salida:** Vender al cierre de la barra de 15:45 ET (precio de las 16:00).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 76 |
| PnL neto | 10,00 USD |
| Resultado medio por operación | 0,13 USD |
| Tasa de acierto | 57,89 % |
| Rentabilidad sobre 10.000 USD | 0,10 % |
| Máximo drawdown (tamaño del plan) | 0,39 % |
| Sharpe | 0,33 |
| Costes | 19,00 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **1,50 %** |
| Pico → valle | 2017-02-17 → 2018-11-21 |
| Recuperación | 2020-04-09 |
| Sesiones bajo el agua | 25 |
| Rentabilidad total | 0,61 % |
| Rentabilidad anual | no calculable |
| Sharpe | 0,48 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Víspera por regla (8 festivos de NYSE); hora ET con horario de verano; ts marca el inicio de la barra.
- Resto = horas 0:00-15:00 del mismo día de víspera; la tarde-noche del día anterior (16:00-24:00) no entra.
- Precios sin ajustar por roll; la ventana no cruza la barra del domingo.
- Los días de cierre anticipado (13:00 ET: Nochebuena y a veces 3 de julio) no tienen barra de 15:00: esas vísperas solo cuentan en el resto.
- Unas 89 vísperas: el intervalo será ancho.
- Es una huella indirecta: sin datos de posiciones cortas no se distingue el cierre de cortos de otros compradores de fin de sesión.

## Siguiente comprobación (propuesta, sin ejecutar)

Según el resultado: comparar con la duración del cierre (festivos de fin de semana largo frente a uno), en IS.
