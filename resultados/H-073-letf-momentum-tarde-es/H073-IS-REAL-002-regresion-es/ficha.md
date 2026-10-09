# H-073 · ¿Predice el movimiento del día (cierre anterior → 15:30 ET), y más cuanto mayor es, el retorno de 15:30 a 16:00 en el ES?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-073.md) → [plan](../../../experimentos/H-073-letf-momentum-tarde-es/H073-IS-REAL-002-regresion-es.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (día → 15:30-16:00): 1,92 pb/operación (2662 sesiones); mediana operadas 0,77 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H073-IS-REAL-002 · variante **ES · regresión día → 15:30-16:00**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 2.662 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 1,92 pb/operación |
| Mediana operadas | 0,77 pb/operación |
| t de la media operadas (sin bloques) | 3,15 t |
| Operaciones largos | 1.450 operaciones |
| Retorno medio largos (con signo) | 1,50 pb/operación |
| Operaciones cortos | 1.212 operaciones |
| Retorno medio cortos (con signo) | 2,41 pb/operación |
| Acierto (posición × retorno > 0) | 50,08 % |
| Sesiones con señal = 0 (van cortas) | 34 sesiones |
| β × 100 (retorno ventana sobre señal) | 2,91 β×100 |
| t de β (Newey-West, retardo 8) | 2,30 t |
| R² | 0,89 % |
| R² fuera de muestra recursivo (desde 2014-09) | 0,10 % |
| Interacción: β1 × 100 (señal) | 5,18 β×100 |
| Interacción: t de β1 (Newey-West, retardo 8) | 2,11 t |
| Interacción: β2 (señal·|señal|) | -0,76 β |
| Interacción: t de β2 (Newey-West, retardo 8) | -0,84 t |
| Interacción: R² | 1,23 % |
| Interacción: R² fuera de muestra recursivo (desde 2014-09) | -0,36 % |
| Sesiones sin señal (falta barra o roll) | 148 sesiones |
| **Retorno bruto medio por operación (día → 15:30-16:00)** | **1,92 pb/operación** |
| Intervalo bootstrap 95 % | [0,85; 3,09] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **9 de 12 años**.
- Quitando un año cada vez: entre **1,56 y 2,22 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -353,25 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 4,62 | 1,81 | 4,33 | -0,06 | 3,77 | 2,12 | 1,90 | -0,84 | -1,22 | 1,75 | 1,26 | 5,52 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si precio 15:30 / cierre 16:00 previo > 1, corto si no.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2662 |
| PnL neto | 312,25 USD |
| Resultado medio por operación | 0,12 USD |
| Tasa de acierto | 46,51 % |
| Rentabilidad sobre 10.000 USD | 3,12 % |
| Máximo drawdown (tamaño del plan) | 2,79 % |
| Sharpe | 0,23 |
| Costes | 665,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **11,77 %** |
| Pico → valle | 2015-02-03 → 2019-06-12 |
| Recuperación | 2020-03-17 |
| Sesiones bajo el agua | 1593 |
| Rentabilidad total | 14,12 % |
| Rentabilidad anual | 0,95 % |
| Sharpe | 0,24 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Señal = precio 15:30 / cierre 16:00 de la sesión lun-vie anterior − 1; regresión en todas las sesiones con señal y precios.
- Modelo: r(15:30→16:00) = α + β1·señal + β2·señal·|señal|; pendiente marginal β1 + 2·β2·|señal|.
- La operativa (largo/corto por signo) solo traduce la señal a dinero; la prueba es la regresión.
- Si falta una barra necesaria o la señal cruza un roll, no se opera ese día.
- Sin datos de exposición de los ETF apalancados: la señal es solo el precio.
- ES y NQ están muy correlacionados: no son pruebas independientes. RTY no tiene datos intradía.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Comparar ES y NQ. OOS bloqueado.
