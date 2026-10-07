# H-019 · ¿Rinde más SPY de noviembre a abril que de mayo a octubre?

**OOS de H019-IS-REAL-001 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-019.md) → [plan](../../../experimentos/H-019-halloween/H019-OOS-REAL-001-spy.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (Nov-Abr): -2,08 pb/día. El intervalo incluye cero: en OOS no se distingue de no tener efecto.

**Muestra:** 2021-01-04 → 2026-05-28 · SPY 1d · experimento H019-OOS-REAL-001 · variante **SPY · Nov-Abr**. OOS autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones Nov-Abr | 699 sesiones |
| Sesiones resto | 657 sesiones |
| Retorno medio Nov-Abr | 5,26 pb/día |
| Retorno medio resto | 7,35 pb/día |
| **Diferencia ventana − resto (Nov-Abr)** | **-2,08 pb/día** |
| Intervalo bootstrap 95 % | [-11,14; 6,76] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia. El intervalo **incluye cero**.

## Robustez

- Positivo en **2 de 6 años**.
- Quitando un año cada vez: entre **-6,34 y 1,94 pb/día**.
- **Cambia de signo al excluir 2025.**
- PnL de la simulación con costes ×2: 155,86 USD.

| Año | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|
| pb/día | 4,15 | -7,50 | 17,17 | -2,91 | -19,71 | -18,78 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la última sesión de octubre.
- **Salida:** Vender al cierre de la última sesión de abril (o de la muestra).
- **Tamaño:** 1 acción por semestre; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 6 |
| PnL neto | 155,98 USD |
| Resultado medio por operación | 26,00 USD |
| Tasa de acierto | 66,67 % |
| Rentabilidad sobre 10.000 USD | 1,56 % |
| Máximo drawdown (tamaño del plan) | 1,13 % |
| Sharpe | 0,45 |
| Costes | 0,12 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **18,74 %** |
| Pico → valle | 2025-02-19 → 2025-04-08 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 319 |
| Rentabilidad total | 39,91 % |
| Rentabilidad anual | 6,44 % |
| Sharpe | 0,55 |

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
