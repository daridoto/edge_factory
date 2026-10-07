# H-018 · ¿Rinde más SPY en la sesión previa a un festivo que en el resto de sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-018.md) → [plan](../../../experimentos/H-018-vispera-festivo/H018-IS-REAL-001-spy.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (víspera): 3,42 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-29 → 2020-12-31 · SPY 1d · experimento H018-IS-REAL-001 · variante **SPY · víspera**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones víspera | 89 sesiones |
| Sesiones resto | 2.746 sesiones |
| Retorno medio víspera | 9,13 pb/día |
| Retorno medio resto | 5,71 pb/día |
| **Diferencia ventana − resto (víspera)** | **3,42 pb/día** |
| Intervalo bootstrap 95 % | [-9,03; 15,77] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). Cada festivo cae una vez al año; bloques de 12 meses conservan un año completo de festivos. El intervalo **incluye cero**.

| Desglose | accion_gracias | ano_nuevo | independencia | memorial | navidad | presidentes | resto | trabajo | viernes_santo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 7,44 | -8,95 | 31,05 | -4,83 | -9,58 | 43,03 | 5,71 | -23,56 | 38,68 |

## Robustez

- Positivo en **6 de 12 años**.
- Quitando un año cada vez: entre **0,50 y 6,74 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 14,91 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -13,56 | 14,66 | -24,82 | 27,17 | -1,83 | 9,35 | -30,10 | 33,05 | -17,13 | -7,79 | 26,76 | 17,91 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la sesión anterior a la víspera.
- **Salida:** Vender al cierre de la víspera.
- **Tamaño:** 1 acción por víspera; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 89 |
| PnL neto | 16,69 USD |
| Resultado medio por operación | 0,19 USD |
| Tasa de acierto | 58,43 % |
| Rentabilidad sobre 10.000 USD | 0,17 % |
| Máximo drawdown (tamaño del plan) | 0,07 % |
| Sharpe | 0,36 |
| Costes | 1,78 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **4,74 %** |
| Pico → valle | 2011-08-31 → 2011-12-22 |
| Recuperación | 2014-07-03 |
| Sesiones bajo el agua | 713 |
| Rentabilidad total | 7,13 % |
| Rentabilidad anual | 0,61 % |
| Sharpe | 0,29 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Víspera = última sesión antes de un cierre observado de NYSE por uno de los 8 festivos (reglas en festivos.py).
- Año Nuevo en sábado (2011) no es cierre: ese año no hay víspera de Año Nuevo.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- Unas 89 vísperas en la IS (10-12 por festivo): el intervalo será ancho y el desglose por festivo, ruidoso.
- Solapa con el cambio de mes (H-001) en Labor Day, Navidad y Año Nuevo.
- El intervalo no corrige la exploración previa de esta hipótesis en la literatura.

## Siguiente comprobación (propuesta, sin ejecutar)

Según el resultado: mirar el desglose por festivo y el solapamiento con TOM, en IS.
