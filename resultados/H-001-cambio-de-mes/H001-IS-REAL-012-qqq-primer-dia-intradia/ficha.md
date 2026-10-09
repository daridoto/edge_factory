# H-001 · ¿Rinde más QQQ de apertura a cierre en el primer día bursátil del mes que en las demás sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-001.md) → [plan](../../../experimentos/H-001-cambio-de-mes/H001-IS-REAL-012-qqq-primer-dia-intradia.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (primer día · Open-Close): 0,07 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-10-01 → 2020-12-31 · QQQ 1d · experimento H001-IS-REAL-012 · variante **QQQ · primer día · Open-Close**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones primer día · Open-Close | 135 sesiones |
| Sesiones resto | 2.698 sesiones |
| Retorno medio primer día · Open-Close | 2,71 pb/día |
| Retorno medio resto | 2,64 pb/día |
| **Diferencia ventana − resto (primer día · Open-Close)** | **0,07 pb/día** |
| Intervalo bootstrap 95 % | [-16,67; 17,04] pb/día |

Bootstrap por bloques circulares (bloque = 3 × mes, 5.000 réplicas, semilla 7301). Evento mensual: bloques circulares de 3 meses; 5000 réplicas, semilla fija del laboratorio. El intervalo **incluye cero**.

## Robustez

- Positivo en **6 de 12 años**.
- Quitando un año cada vez: entre **-4,60 y 4,88 pb/día**.
- **Cambia de signo al excluir 2010, 2013, 2015, 2016, 2018, 2020.**
- PnL de la simulación con costes ×2: -289,97 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -72,76 | 24,78 | -49,17 | -5,21 | 5,26 | -22,94 | 12,07 | 34,40 | -11,96 | 20,95 | -37,07 | 47,96 |

## Simulación de la operativa

- **Entrada:** Comprar al Open del primer día bursátil de cada mes completo IS.
- **Salida:** Vender al Close de esa misma sesión; sin posición nocturna.
- **Tamaño:** 99,9 % de equity por operación, acciones fraccionarias; margen restante para costes, sin apalancamiento.
- **Costes:** 0,01 USD por acción y lado (C1–C3), Open negociado reconstruido con el factor Close/Unadjusted Close del día.

| Resultado | Valor |
|---|---:|
| Operaciones | 135 |
| PnL neto | 0,86 USD |
| Resultado medio por operación | 0,01 USD |
| Tasa de acierto | 53,33 % |
| Rentabilidad sobre 10.000 USD | 0,01 % |
| Máximo drawdown (tamaño del plan) | 10,52 % |
| Sharpe | 0,02 |
| Costes | 290,83 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,52 %** |
| Pico → valle | 2011-02-28 → 2015-01-02 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 2478 |
| Rentabilidad total | 0,01 % |
| Rentabilidad anual | 0,00 % |
| Sharpe | 0,02 |

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
