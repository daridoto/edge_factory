# H-007 · Tras una última hora vendedora, ¿rebota más el NQ de 01:30 a 03:30 ET en tendencia alcista que en bajista?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-IS-REAL-007-nq-btd-tendencia.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia alcista − bajista (OD+ · BtD): -5,04 pb/operación (1021 sesiones frente a 154); mediana alcista 1,79 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · NQ 15min · experimento H007-IS-REAL-007 · variante **NQ · OD+ BtD × tendencia**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones alcista | 1.021 sesiones |
| Sesiones bajista | 154 sesiones |
| Retorno medio alcista | 2,66 pb/operación |
| Retorno medio bajista | 7,70 pb/operación |
| Diferencia alcista − bajista | -5,04 pb/operación |
| Mediana alcista | 1,79 pb/operación |
| t de la media alcista (sin bloques) | 3,97 t |
| Años sin comparación posible (un lado vacío) | 2 años |
| **Diferencia alcista − bajista (OD+ · BtD)** | **-5,04 pb/operación** |
| Intervalo bootstrap 95 % | [-13,79; 2,45] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 9 años**.
- Quitando un año cada vez: entre **-6,52 y -2,70 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 1.569,00 USD.

| Año | 2010 | 2011 | 2012 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 4,37 | -15,75 | 5,67 | -17,81 | -6,48 | 0,27 | -4,73 | 7,62 | -30,21 |

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

## Control: la misma partición en las sesiones que el filtro descarta

Retorno bruto medio por operación (pb). Operadas: 1021 alcista · 154 bajista; descartadas: 1224 alcista · 187 bajista. Diferencia alcista − bajista en las descartadas: **-8,48** [-17,11; -1,64]. «Filtro aporta» = operadas − descartadas en cada lado.

| muestra | operadas alcista | operadas bajista | descartadas alcista | descartadas bajista | filtro aporta (alcista) | filtro aporta (bajista) |
|---|---:|---:|---:|---:|---:|---:|
| toda la muestra | 2,66 | 7,70 | 0,66 | 9,14 | 2,00 | -1,44 |
| sin 2009 | 2,66 | 7,70 | 0,66 | 9,14 | 2,00 | -1,44 |
| sin 2010 | 2,75 | 8,85 | 0,79 | 9,21 | 1,96 | -0,36 |
| sin 2011 | 2,70 | 5,40 | 0,64 | 10,67 | 2,06 | -5,27 |
| sin 2012 | 2,74 | 8,75 | 0,57 | 9,70 | 2,17 | -0,95 |
| sin 2013 | 2,53 | 7,70 | 0,77 | 9,14 | 1,76 | -1,44 |
| sin 2014 | 2,91 | 7,56 | 0,64 | 9,14 | 2,27 | -1,58 |
| sin 2015 | 2,50 | 7,44 | 0,51 | 8,86 | 1,99 | -1,42 |
| sin 2016 | 2,60 | 9,11 | 0,55 | 10,82 | 2,05 | -1,71 |
| sin 2017 | 2,89 | 7,70 | 0,83 | 9,14 | 2,06 | -1,44 |
| sin 2018 | 2,75 | 7,90 | 0,64 | 9,83 | 2,11 | -1,93 |
| sin 2019 | 2,75 | 9,16 | 0,64 | 10,15 | 2,10 | -0,99 |
| sin 2020 | 2,16 | 5,18 | 0,68 | 4,58 | 1,48 | 0,60 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- La idea sale del OOS del ES (2022, mercado bajista): se declara; aquí solo se usa IS del NQ.
- En 2009-2020 el NQ estuvo casi siempre en tendencia alcista: el grupo bajista es pequeño y su IC, ancho.
- Las primeras 200 sesiones no tienen tendencia y quedan fuera de la comparación.
- El NQ se mueve muy parecido al ES: no es una muestra independiente.
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6).
- Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).

## Siguiente comprobación (propuesta, sin ejecutar)

Interpretar con el usuario; para entender el mecanismo, no para operar. OOS no autorizado.
