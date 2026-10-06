# H-010 · ¿Predicen r1 (cierre anterior → 10:00 ET) y r12 (15:00 → 15:30 ET), cuando coinciden en signo, el de 15:30 → 16:00 ET en el ES?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-010.md) → [plan](../../../experimentos/H-010-momentum-intradia-es/H010-IS-REAL-003-r1-r12.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (r1 + r12 → r13): 0,46 pb/operación (1237 sesiones); mediana operadas -0,00 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H010-IS-REAL-003 · variante **ES · r1 + r12 → r13**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 1.237 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 0,46 pb/operación |
| Mediana operadas | -0 pb/operación |
| t de la media operadas (sin bloques) | 0,46 t |
| Operaciones largos | 684 operaciones |
| Retorno medio largos (con signo) | 0,77 pb/operación |
| Operaciones cortos | 553 operaciones |
| Retorno medio cortos (con signo) | 0,08 pb/operación |
| Acierto (posición × retorno > 0) | 47,21 % |
| β × 100 (retorno ventana sobre señal) | 3,24 β×100 |
| t de β (Newey-West, retardo 8) | 1,70 t |
| R² | 0,53 % |
| R² fuera de muestra recursivo (desde 2014-09) | -0,31 % |
| Sesiones sin acuerdo de señales (no operadas) | 1.425 sesiones |
| Sesiones sin señal (falta barra o roll) | 148 sesiones |
| **Retorno bruto medio por operación (r1 + r12 → r13)** | **0,46 pb/operación** |
| Intervalo bootstrap 95 % | [-1,25; 2,24] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **6 de 12 años**.
- Quitando un año cada vez: entre **0,17 y 0,68 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -551,50 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 0,30 | -0,47 | 0,69 | 1,97 | 2,37 | -1,11 | 3,07 | -1,86 | -1,61 | 2,86 | -0,11 | -0,35 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si r1 (16:00 previa → 10:00 ET) y r12 (15:00 → 15:30 ET) son > 0; corto si ambos < 0; si no, no opera.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1237 |
| PnL neto | -242,25 USD |
| Resultado medio por operación | -0,20 USD |
| Tasa de acierto | 44,06 % |
| Rentabilidad sobre 10.000 USD | -2,42 % |
| Máximo drawdown (tamaño del plan) | 2,64 % |
| Sharpe | -0,22 |
| Costes | 309,25 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **13,15 %** |
| Pico → valle | 2010-07-12 → 2020-03-18 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 3256 |
| Rentabilidad total | -11,14 % |
| Rentabilidad anual | -0,85 % |
| Sharpe | -0,24 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- ES en lugar de SPY (C8); retorno simple con precios de operación, con rebote bid-ask.
- r1 incluye el overnight, como en el paper; sesión previa = lun-vie anterior.
- Si falta una barra necesaria o r1 cruza un roll, no se opera ese día.
- r12 se conoce a las 15:30, el mismo instante de la entrada (como en el paper).
- La regresión de los componentes es la de r13 sobre r1 sola (todas las sesiones con r1), no la conjunta.
- La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).
- El coste de 1,2 pb del paper es el spread de SPY, no el del ES.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Filtro por volatilidad (VIX) en IS. OOS bloqueado.
