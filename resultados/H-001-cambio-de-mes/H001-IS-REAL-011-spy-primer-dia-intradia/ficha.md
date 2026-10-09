# H-001 · ¿Rinde más SPY de apertura a cierre en el primer día bursátil del mes que en las demás sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-IS-REAL-011-spy-primer-dia-intradia.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (primer día · Open-Close): -0,67 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · SPY 1d · experimento H001-IS-REAL-011 · variante **SPY · primer día · Open-Close**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones primer día · Open-Close | 135 sesiones |
| Sesiones resto | 2.698 sesiones |
| Retorno medio primer día · Open-Close | 1,34 pb/día |
| Retorno medio resto | 2,01 pb/día |
| **Diferencia ventana − resto (primer día · Open-Close)** | **-0,67 pb/día** |
| Intervalo bootstrap 95 % | [-14,72; 13,04] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). Evento mensual: bloques circulares de 3 meses; 5000 réplicas, semilla fija del laboratorio. El intervalo **incluye cero**.

## Robustez

- Positivo en **7 de 12 años**.
- Quitando un año cada vez: entre **-4,26 y 5,14 pb/día**.
- **Cambia de signo al excluir 2011, 2014, 2019.**
- PnL de la simulación con costes ×2: -155,98 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 14,11 | 33,85 | -60,20 | -5,87 | 6,83 | -32,05 | 14,72 | 24,50 | 0,47 | -2,26 | -27,15 | 36,13 |

## Simulación de la operativa

- **Entrada:** Comprar al Open del primer día bursátil de cada mes completo IS.
- **Salida:** Vender al Close de esa misma sesión; sin posición nocturna.
- **Tamaño:** 99,9 % de equity por operación, acciones fraccionarias; margen restante para costes, sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado (C1–C3), Open negociado reconstruido con el factor Close/Unadjusted Close del día.

| Resultado | Valor |
|---|---:|
| Operaciones | 135 |
| PnL neto | -9,20 USD |
| Resultado medio por operación | -0,07 USD |
| Tasa de acierto | 49,63 % |
| Rentabilidad sobre 10.000 USD | -0,09 % |
| Máximo drawdown (tamaño del plan) | 11,07 % |
| Sharpe | 0,01 |
| Costes | 146,78 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **11,07 %** |
| Pico → valle | 2011-02-28 → 2015-01-02 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 2478 |
| Rentabilidad total | -0,09 % |
| Rentabilidad anual | -0,01 % |
| Sharpe | 0,01 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Solo IS según proteccion.py; se excluye septiembre de 2009 por incompleto.
- Primer día identificado por calendario observado (C5); una operación por mes.
- Evidencia bruta Open-Close comparada con Open-Close del resto, incluidos los días segundo y tercero y el último del mes.
- Open y Close ajustados con el mismo factor diario; no se cobra el gap nocturno ni dividendos por tenencia nocturna.
- Ejecución idealizada en Open y Close; efectivo sin remunerar, sin stops ni filtros de volumen.
- Selección exploratoria tras estudiar previamente TOM: el intervalo no corrige esa exploración.
- Precio de apertura/cierre del proveedor, no garantía de ejecución en subasta; costes simplificados sin impacto.
- Con OHLC diario no se mide el drawdown intradía; drawdown de la curva a cierre.
- C5 presupone conocidos los cierres no programados; no es una simulación exacta del calendario disponible en tiempo real.
- No establece causalidad ni autoriza OOS; tamaño elegido para lectura sobre capital, no optimizado.

## Siguiente comprobación (propuesta, sin ejecutar)

Revisar con el usuario el resultado antes de proponer o ejecutar otra variante.
