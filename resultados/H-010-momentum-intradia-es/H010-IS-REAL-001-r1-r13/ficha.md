# H-010 · ¿Predice el signo del retorno cierre anterior → 10:00 ET el de 15:30 → 16:00 ET en el ES?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-010.md) → [plan](../../../experimentos/H-010-momentum-intradia-es/H010-IS-REAL-001-r1-r13.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (r1 → r13): 0,28 pb/operación (2662 sesiones); mediana operadas 0,00 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H010-IS-REAL-001 · variante **ES · r1 → r13**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 2.662 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 0,28 pb/operación |
| Mediana operadas | 0 pb/operación |
| t de la media operadas (sin bloques) | 0,45 t |
| Operaciones largos | 1.391 operaciones |
| Retorno medio largos (con signo) | -0,01 pb/operación |
| Operaciones cortos | 1.271 operaciones |
| Retorno medio cortos (con signo) | 0,58 pb/operación |
| Acierto (posición × retorno > 0) | 47,97 % |
| Sesiones con señal = 0 (van cortas) | 39 sesiones |
| β × 100 (retorno ventana sobre señal) | 3,24 β×100 |
| t de β (Newey-West, retardo 8) | 1,70 t |
| R² | 0,53 % |
| R² fuera de muestra recursivo (desde 2014-09) | -0,31 % |
| Sesiones sin señal (falta barra o roll) | 148 sesiones |
| **Retorno bruto medio por operación (r1 → r13)** | **0,28 pb/operación** |
| Intervalo bootstrap 95 % | [-0,87; 1,45] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **8 de 12 años**.
- Quitando un año cada vez: entre **0,12 y 0,41 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -1.308,75 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | -3,21 | 0,66 | 1,56 | 1,39 | 1,88 | 0,06 | 0,35 | -0,94 | -1,10 | -0,32 | 0,15 | 0,23 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si el retorno 16:00 previa → 10:00 ET es > 0, corto si no.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2662 |
| PnL neto | -643,25 USD |
| Resultado medio por operación | -0,24 USD |
| Tasa de acierto | 44,59 % |
| Rentabilidad sobre 10.000 USD | -6,43 % |
| Máximo drawdown (tamaño del plan) | 6,98 % |
| Sharpe | -0,46 |
| Costes | 665,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **28,91 %** |
| Pico → valle | 2010-06-02 → 2020-03-06 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 3290 |
| Rentabilidad total | -26,26 % |
| Rentabilidad anual | -2,17 % |
| Sharpe | -0,48 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- ES en lugar de SPY (C8); retorno simple con precios de operación, con rebote bid-ask.
- r1 incluye el overnight, como en el paper; sesión previa = lun-vie anterior.
- Si falta una barra necesaria o r1 cruza un roll, no se opera ese día.
- La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).
- El coste de 1,2 pb del paper es el spread de SPY, no el del ES.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Variantes de la receta en IS: r1 desde la apertura de las 9:30 (sin overnight) y señal combinada r1 + r12. OOS bloqueado.
