# H-018 · ¿Rinde más SPY en la sesión previa a un festivo que en el resto de sesiones?

**Total de H018-IS-REAL-001 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-018.md) → [plan](../../../experimentos/H-018-vispera-festivo/H018-TOT-REAL-001-spy.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (víspera): 7,96 pb/día. El intervalo incluye cero: en Total no se distingue de no tener efecto.

**Muestra:** 2009-09-29 → 2026-05-28 · SPY 1d · experimento H018-TOT-REAL-001 · variante **SPY · víspera**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones víspera | 132 sesiones |
| Sesiones resto | 4.059 sesiones |
| Retorno medio víspera | 13,68 pb/día |
| Retorno medio resto | 5,71 pb/día |
| **Diferencia ventana − resto (víspera)** | **7,96 pb/día** |
| Intervalo bootstrap 95 % | [-1,75; 17,14] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). Cada festivo cae una vez al año; bloques de 12 meses conservan un año completo de festivos. El intervalo **incluye cero**.

| Desglose | accion_gracias | ano_nuevo | independencia | memorial | navidad | presidentes | resto | trabajo | viernes_santo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 15,08 | -13,63 | 41,17 | 22,18 | 10,07 | 22,93 | 5,71 | -19,54 | 27,61 |

## Robustez

- Positivo en **11 de 18 años**.
- Quitando un año cada vez: entre **6,25 y 10,42 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 58,15 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | -13,56 | 14,66 | -24,82 | 27,17 | -1,83 | 9,35 | -30,10 | 33,05 | -17,13 | -7,79 | 26,76 | 21,15 | 39,04 | 26,51 | 16,31 | 16,26 | -8,18 | 8,04 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la sesión anterior a la víspera.
- **Salida:** Vender al cierre de la víspera.
- **Tamaño:** 1 acción por víspera; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 132 |
| PnL neto | 60,79 USD |
| Resultado medio por operación | 0,46 USD |
| Tasa de acierto | 60,61 % |
| Rentabilidad sobre 10.000 USD | 0,61 % |
| Máximo drawdown (tamaño del plan) | 0,08 % |
| Sharpe | 0,57 |
| Costes | 2,64 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **4,74 %** |
| Pico → valle | 2011-08-31 → 2011-12-22 |
| Recuperación | 2014-07-03 |
| Sesiones bajo el agua | 713 |
| Rentabilidad total | 17,95 % |
| Rentabilidad anual | 1,00 % |
| Sharpe | 0,48 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Víspera = última sesión antes de un cierre observado de NYSE por uno de los 8 festivos (reglas en festivos.py).
- Año Nuevo en sábado (2011) no es cierre: ese año no hay víspera de Año Nuevo.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- Unas 89 vísperas en la IS (10-12 por festivo): el intervalo será ancho y el desglose por festivo, ruidoso.
- Solapa con el cambio de mes (H-001) en Labor Day, Navidad y Año Nuevo.
- El intervalo no corrige la exploración previa de esta hipótesis en la literatura.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario qué hacer con H-018 a la vista del OOS.
