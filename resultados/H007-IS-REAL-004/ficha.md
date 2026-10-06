# H-007 · Dentro del núcleo OD+ · BtD, ¿rinde más el ES las noches con VIX previo > 20?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../estrategias/H-007.md) → [plan](../../experimentos/H007-IS-REAL-004.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2): 7,35 pb/operación (385 sesiones frente a 861); mediana VIX > 20 6,86 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H007-IS-REAL-004. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones VIX > 20 | 385 sesiones |
| Sesiones VIX ≤ 20 | 861 sesiones |
| Retorno medio VIX > 20 | 9,04 pb/operación |
| Retorno medio VIX ≤ 20 | 1,70 pb/operación |
| Diferencia VIX > 20 − VIX ≤ 20 | 7,35 pb/operación |
| Mediana VIX > 20 | 6,86 pb/operación |
| t de la media VIX > 20 (sin bloques) | 4,25 t |
| Años sin comparación posible (un lado vacío) | 1 años |
| **Diferencia VIX > 20 − VIX ≤ 20 (OD+ · BtD · VIX>20 ×2)** | **7,35 pb/operación** |
| Intervalo bootstrap 95 % | [3,60; 11,38] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones conservan la dependencia de corto plazo y los regímenes de VIX. El intervalo **no incluye cero**.

## Robustez

- Positivo en **10 de 11 años**.
- Quitando un año cada vez: entre **6,74 y 8,89 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 847,50 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 13,47 | -1,44 | 6,37 | 11,92 | 32,90 | 10,38 | 12,39 | 1,42 | 13,47 | 13,09 | 6,97 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET, lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0.
- **Salida:** Vender al precio de las 03:30 ET.
- **Tamaño:** 1 unidad del índice; 2 unidades si el VIX al cierre de la sesión previa es > 20. Referencia al 100 % del capital (×2 = 200 %) aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa y unidad: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 1246 |
| PnL neto | 1.255,25 USD |
| Resultado medio por operación | 1,01 USD |
| Tasa de acierto | 52,01 % |
| Rentabilidad sobre 10.000 USD | 12,55 % |
| Máximo drawdown (tamaño del plan) | 1,20 % |
| Sharpe | 0,94 |
| Costes | 407,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **7,02 %** |
| Pico → valle | 2010-06-27 → 2011-03-10 |
| Recuperación | 2011-08-09 |
| Sesiones bajo el agua | 348 |
| Rentabilidad total | 81,76 % |
| Rentabilidad anual | 4,39 % |
| Sharpe | 0,95 |

## Sensibilidad del tamaño por serie (se informa, no se elige)

Al 100 % del capital por unidad de tamaño (multiplicador > 1 = apalancamiento). La diferencia es el retorno bruto medio por operación sobre el umbral menos el resto y no depende del multiplicador.

| Umbral | Ops sobre umbral | Diferencia (pb) | × | Rentabilidad total | Máx. drawdown | Sharpe |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 770 | 4,79 | 1,5 | 61,34 % | 5,65 % | 0,93 |
| 15 | 770 | 4,79 | 2,0 | 88,90 % | 7,48 % | 0,94 |
| 15 | 770 | 4,79 | 3,0 | 157,38 % | 11,06 % | 0,95 |
| 20 | 385 | 7,35 | 1,5 | 58,23 % | 5,42 % | 0,94 |
| 20 | 385 | 7,35 | 2,0 | 81,76 % | 7,02 % | 0,95 |
| 20 | 385 | 7,35 | 3,0 | 138,67 % | 10,16 % | 0,95 |
| 25 | 193 | 9,00 | 1,5 | 51,00 % | 4,03 % | 0,89 |
| 25 | 193 | 9,00 | 2,0 | 65,59 % | 4,49 % | 0,86 |
| 25 | 193 | 9,00 | 3,0 | 98,35 % | 6,30 % | 0,82 |
| 30 | 90 | 12,10 | 1,5 | 45,80 % | 3,90 % | 0,85 |
| 30 | 90 | 12,10 | 2,0 | 54,42 % | 4,22 % | 0,79 |
| 30 | 90 | 12,10 | 3,0 | 72,67 % | 6,30 % | 0,72 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Los de H007-IS-REAL-003.
- VIX: cierre diario de la sesión previa (16:15 ET), conocido antes de la entrada.
- Al 100 % con ×2 la exposición es del 200 % del capital (apalancamiento).
- Umbral y multiplicador elegidos tras ver el IS en el dashboard: sesgo de selección; la sensibilidad lo acota, no lo elimina.
- Las noches con VIX > 20 se concentran en pocos regímenes (2010-2012, 2015, 2018, 2020): pocas unidades independientes.
- Los de H007-IS-REAL-003.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario si el VIX se mantiene; OOS sigue bloqueado.
