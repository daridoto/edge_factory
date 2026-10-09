# H-001 · ¿Rinde más QQQ de apertura a cierre en el último día bursátil del mes que en las demás sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-IS-REAL-010-qqq-ultimo-dia-intradia.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (último día · Open-Close): -12,94 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · QQQ 1d · experimento H001-IS-REAL-010 · variante **QQQ · último día · Open-Close**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones último día · Open-Close | 135 sesiones |
| Sesiones resto | 2.698 sesiones |
| Retorno medio último día · Open-Close | -9,68 pb/día |
| Retorno medio resto | 3,26 pb/día |
| **Diferencia ventana − resto (último día · Open-Close)** | **-12,94 pb/día** |
| Intervalo bootstrap 95 % | [-26,96; 1,17] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). Evento mensual: bloques circulares de 3 meses; 5000 réplicas, semilla fija del laboratorio. El intervalo **incluye cero**.

## Robustez

- Positivo en **4 de 12 años**.
- Quitando un año cada vez: entre **-16,30 y -8,46 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -1.788,24 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -119,12 | -58,86 | 7,98 | -3,18 | 3,64 | -8,95 | -51,61 | -10,06 | -8,63 | 12,74 | -20,31 | 21,56 |

## Simulación de la operativa

- **Entrada:** Comprar al Open del último día bursátil de cada mes completo IS.
- **Salida:** Vender al Close de esa misma sesión; sin posición nocturna.
- **Tamaño:** 99,9 % de equity por operación, acciones fraccionarias; margen restante para costes, sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado (C1–C3), Open negociado reconstruido con el factor Close/Unadjusted Close del día.

| Resultado | Valor |
|---|---:|
| Operaciones | 135 |
| PnL neto | -1.523,26 USD |
| Resultado medio por operación | -11,28 USD |
| Tasa de acierto | 40,74 % |
| Rentabilidad sobre 10.000 USD | -15,23 % |
| Máximo drawdown (tamaño del plan) | 19,53 % |
| Sharpe | -0,48 |
| Costes | 264,98 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **19,53 %** |
| Pico → valle | 2009-10-29 → 2020-01-31 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 2812 |
| Rentabilidad total | -15,23 % |
| Rentabilidad anual | -1,46 % |
| Sharpe | -0,48 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Solo IS según proteccion.py; se excluye septiembre de 2009 por incompleto.
- Último día identificado por calendario observado (C5); una operación por mes.
- Evidencia bruta Open-Close comparada con Open-Close del resto, incluidos los tres primeros días del mes.
- Open y Close ajustados con el mismo factor diario; no se cobra el gap nocturno ni dividendos por tenencia nocturna.
- Ejecución idealizada en Open y Close; efectivo sin remunerar, sin stops ni filtros de volumen.
- Selección exploratoria tras estudiar previamente TOM: el intervalo no corrige esa exploración.
- Precio de apertura/cierre del proveedor, no garantía de ejecución en subasta; costes simplificados sin impacto.
- Con OHLC diario no se mide el drawdown intradía; drawdown de la curva a cierre.
- C5 presupone conocidos los cierres no programados; no es una simulación exacta del calendario disponible en tiempo real.
- No establece causalidad ni autoriza OOS; tamaño elegido para lectura sobre capital, no optimizado.

## Siguiente comprobación (propuesta, sin ejecutar)

Revisar con el usuario el resultado antes de proponer o ejecutar otra variante.
