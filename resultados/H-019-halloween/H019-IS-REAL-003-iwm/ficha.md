# H-019 · ¿Rinde más IWM de noviembre a abril que de mayo a octubre?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-019.md) → [plan](../../../experimentos/H-019-halloween/H019-IS-REAL-003-iwm.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Diferencia ventana − resto (Nov-Abr): 6,63 pb/día. El intervalo incluye cero: en IS no se distingue de no tener efecto.

**Muestra:** 2009-09-29 → 2020-12-31 · IWM 1d · experimento H019-IS-REAL-003 · variante **IWM · Nov-Abr**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones Nov-Abr | 1.400 sesiones |
| Sesiones resto | 1.435 sesiones |
| Retorno medio Nov-Abr | 9,00 pb/día |
| Retorno medio resto | 2,37 pb/día |
| **Diferencia ventana − resto (Nov-Abr)** | **6,63 pb/día** |
| Intervalo bootstrap 95 % | [-1,57; 15,55] pb/día |

Bootstrap por bloques circulares (bloque = 12 × mes, 5.000 réplicas, semilla 7301). La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia. El intervalo **incluye cero**.

## Robustez

- Positivo en **8 de 12 años**.
- Quitando un año cada vez: entre **5,32 y 8,15 pb/día**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 115,72 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/día | 60,05 | 20,03 | 18,16 | 10,79 | 1,83 | -3,35 | 2,89 | 6,46 | -1,12 | -6,69 | 19,94 | -8,87 |

## Simulación de la operativa

- **Entrada:** Comprar al cierre de la última sesión de octubre.
- **Salida:** Vender al cierre de la última sesión de abril (o de la muestra).
- **Tamaño:** 1 acción por semestre; referencia al 100 % del capital aparte.
- **Costes:** 0,01 USD por acción y lado; sin comisión adicional ni impacto.

| Resultado | Valor |
|---|---:|
| Operaciones | 12 |
| PnL neto | 115,97 USD |
| Resultado medio por operación | 9,66 USD |
| Tasa de acierto | 83,33 % |
| Rentabilidad sobre 10.000 USD | 1,16 % |
| Máximo drawdown (tamaño del plan) | 0,69 % |
| Sharpe | 0,56 |
| Costes | 0,24 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **41,04 %** |
| Pico → valle | 2020-01-16 → 2020-03-23 |
| Recuperación | 2020-12-23 |
| Sesiones bajo el agua | 237 |
| Rentabilidad total | 204,92 % |
| Rentabilidad anual | 10,42 % |
| Sharpe | 0,71 |

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
