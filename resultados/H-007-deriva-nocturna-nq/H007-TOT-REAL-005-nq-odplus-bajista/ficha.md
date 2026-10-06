# H-007 · ¿Rinde el NQ entre las 01:30 y las 03:30 ET cuando está por debajo de su media de 200 sesiones?

**Total de H007-IS-REAL-008 · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-TOT-REAL-005-nq-odplus-bajista.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · bajista): 5,01 pb/operación (646 sesiones frente a 3275); mediana operadas 0,89 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2026-05-28 · NQ 15min · experimento H007-TOT-REAL-005 · variante **NQ · OD+ bajista**. Total autorizada; misma especificación que la base.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 646 sesiones |
| Sesiones descartadas por el filtro | 3.275 sesiones |
| Retorno medio operadas | 5,01 pb/operación |
| Retorno medio descartadas por el filtro | 1,20 pb/operación |
| Diferencia operadas − descartadas por el filtro | 3,81 pb/operación |
| Mediana operadas | 0,89 pb/operación |
| t de la media operadas (sin bloques) | 2,69 t |
| Años sin comparación posible (un lado vacío) | 4 años |
| **Retorno bruto medio por operación (OD+ · bajista)** | **5,01 pb/operación** |
| Intervalo bootstrap 95 % | [1,07; 9,47] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **9 de 13 años**.
- Quitando un año cada vez: entre **3,03 y 8,51 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 2.197,75 USD.

| Año | 2010 | 2011 | 2012 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 | 2022 | 2023 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 0,36 | 9,46 | -0,28 | 18,35 | 10,79 | 3,48 | 5,16 | -0,85 | 63,97 | -1,26 | -3,27 | 15,39 | 1,51 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el precio de las 16:15 de la sesión previa está en o por debajo de su media de 200 sesiones.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 646 |
| PnL neto | 2.359,25 USD |
| Resultado medio por operación | 3,65 USD |
| Tasa de acierto | 50,00 % |
| Rentabilidad sobre 10.000 USD | 23,59 % |
| Máximo drawdown (tamaño del plan) | 11,78 % |
| Sharpe | 0,44 |
| Costes | 161,50 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **10,73 %** |
| Pico → valle | 2022-04-13 → 2025-04-07 |
| Recuperación | no recupera en la muestra |
| Sesiones bajo el agua | 1284 |
| Rentabilidad total | 33,18 % |
| Rentabilidad anual | 1,40 % |
| Sharpe | 0,54 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Parámetros elegidos tras ver el IS (y conociendo el OOS del ES): el OOS mide si sobreviven a esa elección.
- Toda la muestra posterior a la IS se usa aquí: no queda holdout del NQ.

## Siguiente comprobación (propuesta, sin ejecutar)

Decidir con el usuario a la vista del OOS; no queda holdout del NQ.
