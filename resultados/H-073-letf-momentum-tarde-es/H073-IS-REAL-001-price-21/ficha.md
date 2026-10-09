# H-073 · ¿Sigue el ES de 14:45 al cierre el signo de un movimiento ≥ |2 %| desde el cierre anterior?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-073.md) → [plan](../../../experimentos/H-073-letf-momentum-tarde-es/H073-IS-REAL-001-price-21.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (price-21): 14,40 pb/operación (119 sesiones frente a 2543); mediana operadas 8,63 pb/operación. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H073-IS-REAL-001 · variante **ES · price-21 (±2 % a las 14:45)**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 119 sesiones |
| Sesiones descartadas por el filtro | 2.543 sesiones |
| Retorno medio operadas | 14,40 pb/operación |
| Retorno medio descartadas por el filtro | 0,21 pb/operación |
| Diferencia operadas − descartadas por el filtro | 14,19 pb/operación |
| Mediana operadas | 8,63 pb/operación |
| t de la media operadas (sin bloques) | 1,43 t |
| Operaciones largos | 50 operaciones |
| Retorno medio largos (con signo) | 25,79 pb/operación |
| Operaciones cortos | 69 operaciones |
| Retorno medio cortos (con signo) | 6,14 pb/operación |
| Acierto (posición × retorno > 0) | 56,30 % |
| Sesiones con señal = 0 (van cortas) | 28 sesiones |
| β × 100 (retorno ventana sobre señal) | 2,24 β×100 |
| t de β (Newey-West, retardo 8) | 1,27 t |
| R² | 0,25 % |
| R² fuera de muestra recursivo (desde 2014-09) | 0,16 % |
| Sesiones sin señal (falta barra o roll) | 148 sesiones |
| Años sin comparación posible (un lado vacío) | 1 años |
| **Retorno bruto medio por operación (price-21)** | **14,40 pb/operación** |
| Intervalo bootstrap 95 % | [-2,35; 33,33] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **incluye cero**.

## Robustez

- Positivo en **9 de 11 años**.
- Quitando un año cada vez: entre **10,88 y 17,38 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 213,50 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 14,89 | 9,26 | 26,89 | 22,14 | 47,21 | 8,63 | 94,56 | -21,57 | 21,86 | -10,14 | 9,67 |

## Simulación de la operativa

- **Entrada:** A las 14:45 ET (cierre de la barra de 14:30), lun-vie, si |precio 14:45 / cierre 16:00 previo − 1| ≥ 2 %: largo si > 0, corto si < 0.
- **Salida:** A las 16:00 ET (cierre de la barra de 15:45).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 119 |
| PnL neto | 243,25 USD |
| Resultado medio por operación | 2,04 USD |
| Tasa de acierto | 53,78 % |
| Rentabilidad sobre 10.000 USD | 2,43 % |
| Máximo drawdown (tamaño del plan) | 2,48 % |
| Sharpe | 0,24 |
| Costes | 29,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **8,20 %** |
| Pico → valle | 2020-03-17 → 2020-11-09 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 246 |
| Rentabilidad total | 15,83 % |
| Rentabilidad anual | 1,06 % |
| Sharpe | 0,34 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- ES en lugar de la cesta del S&P 500 (C8); cierre previo = cierre de la barra de 15:45 de la sesión lun-vie anterior.
- Resto de la evidencia: sesiones con |señal| < 2 %, con la misma dirección por signo (contraste de refutación del paper).
- Si falta una barra necesaria o la señal cruza un roll, no se opera ese día.
- Pocas operaciones esperadas (el paper: 128 días en 2006-2011, con la crisis); la IS empieza en 2009.
- El paper no incluye costes; aquí 1 tick por operación.
- Solo la ventana 21; 19 y 20 sin probar. La regla de roll anterior a 2022 no está verificada (C6).

## Siguiente comprobación (propuesta, sin ejecutar)

Comparar con HPROPIA003-IS-REAL-001. OOS bloqueado.
