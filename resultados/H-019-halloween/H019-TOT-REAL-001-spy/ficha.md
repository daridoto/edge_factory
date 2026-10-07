# H-019 · ¿Rinde más SPY de noviembre a abril que de mayo a octubre?

**Total de H019-IS-REAL-001 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-019.md) → [plan](../../../experimentos/H-019-halloween/H019-TOT-REAL-001-spy.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (Nov-Abr): 2,34 pb/día. El intervalo incluye cero: en Total no se distingue de no tener efecto.

**Muestra:** 2009-09-29 → 2026-05-28 · SPY 1d · experimento H019-TOT-REAL-001 · variante **SPY · Nov-Abr**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones Nov-Abr | 2.099 sesiones |
| Sesiones resto | 2.092 sesiones |
| Retorno medio Nov-Abr | 7,13 pb/día |
| Retorno medio resto | 4,79 pb/día |
| **Diferencia ventana − resto (Nov-Abr)** | **2,34 pb/día** |
| Intervalo bootstrap 95 % | [-2,13; 6,91] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia. El intervalo **incluye cero**.

## Robustez

- Positivo en **10 de 18 años**.
- Quitando un año cada vez: entre **1,42 y 3,75 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 349,56 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 29,25 | 9,52 | 12,29 | 8,61 | 5,86 | -2,06 | -0,41 | 2,96 | 2,24 | -8,32 | 15,48 | -3,56 | 4,15 | -7,50 | 17,17 | -2,91 | -19,71 | -18,78 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la última sesión de octubre.
- **Salida:** Vender al cierre de la última sesión de abril (o de la muestra).
- **Tamaño:** 1 acción por semestre; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 17 |
| PnL neto | 349,90 USD |
| Resultado medio por operación | 20,58 USD |
| Tasa de acierto | 82,35 % |
| Rentabilidad sobre 10.000 USD | 3,50 % |
| Máximo drawdown (tamaño del plan) | 1,12 % |
| Sharpe | 0,48 |
| Costes | 0,34 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **33,69 %** |
| Pico → valle | 2020-02-19 → 2020-03-23 |
| Recuperación | 2021-01-07 |
| Sesiones bajo el agua | 224 |
| Rentabilidad total | 288,16 % |
| Rentabilidad anual | 8,50 % |
| Sharpe | 0,70 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Invierno = sesiones de noviembre a abril; verano = mayo a octubre.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- El invierno 2020-21 queda cortado el 31-12-2020: cuenta en el estadístico y la operación se cierra ahí.
- Solo 11 inviernos completos en la IS: el intervalo será ancho.
- El intervalo no corrige la exploración previa de esta hipótesis en la literatura.
- Sin comisiones adicionales, impacto ni dividendos fuera de posición.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario qué hacer con H-019 a la vista del OOS.
