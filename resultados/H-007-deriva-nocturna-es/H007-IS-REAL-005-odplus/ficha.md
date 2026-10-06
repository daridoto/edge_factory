# H-007 · ¿Rinde el ES entre las 01:30 y las 03:30 ET?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-es/H007-IS-REAL-005-odplus.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+): 2,62 pb/operación (2903 sesiones); mediana operadas 1,30 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · ES 15min · experimento H007-IS-REAL-005 · variante **OD+**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 2.903 sesiones |
| Sesiones descartadas por el filtro | 0 sesiones |
| Retorno medio operadas | 2,62 pb/operación |
| Mediana operadas | 1,30 pb/operación |
| t de la media operadas (sin bloques) | 5,59 t |
| **Retorno bruto medio por operación (OD+)** | **2,62 pb/operación** |
| Intervalo bootstrap 95 % | [1,60; 3,70] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **12 de 12 años**.
- Quitando un año cada vez: entre **2,20 y 2,84 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: -9,25 USD.

| Año | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 7,13 | 2,31 | 3,71 | 1,74 | 2,26 | 0,99 | 3,87 | 2,76 | 0,76 | 1,88 | 0,36 | 6,95 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 2903 |
| PnL neto | 716,50 USD |
| Resultado medio por operación | 0,25 USD |
| Tasa de acierto | 47,95 % |
| Rentabilidad sobre 10.000 USD | 7,16 % |
| Máximo drawdown (tamaño del plan) | 1,82 % |
| Sharpe | 0,66 |
| Costes | 725,75 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **8,23 %** |
| Pico → valle | 2010-06-23 → 2011-03-14 |
| Recuperación | 2012-01-16 |
| Sesiones bajo el agua | 484 |
| Rentabilidad total | 42,33 % |
| Rentabilidad anual | 2,57 % |
| Sharpe | 0,72 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria, no se opera esa noche.
- OD+ es la ventana del paper (Tabla IX), vista ya en el dashboard (H007-IS-REAL-002).
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6).
- Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).

## Siguiente comprobación (propuesta, sin ejecutar)

OOS de OD+ sola (H007-OOS-REAL-003), autorizado por el usuario el 2026-10-06.
