# H-010 · ¿Predice el signo del retorno 9:30 → 10:00 ET el de 15:30 → 16:00 ET en el ES cuando el VIX está alto?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-010.md) → [plan](../../../experimentos/H-010-momentum-intradia-es/H010-IS-REAL-004-r1-apertura-vix.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (r1 apertura → r13): 2,40 pb/operación (759 sesiones frente a 1960); mediana operadas 2,91 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H010-IS-REAL-004 · variante **ES · r1 apertura → r13 · VIX ≥ 20**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 759 sesiones |
| Sesiones descartadas por el filtro | 1.960 sesiones |
| Retorno medio operadas | 2,40 pb/operación |
| Retorno medio descartadas por el filtro | 0,01 pb/operación |
| Diferencia operadas − descartadas por el filtro | 2,39 pb/operación |
| Mediana operadas | 2,91 pb/operación |
| t de la media operadas (sin bloques) | 1,24 t |
| Operaciones largos | 364 operaciones |
| Retorno medio largos (con signo) | 3,45 pb/operación |
| Operaciones cortos | 395 operaciones |
| Retorno medio cortos (con signo) | 1,43 pb/operación |
| Acierto (posición × retorno > 0) | 52,70 % |
| Sesiones con señal = 0 (van cortas) | 61 sesiones |
| β × 100 (retorno ventana sobre señal) | 6,11 β×100 |
| t de β (Newey-West, retardo 8) | 1,61 t |
| R² | 0,32 % |
| R² fuera de muestra recursivo (desde 2014-09) | 0,15 % |
| Años sin comparación posible (un lado vacío) | 1 años |
| **Retorno bruto medio por operación (r1 apertura → r13)** | **2,40 pb/operación** |
| Intervalo bootstrap 95 % | [-0,86; 5,81] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **9 de 11 años**.
- Quitando un año cada vez: entre **2,01 y 2,85 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -103,75 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 1,54 | 2,12 | 2,34 | 8,72 | 23,81 | 1,71 | -1,88 | 1,33 | -3,46 | 8,50 | 3,41 |

## Simulación de la operativa

- **Entrada:** A las 15:30 ET (cierre de la barra de 15:15), lun-vie: si el VIX al cierre de la sesión previa es ≥ 20: largo si el retorno 9:30 → 10:00 ET es > 0, corto si no.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 759 |
| PnL neto | 86,00 USD |
| Resultado medio por operación | 0,11 USD |
| Tasa de acierto | 50,33 % |
| Rentabilidad sobre 10.000 USD | 0,86 % |
| Máximo drawdown (tamaño del plan) | 2,54 % |
| Sharpe | 0,07 |
| Costes | 189,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,40 %** |
| Pico → valle | 2015-08-25 → 2020-03-17 |
| Recuperación | 2020-03-27 |
| Sesiones bajo el agua | 1428 |
| Rentabilidad total | 5,39 % |
| Rentabilidad anual | 0,38 % |
| Sharpe | 0,12 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- ES en lugar de SPY (C8); retorno simple con precios de operación, con rebote bid-ask.
- r1 = precio 10:00 / precio 9:30 − 1 (cierres de las barras de 09:45 y 09:15), sin overnight.
- Si falta una barra necesaria o el VIX de la sesión previa, no se opera ese día.
- VIX: cierre de la sesión lun-vie anterior (16:15 ET), conocido antes de la entrada.
- Variante elegida tras ver 001-003: el efecto de 002 se concentraba en años de volatilidad alta (sesgo de selección).
- Umbral 20 fijado antes de calcular (≈ mediana del VIX, el mismo de H-007); sin barrido de umbrales.
- La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).
- El coste de 1,2 pb del paper es el spread de SPY, no el del ES.
- La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario si H-010 se descarta o se lleva a OOS. OOS bloqueado.
