# Estado

**Última actualización:** 2026-09-25. Normas y funcionamiento en [CLAUDE.md](CLAUDE.md); aquí solo lo que cambia.

## Siguiente paso
1. **H-001 · QQQ a OOS** (candidato elegido: efecto +4,30 pb/día, positivo sin cualquier año; IC IS aún cruza 0). Antes de calcular: el usuario fija las fechas OOS y autoriza explícitamente su uso para QQQ.
2. Comprobaciones de H-007 en IS (día de la semana, semanas de desfase horario).
3. Aparcado por decisión del usuario: métricas al 100 % del capital (DD de referencia de la estrategia) en `resumen.json` o como experimentos aparte.

## Dónde estamos
| pieza | estado |
|---|---|
| Triaje | 36 hipótesis: 11 compatibles, 5 proxy, 20 bloqueadas. Los datos son los que hay: las bloqueadas quedan fuera, no esperan datos |
| Recetas | H-001, H-007, H-008 y H-010 `lista`; H-025 `bloqueada` (FOMC) |
| Experimentos | H-001 en IS sobre SPY, QQQ, IWM y DIA: 1 acción (H001-IS-REAL-001 a 004) y 30 % de la equity (005 a 008, las que muestra el dashboard). H007-IS-REAL-001 sigue con 1 punto. Cifras en [resultados/indice.csv](resultados/indice.csv) |
| Catálogo del ejecutor | datasets `SPY 1d`, `QQQ 1d`, `IWM 1d`, `DIA 1d` y `ES 15min`; periodos `1d` y `1h`; ventanas `dias_de_mes` y `hora`; estadísticos `media_ventana` y `media_vs_resto` |
| Agente `investigador` | sin estrenar: H-001 y H-007 se hicieron en línea |

## Pendiente (hoja de ruta)
- Más pruebas estadísticas según la pregunta (sensibilidad de bloque y parámetros, contrastes con benchmark).
- Simulación de trayectorias y cartera: drawdown, rachas, varias estrategias juntas.
- Encaje con cuenta personal y fondeo (límites diarios, drawdown), separado de la evidencia.
- Criterios de aprobación y muestra OOS: los decide el usuario.

## Problemas conocidos
- Rolls del ES: la regla C6 solo está verificada desde 2022.
- H-010 (primera media hora → última) necesitará un estadístico nuevo en el catálogo (predicción de signo o regresión).

## Registro
- **2026-09-22:** agentes `triaje` y `estratega`, catálogo de datos, convenciones, triaje de las 36 y 5 recetas. Motor inicial y primera prueba real de H-001. Commit `262b62a`.
- **2026-09-24:** fuera el etiquetado manual. `laboratorio/` a pydantic: la salida pasa de 5 ficheros a `resumen.json` + 2 CSV + ficha, con `indice.csv`. Ejecutor único que lee el TOML del plan, sin `.py` por hipótesis. H-001 migrada con cifras idénticas y H-007 ejecutada en IS. Manual unificado en CLAUDE.md; fuera `docs/`. Recetas en formato corto (de ~800 a ~380 líneas) y `estratega` adaptado.
- **2026-09-24 (tarde):** nace `edge_factory` a partir de sentinel2 (commit `7346b6e`) y del dashboard de front-testing/project1, que pasa a `dashboard/`. Los repos originales se conservan intactos como respaldo.
- **2026-09-24 (noche):** retirado del dashboard el OOS sintético de H-001 (`demo-oos.js`, `oosDemo`); solo se muestra IS real.
- **2026-09-24 (noche):** H-001 replicada en IS sobre QQQ, IWM y DIA (misma especificación); datasets añadidos al catálogo con test de filtrado IS; registradas en el dashboard como `H-001-QQQ/IWM/DIA`.
- **2026-09-24 (noche):** sizing opcional por fracción de equity (`fraccion` en `[operativa]`, C10), con test; el modo 1 unidad reproduce los resultados previos. H-001 ejecutada con 30 % en los cuatro ETF (005-008). Dashboard: comparativa por hipótesis (`#H-001`) y fila agrupada en la portada.
- **2026-09-24 (cierre):** paleta por instrumento en la comparativa. QQQ elegido como candidato a OOS de H-001 (pendiente de muestra y autorización). Transiciones de entrada y salida entre vistas del dashboard. Primer commit de `edge_factory`.
- **2026-09-25:** dashboard: filtro de curvas y resaltado cruzado en la comparativa; arreglado el tooltip de la equity (fecha numérica en eje temporal), que bloqueaba ECharts; nota «antes de costes» en los gráficos por año. Comparativa y trampas de ECharts documentadas en la skill `nueva-hipotesis`, `dashboard/CLAUDE.md` y `DISENO.md`.
