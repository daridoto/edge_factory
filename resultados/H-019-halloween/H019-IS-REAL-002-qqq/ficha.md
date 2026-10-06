# H-019 · ¿Rinde más QQQ de noviembre a abril que de mayo a octubre?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-019.md) → [plan](../../../experimentos/H-019-halloween/H019-IS-REAL-002-qqq.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (Nov-Abr): 2,52 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-29 → 2020-12-31 · QQQ 1d · experimento H019-IS-REAL-002 · variante **QQQ · Nov-Abr**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones Nov-Abr | 1.400 sesiones |
| Sesiones resto | 1.435 sesiones |
| Retorno medio Nov-Abr | 9,50 pb/día |
| Retorno medio resto | 6,98 pb/día |
| **Diferencia ventana − resto (Nov-Abr)** | **2,52 pb/día** |
| Intervalo bootstrap 95 % | [-3,39; 8,96] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia. El intervalo **incluye cero**.

## Robustez

- Positivo en **7 de 12 años**.
- Quitando un año cada vez: entre **0,87 y 3,84 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 153,27 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 40,91 | 3,89 | 4,38 | 16,98 | -0,60 | -10,05 | -2,01 | -11,02 | 4,31 | -8,50 | 19,63 | 0,93 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la última sesión de octubre.
- **Salida:** Vender al cierre de la última sesión de abril (o de la muestra).
- **Tamaño:** 1 acción por semestre; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 12 |
| PnL neto | 153,51 USD |
| Resultado medio por operación | 12,79 USD |
| Tasa de acierto | 91,67 % |
| Rentabilidad sobre 10.000 USD | 1,54 % |
| Máximo drawdown (tamaño del plan) | 0,67 % |
| Sharpe | 0,61 |
| Costes | 0,24 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **28,54 %** |
| Pico → valle | 2020-02-19 → 2020-03-16 |
| Recuperación | 2020-11-05 |
| Sesiones bajo el agua | 182 |
| Rentabilidad total | 235,42 % |
| Rentabilidad anual | 11,36 % |
| Sharpe | 0,82 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Invierno = sesiones de noviembre a abril; verano = mayo a octubre.
- Retornos close-to-close ajustados por dividendos, antes de costes.
- El invierno 2020-21 queda cortado el 31-12-2020: cuenta en el estadístico y la operación se cierra ahí.
- Solo 11 inviernos completos en la IS: el intervalo será ancho.
- El intervalo no corrige la exploración previa de esta hipótesis en la literatura.
- Sin comisiones adicionales, impacto ni dividendos fuera de posición.

## Siguiente comprobación (propuesta, sin ejecutar)

Comparar los cuatro ETF con el usuario. OOS bloqueado.
