# H-007 · ¿Rinde el NQ entre las 01:30 y las 03:30 ET cuando está por debajo de su media de 200 sesiones?

**SOLO IS · EXPLORATORIA**

**Recorrido:** [receta](../../../estrategias/H-007.md) → [plan](../../../experimentos/H-007-deriva-nocturna-nq/H007-IS-REAL-008-nq-odplus-bajista.md) → esta ficha · datos: [resumen.json](resumen.json), [equity.csv](equity.csv), [operaciones.csv](operaciones.csv)

> Retorno bruto medio por operación (OD+ · bajista): 8,49 pb/operación (341 sesiones frente a 2245); mediana operadas 1,44 pb/operación. El intervalo no incluye cero bajo los supuestos del remuestreo; no prueba estabilidad futura.

**Muestra:** 2009-09-27 → 2020-12-31 · NQ 15min · experimento H007-IS-REAL-008 · variante **NQ · OD+ bajista**. OOS y holdout no utilizados.

## Evidencia

| | Valor |
|---|---:|
| Sesiones operadas | 341 sesiones |
| Sesiones descartadas por el filtro | 2.245 sesiones |
| Retorno medio operadas | 8,49 pb/operación |
| Retorno medio descartadas por el filtro | 1,57 pb/operación |
| Diferencia operadas − descartadas por el filtro | 6,92 pb/operación |
| Mediana operadas | 1,44 pb/operación |
| t de la media operadas (sin bloques) | 3,10 t |
| Años sin comparación posible (un lado vacío) | 2 años |
| **Retorno bruto medio por operación (OD+ · bajista)** | **8,49 pb/operación** |
| Intervalo bootstrap 95 % | [2,46; 16,05] pb/operación |

Bootstrap por bloques circulares (bloque = 5 × sesión, 5.000 réplicas, semilla 7301). Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo. El intervalo **no incluye cero**.

## Robustez

- Positivo en **7 de 9 años**.
- Quitando un año cada vez: entre **4,85 y 10,05 pb/operación**.
- No cambia de signo al excluir ningún año.
- PnL de la simulación con costes ×2: 1.363,00 USD.

| Año | 2010 | 2011 | 2012 | 2014 | 2015 | 2016 | 2018 | 2019 | 2020 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| pb/operación | 0,36 | 9,46 | -0,28 | 18,35 | 10,79 | 3,48 | 5,16 | -0,85 | 63,97 |

## Simulación de la operativa

- **Entrada:** Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el precio de las 16:15 de la sesión previa está en o por debajo de su media de 200 sesiones.
- **Salida:** Vender al precio de las 03:30 ET (cierre de la barra de 03:15).
- **Tamaño:** 1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte.
- **Costes:** 1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado.

| Resultado | Valor |
|---|---:|
| Operaciones | 341 |
| PnL neto | 1.448,25 USD |
| Resultado medio por operación | 4,25 USD |
| Tasa de acierto | 50,73 % |
| Rentabilidad sobre 10.000 USD | 14,48 % |
| Máximo drawdown (tamaño del plan) | 1,96 % |
| Sharpe | 0,72 |
| Costes | 85,25 USD |

**Referencia al 100 % del capital** (la misma operativa con el 99,9 % de la equity por unidad de tamaño; con multiplicador > 1 hay apalancamiento):

| Riesgo | Valor |
|---|---:|
| Máximo drawdown | **2,89 %** |
| Pico → valle | 2011-08-10 → 2011-09-13 |
| Recuperación | 2015-08-21 |
| Sesiones bajo el agua | 1252 |
| Rentabilidad total | 29,78 % |
| Rentabilidad anual | 1,89 % |
| Sharpe | 0,75 |

Métricas completas y sus definiciones: `metricas` en resumen.json y [esquema](../../../esquemas/resumen.schema.json).

## Supuestos y límites

- Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.
- Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.
- Si falta una barra necesaria (ventana o señal), no se opera esa noche.
- Regla sacada del IS del NQ (H007-IS-REAL-007): sesgo de selección declarado.
- Pocas noches bajistas (unas 340 en IS) y las primeras 200 sesiones sin tendencia quedan fuera.
- Conocemos el OOS del ES, que se mueve casi igual que el NQ: el OOS del NQ no es del todo a ciegas.
- La muestra empieza en 2009; el paper cubre 1998-2020.
- La regla de roll anterior a 2022 no está verificada (C6).
- Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).

## Siguiente comprobación (propuesta, sin ejecutar)

OOS 2021-2026 autorizado por el usuario el 2026-10-06 (H007-OOS-REAL-005).
