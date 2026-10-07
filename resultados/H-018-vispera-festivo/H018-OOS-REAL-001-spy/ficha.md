# H-018 · ¿Rinde más SPY en la sesión previa a un festivo que en el resto de sesiones?

**OOS de H018-IS-REAL-001 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-018.md) → [plan](../../../experimentos/H-018-vispera-festivo/H018-OOS-REAL-001-spy.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (víspera): 16,66 pb/día. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2021-01-04 → 2026-05-28 · SPY 1d · experimento H018-OOS-REAL-001 · variante **SPY · víspera**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones víspera | 42 sesiones |
| Sesiones resto | 1.314 sesiones |
| Retorno medio víspera | 22,42 pb/día |
| Retorno medio resto | 5,76 pb/día |
| **Diferencia ventana − resto (víspera)** | **16,66 pb/día** |
| Intervalo bootstrap 95 % | [4,37; 29,30] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). Cada festivo cae una vez al año; bloques de 12 meses conservan un año completo de festivos. El intervalo **no incluye cero**.

| Desglose | accion_gracias | ano_nuevo | independencia | memorial | navidad | presidentes | resto | trabajo | viernes_santo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 33,41 | -41,44 | 63,43 | 71,68 | 57,23 | -13,93 | 5,76 | -10,68 | 7,31 |

## Robustez

- Positivo en **5 de 6 años**.
- Quitando un año cada vez: entre **12,29 y 22,49 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 41,39 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/día | 39,04 | 26,51 | 16,31 | 16,26 | -8,18 | 8,04 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la sesión anterior a la víspera.
- **Salida:** Vender al cierre de la víspera.
- **Tamaño:** 1 acción por víspera; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 42 |
| PnL neto | 42,23 USD |
| Resultado medio por operación | 1,01 USD |
| Tasa de acierto | 64,29 % |
| Rentabilidad sobre 10.000 USD | 0,42 % |
| Máximo drawdown (tamaño del plan) | 0,08 % |
| Sharpe | 0,83 |
| Costes | 0,84 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **1,89 %** |
| Pico → valle | 2022-02-16 → 2022-05-26 |
| Recuperación | 2022-05-27 |
| Sesiones bajo el agua | 70 |
| Rentabilidad total | 9,56 % |
| Rentabilidad anual | 1,71 % |
| Sharpe | 0,86 |

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
