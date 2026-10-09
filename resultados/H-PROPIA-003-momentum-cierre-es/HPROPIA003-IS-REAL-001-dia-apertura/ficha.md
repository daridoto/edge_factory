# H-PROPIA-003 · ¿Sigue el ES de 15:30 a 16:00 ET el signo del movimiento 9:30 → 15:30 del mismo día?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-PROPIA-003.md) → [plan](../../../experimentos/H-PROPIA-003-momentum-cierre-es/HPROPIA003-IS-REAL-001-dia-apertura.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (día apertura → 15:30-16:00): 1,61 pb/operación (2810 sesiones); mediana operadas 0,00 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento HPROPIA003-IS-REAL-001 · variante **ES · día desde apertura → 15:30-16:00**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 2.810 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 1,61 pb/operación |
| Mediana operadas | 0 pb/operación |
| t de la media operadas (sin bloques) | 2,68 t |
| Operaciones largos | 1.515 operaciones |
| Retorno medio largos (con signo) | 1,54 pb/operación |
| Operaciones cortos | 1.295 operaciones |
| Retorno medio cortos (con signo) | 1,68 pb/operación |
| Acierto (posición × retorno > 0) | 49,25 % |
| Sesiones con señal = 0 (van cortas) | 26 sesiones |
| β × 100 (retorno ventana sobre señal) | 3,63 β×100 |
| t de β (Newey-West, retardo 8) | 2,19 t |
| R² | 0,67 % |
| R² fuera de muestra recursivo (desde 2014-09) | 0,39 % |
| **Retorno bruto medio por operación (día apertura → 15:30-16:00)** | **1,61 pb/operación** |
| Intervalo bootstrap 95 % | [0,47; 2,85] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **8 de 12 años**.
- Quitando un año cada vez: entre **1,16 y 1,83 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -674,00 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | -0,22 | 3,83 | 6,18 | 0,40 | 2,35 | 0,35 | 2,49 | -0,46 | -0,67 | 2,95 | -0,02 | 0,73 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si precio 15:30 > precio 9:30, corto si no.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2810 |
| PnL neto | 28,50 USD |
| Resultado medio por operación | 0,01 USD |
| Tasa de acierto | 45,73 % |
| Rentabilidad sobre 10.000 USD | 0,29 % |
| Máximo drawdown (tamaño del plan) | 2,41 % |
| Sharpe | 0,03 |
| Costes | 702,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,66 %** |
| Pico → valle | 2011-11-27 → 2018-10-09 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 2827 |
| Rentabilidad total | 5,33 % |
| Rentabilidad anual | 0,37 % |
| Sharpe | 0,11 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Apertura = cierre de la barra de 09:15 (precio a las 9:30); 15:30 = cierre de la barra de 15:15.
- Retorno simple con precios de operación, con rebote bid-ask; señal = 0 va corta (literal del usuario).
- Si falta una barra necesaria, no se opera ese día.
- Sin dato de exposición de los ETF apalancados ni de gamma de los dealers: la señal es solo el precio.
- W3124869677 no encuentra efecto con entrada a partir de las 15:00 sin umbral de ±2 %.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Comparar con H073-IS-REAL-001 (regla del paper). OOS bloqueado.
