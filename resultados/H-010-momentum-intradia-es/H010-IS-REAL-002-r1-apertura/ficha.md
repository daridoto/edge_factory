# H-010 · ¿Predice el signo del retorno 9:30 → 10:00 ET el de 15:30 → 16:00 ET en el ES?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-010.md) → [plan](../../../experimentos/H-010-momentum-intradia-es/H010-IS-REAL-002-r1-apertura.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (r1 apertura → r13): 0,56 pb/operación (2810 sesiones); mediana operadas 0,00 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H010-IS-REAL-002 · variante **ES · r1 apertura → r13**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 2.810 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 0,56 pb/operación |
| Mediana operadas | 0 pb/operación |
| t de la media operadas (sin bloques) | 0,93 t |
| Operaciones largos | 1.367 operaciones |
| Retorno medio largos (con signo) | 0,63 pb/operación |
| Operaciones cortos | 1.443 operaciones |
| Retorno medio cortos (con signo) | 0,49 pb/operación |
| Acierto (posición × retorno > 0) | 49,11 % |
| Sesiones con señal = 0 (van cortas) | 61 sesiones |
| β × 100 (retorno ventana sobre señal) | 6,11 β×100 |
| t de β (Newey-West, retardo 8) | 1,61 t |
| R² | 0,32 % |
| R² fuera de muestra recursivo (desde 2014-09) | 0,15 % |
| **Retorno bruto medio por operación (r1 apertura → r13)** | **0,56 pb/operación** |
| Intervalo bootstrap 95 % | [-0,48; 1,67] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **8 de 12 años**.
- Quitando un año cada vez: entre **0,37 y 0,81 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -1.253,50 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 2,49 | 1,56 | 1,12 | 2,40 | 1,38 | -1,11 | 0,25 | -0,09 | 0,28 | -2,07 | -0,59 | 2,50 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si el retorno 9:30 → 10:00 ET es > 0, corto si no.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2810 |
| PnL neto | -551,00 USD |
| Resultado medio por operación | -0,20 USD |
| Tasa de acierto | 45,73 % |
| Rentabilidad sobre 10.000 USD | -5,51 % |
| Máximo drawdown (tamaño del plan) | 8,25 % |
| Sharpe | -0,37 |
| Costes | 702,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **31,24 %** |
| Pico → valle | 2010-05-13 → 2020-03-17 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 3307 |
| Rentabilidad total | -21,52 % |
| Rentabilidad anual | -1,73 % |
| Sharpe | -0,36 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- ES en lugar de SPY (C8); retorno simple con precios de operación, con rebote bid-ask.
- r1 = precio 10:00 / precio 9:30 − 1 (cierres de las barras de 09:45 y 09:15), sin overnight.
- Si falta una barra necesaria, no se opera ese día.
- La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).
- El coste de 1,2 pb del paper es el spread de SPY, no el del ES.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Señal combinada r1 + r12 y filtro por volatilidad (VIX), en IS. OOS bloqueado.
