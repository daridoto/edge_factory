# H-PROPIA-001 · ¿Rinde RAY en los 28 días siguientes a que el volumen de Raydium doble su nivel normal?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-PROPIA-001.md) → [plan](../../experimentos/HPROPIA001-IS-REAL-001.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno neto medio por operación (VOL×2): 37,51 % / operación en 16 operaciones; mediana 11,08 %, t 2,44. Placebo: percentil 99 (p95 30,98 %). El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2022-08-15 → 2026-09-29 · RAY 1d · experimento HPROPIA001-IS-REAL-001. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Operaciones cerradas | 16 operaciones |
| Sorteos placebo | 2.000 sorteos |
| Retorno neto medio por operación | 37,51 % / operación |
| Media del placebo | 12,66 % / operación |
| Mediana por operación | 11,08 % |
| t de la media | 2,44 t |
| Percentil 95 del placebo | 30,98 % / operación |
| Percentil del resultado en el placebo | 98,85 % |
| Señales sin cerrar al final de la muestra | 1 operaciones |
| Exceso medio frente a BTC | 31,01 % |
| **Retorno neto medio por operación (VOL×2)** | **37,51 % / operación** |
| Intervalo bootstrap 95 % | [9,41; 68,22] % / operación |

Bootstrap por bloques circulares (bloque = 1 × operación, 5.000 réplicas, semilla 7301). Las operaciones no se solapan (enfriamiento = tenencia); con 16 operaciones no caben bloques más largos. El intervalo **no incluye cero**.

## Robustez

- Positivo en **3 de 5 años**.
- Quitando un año cada vez: entre **27,97 y 46,49 % / operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 343.888,84 USDT.

| Año | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|
| % / operación | -25,30 | 53,42 | 39,33 | -25,30 | 119,55 |

## Simulación de la operativa

- **Entrada:** Largo a la apertura del día siguiente a la señal (mediana 7 d / mediana 90 d del volumen de Raydium ≥ 2).
- **Salida:** Stop −25 % (al stop, o a la apertura si abre por debajo); si no, al cierre del día t + 28.
- **Tamaño:** 100 % de la equity, una operación a la vez, sin apalancamiento; 28 días sin señales tras cada una.
- **Costes:** 0,2 % del nocional por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 16 |
| PnL neto | 367.278,43 USDT |
| Resultado medio por operación | 22.954,90 USDT |
| Tasa de acierto | 62,50 % |
| Rentabilidad sobre 10.000 USDT | 3.672,78 % |
| Máximo drawdown | 54,15 % |
| Sharpe | 1,34 |
| Costes | 7.734,11 USDT |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Velas diarias UTC de Binance spot; el volumen de DefiLlama se da por conocido al cierre UTC de su día.
- Las medianas cuentan días con dato: los 4 huecos de DefiLlama se saltan, como en la implementación del usuario.
- El stop se ejecuta exactamente al nivel salvo gap de apertura; sin más deslizamiento.
- Exceso frente a BTC: del cierre del día de señal (≈ apertura de entrada) al cierre del día de salida.
- Parámetros (stop, día 28) elegidos por el usuario mirando todo el histórico: la muestra IS no es independiente de ellos.
- Un solo token y pocas operaciones: el resultado depende de unas pocas operaciones grandes.
- DefiLlama no es point-in-time: el volumen se revisa hacia atrás.
- Rentabilidad y drawdown con el 100 % de la equity en un token muy volátil: miden la cuenta, no el edge.

## Siguiente comprobación (propuesta, sin ejecutar)

Seguimiento en tiempo real desde el 2026-09-30 con los criterios de refutación del usuario (≥ 10 operaciones).
