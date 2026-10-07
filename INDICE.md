# Índice de hipótesis y experimentos

Generado por `python -m laboratorio indice` desde `resultados/`; no se edita a mano. Cada hipótesis tiene su carpeta en `experimentos/` (planes) y otra igual en `resultados/` (salida). Estadístico y su IC tal como los da el lab; ROI y drawdown, con la operativa al 100 % del capital.

| hipótesis | qué es | variantes | experimentos |
|---|---|---:|---:|
| [H-001](#h-001) | Cambio de mes (−1 a +3): rendimiento diario medio mayor que el resto del mes | 9 | 10 |
| [H-007](#h-007) | Deriva nocturna del ES en la hora 2:00-3:00 ET | 8 | 18 |
| [H-010](#h-010) | Primera media hora (cierre anterior → 10:00 ET) predice la última (15:30-16:00 ET) | 4 | 4 |
| [H-018](#h-018) | La víspera de festivo rinde más que el resto | 2 | 4 |
| [H-019](#h-019) | Noviembre-abril rinde más que mayo-octubre | 4 | 6 |
| [H-PROPIA-001](#h-propia-001) | RAY largo 28 días cuando el volumen de Raydium dobla su nivel normal | 1 | 1 |

<a id="h-001"></a>

## H-001 · Cambio de mes (−1 a +3): rendimiento diario medio mayor que el resto del mes

[receta](estrategias/H-001.md) · [notas](conocimiento/H-001.md) · planes: `experimentos/H-001-cambio-de-mes/` · resultados: `resultados/H-001-cambio-de-mes/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **SPY · 1 acción** | IS | [H001-IS-REAL-001](resultados/H-001-cambio-de-mes/H001-IS-REAL-001-spy-1-accion/ficha.md) | 2009–2020 | Diferencia ventana − resto | 2,37 pb/día | [-6,27; 11,50] · cruza 0 | 4/12 | 46,8 % | −13,9 % |
| **QQQ · 1 acción** | IS | [H001-IS-REAL-002](resultados/H-001-cambio-de-mes/H001-IS-REAL-002-qqq-1-accion/ficha.md) | 2009–2020 | Diferencia ventana − resto | 4,30 pb/día | [-4,83; 13,86] · cruza 0 | 6/12 | 79,5 % | −11,0 % |
| **IWM · 1 acción** | IS | [H001-IS-REAL-003](resultados/H-001-cambio-de-mes/H001-IS-REAL-003-iwm-1-accion/ficha.md) | 2009–2020 | Diferencia ventana − resto | -3,55 pb/día | [-15,78; 8,59] · cruza 0 | 3/12 | 10,3 % | −24,8 % |
| **DIA · 1 acción** | IS | [H001-IS-REAL-004](resultados/H-001-cambio-de-mes/H001-IS-REAL-004-dia-1-accion/ficha.md) | 2009–2020 | Diferencia ventana − resto | 0,05 pb/día | [-8,55; 9,13] · cruza 0 | 4/12 | 30,3 % | −12,8 % |
| **SPY · 30 %** | IS | [H001-IS-REAL-005](resultados/H-001-cambio-de-mes/H001-IS-REAL-005-spy-30pct/ficha.md) | 2009–2020 | Diferencia ventana − resto | 2,37 pb/día | [-6,27; 11,50] · cruza 0 | 4/12 | 46,8 % | −13,9 % |
| **QQQ · 30 %** | IS | [H001-IS-REAL-006](resultados/H-001-cambio-de-mes/H001-IS-REAL-006-qqq-30pct/ficha.md) | 2009–2020 | Diferencia ventana − resto | 4,30 pb/día | [-4,83; 13,86] · cruza 0 | 6/12 | 79,5 % | −11,0 % |
| **IWM · 30 %** | IS | [H001-IS-REAL-007](resultados/H-001-cambio-de-mes/H001-IS-REAL-007-iwm-30pct/ficha.md) | 2009–2020 | Diferencia ventana − resto | -3,55 pb/día | [-15,78; 8,59] · cruza 0 | 3/12 | 10,3 % | −24,8 % |
| **DIA · 30 %** | IS | [H001-IS-REAL-008](resultados/H-001-cambio-de-mes/H001-IS-REAL-008-dia-30pct/ficha.md) | 2009–2020 | Diferencia ventana − resto | 0,05 pb/día | [-8,55; 9,13] · cruza 0 | 4/12 | 30,3 % | −12,8 % |
| **QQQ · TOM** | OOS | [H001-OOS-REAL-001](resultados/H-001-cambio-de-mes/H001-OOS-REAL-001-qqq-tom/ficha.md) | 2021–2026 | Diferencia ventana − resto | -4,16 pb/día | [-20,70; 11,94] · cruza 0 | 4/6 | 7,5 % | −14,5 % |
|  | Total | [H001-TOT-REAL-001](resultados/H-001-cambio-de-mes/H001-TOT-REAL-001-qqq-tom/ficha.md) | 2009–2026 | Diferencia ventana − resto | 1,58 pb/día | [-6,73; 10,13] · cruza 0 | 10/18 | 89,6 % | −14,5 % |

<a id="h-007"></a>

## H-007 · Deriva nocturna del ES en la hora 2:00-3:00 ET

[receta](estrategias/H-007.md) · [notas](conocimiento/H-007.md) · planes: `experimentos/H-007-deriva-nocturna-es/` · resultados: `resultados/H-007-deriva-nocturna-es/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **OD** | IS | [H007-IS-REAL-001](resultados/H-007-deriva-nocturna-es/H007-IS-REAL-001-od/ficha.md) | 2009–2020 | Retorno medio en la ventana | 1,63 pb/hora | [1,01; 2,29] | 11/12 | 7,4 % | −6,5 % |
| **OD · tabla de variantes** | IS | [H007-IS-REAL-002](resultados/H-007-deriva-nocturna-es/H007-IS-REAL-002-od-tabla-variantes/ficha.md) | 2009–2020 | Retorno medio en la ventana | 1,63 pb/hora | [1,01; 2,29] | 11/12 | 7,4 % | −6,5 % |
| **OD+ BtD** | IS | [H007-IS-REAL-003](resultados/H-007-deriva-nocturna-es/H007-IS-REAL-003-odplus-btd/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 3,97 pb/operación | [2,42; 5,50] | 12/12 | 37,5 % | −3,9 % |
|  | OOS | [H007-OOS-REAL-001](resultados/H-007-deriva-nocturna-es/H007-OOS-REAL-001-odplus-btd/ficha.md) | 2021–2026 | Retorno bruto medio por operación | 0,35 pb/operación | [-1,44; 2,25] · cruza 0 | 4/6 | -1,3 % | −10,4 % |
|  | Total | [H007-TOT-REAL-001](resultados/H-007-deriva-nocturna-es/H007-TOT-REAL-001-odplus-btd/ficha.md) | 2009–2026 | Retorno bruto medio por operación | 2,71 pb/operación | [1,53; 3,94] | 16/18 | 35,7 % | −10,4 % |
| **OD+ BtD VIX** | IS | [H007-IS-REAL-004](resultados/H-007-deriva-nocturna-es/H007-IS-REAL-004-odplus-btd-vix/ficha.md) | 2009–2020 | Diferencia VIX > 20 − VIX ≤ 20 | 7,35 pb/operación | [3,60; 11,38] | 10/11 | 81,8 % | −7,0 % |
|  | OOS | [H007-OOS-REAL-002](resultados/H-007-deriva-nocturna-es/H007-OOS-REAL-002-odplus-btd-vix/ficha.md) | 2021–2026 | Diferencia VIX > 20 − VIX ≤ 20 | 0,62 pb/operación | [-4,40; 5,24] · cruza 0 | 4/6 | -1,4 % | −19,4 % |
|  | Total | [H007-TOT-REAL-002](resultados/H-007-deriva-nocturna-es/H007-TOT-REAL-002-odplus-btd-vix/ficha.md) | 2009–2026 | Diferencia VIX > 20 − VIX ≤ 20 | 4,54 pb/operación | [1,58; 7,63] | 14/17 | 79,2 % | −19,4 % |
| **OD+** | IS | [H007-IS-REAL-005](resultados/H-007-deriva-nocturna-es/H007-IS-REAL-005-odplus/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 2,62 pb/operación | [1,60; 3,70] | 12/12 | 42,3 % | −8,2 % |
|  | OOS | [H007-OOS-REAL-003](resultados/H-007-deriva-nocturna-es/H007-OOS-REAL-003-odplus/ficha.md) | 2021–2026 | Retorno bruto medio por operación | 0,03 pb/operación | [-1,08; 1,13] · cruza 0 | 3/6 | -6,8 % | −15,6 % |
|  | Total | [H007-TOT-REAL-003](resultados/H-007-deriva-nocturna-es/H007-TOT-REAL-003-odplus/ficha.md) | 2009–2026 | Retorno bruto medio por operación | 1,78 pb/operación | [0,99; 2,65] | 15/18 | 32,6 % | −15,6 % |
| **NQ · OD+ BtD** | IS | [H007-IS-REAL-006](resultados/H-007-deriva-nocturna-nq/H007-IS-REAL-006-nq-odplus-btd/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 3,66 pb/operación | [2,17; 5,25] | 12/12 | 44,7 % | −3,5 % |
|  | OOS | [H007-OOS-REAL-004](resultados/H-007-deriva-nocturna-nq/H007-OOS-REAL-004-nq-odplus-btd/ficha.md) | 2021–2026 | Retorno bruto medio por operación | 0,99 pb/operación | [-1,30; 3,29] · cruza 0 | 5/6 | 5,2 % | −10,0 % |
|  | Total | [H007-TOT-REAL-004](resultados/H-007-deriva-nocturna-nq/H007-TOT-REAL-004-nq-odplus-btd/ficha.md) | 2009–2026 | Retorno bruto medio por operación | 2,76 pb/operación | [1,48; 4,03] | 17/18 | 52,3 % | −10,0 % |
| **NQ · OD+ BtD × tendencia** | IS | [H007-IS-REAL-007](resultados/H-007-deriva-nocturna-nq/H007-IS-REAL-007-nq-btd-tendencia/ficha.md) | 2009–2020 | Diferencia alcista − bajista | -5,04 pb/operación | [-13,79; 2,45] · cruza 0 | 4/9 | 44,7 % | −3,5 % |
| **NQ · OD+ bajista** | IS | [H007-IS-REAL-008](resultados/H-007-deriva-nocturna-nq/H007-IS-REAL-008-nq-odplus-bajista/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 8,49 pb/operación | [2,46; 16,05] | 7/9 | 29,8 % | −2,9 % |
|  | OOS | [H007-OOS-REAL-005](resultados/H-007-deriva-nocturna-nq/H007-OOS-REAL-005-nq-odplus-bajista/ficha.md) | 2021–2026 | Retorno bruto medio por operación | 1,13 pb/operación | [-3,28; 5,73] · cruza 0 | 2/4 | 2,6 % | −10,7 % |
|  | Total | [H007-TOT-REAL-005](resultados/H-007-deriva-nocturna-nq/H007-TOT-REAL-005-nq-odplus-bajista/ficha.md) | 2009–2026 | Retorno bruto medio por operación | 5,01 pb/operación | [1,07; 9,47] | 9/13 | 33,2 % | −10,7 % |

<a id="h-010"></a>

## H-010 · Primera media hora (cierre anterior → 10:00 ET) predice la última (15:30-16:00 ET)

[receta](estrategias/H-010.md) · [notas](conocimiento/H-010.md) · planes: `experimentos/H-010-momentum-intradia-es/` · resultados: `resultados/H-010-momentum-intradia-es/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **ES · r1 → r13** | IS | [H010-IS-REAL-001](resultados/H-010-momentum-intradia-es/H010-IS-REAL-001-r1-r13/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 0,28 pb/operación | [-0,87; 1,45] · cruza 0 | 8/12 | -26,3 % | −28,9 % |
| **ES · r1 apertura → r13** | IS | [H010-IS-REAL-002](resultados/H-010-momentum-intradia-es/H010-IS-REAL-002-r1-apertura/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 0,56 pb/operación | [-0,48; 1,67] · cruza 0 | 8/12 | -21,5 % | −31,2 % |
| **ES · r1 + r12 → r13** | IS | [H010-IS-REAL-003](resultados/H-010-momentum-intradia-es/H010-IS-REAL-003-r1-r12/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 0,46 pb/operación | [-1,25; 2,24] · cruza 0 | 6/12 | -11,1 % | −13,1 % |
| **ES · r1 apertura → r13 · VIX ≥ 20** | IS | [H010-IS-REAL-004](resultados/H-010-momentum-intradia-es/H010-IS-REAL-004-r1-apertura-vix/ficha.md) | 2009–2020 | Retorno bruto medio por operación | 2,40 pb/operación | [-0,86; 5,81] · cruza 0 | 9/11 | 5,4 % | −10,4 % |

<a id="h-018"></a>

## H-018 · La víspera de festivo rinde más que el resto

[receta](estrategias/H-018.md) · [notas](conocimiento/H-018.md) · planes: `experimentos/H-018-vispera-festivo/` · resultados: `resultados/H-018-vispera-festivo/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **SPY · víspera** | IS | [H018-IS-REAL-001](resultados/H-018-vispera-festivo/H018-IS-REAL-001-spy/ficha.md) | 2009–2020 | Diferencia ventana − resto | 3,42 pb/día | [-9,03; 15,77] · cruza 0 | 6/12 | 7,1 % | −4,7 % |
|  | OOS | [H018-OOS-REAL-001](resultados/H-018-vispera-festivo/H018-OOS-REAL-001-spy/ficha.md) | 2021–2026 | Diferencia ventana − resto | 16,66 pb/día | [4,37; 29,30] | 5/6 | 9,6 % | −1,9 % |
|  | Total | [H018-TOT-REAL-001](resultados/H-018-vispera-festivo/H018-TOT-REAL-001-spy/ficha.md) | 2009–2026 | Diferencia ventana − resto | 7,96 pb/día | [-1,75; 17,14] · cruza 0 | 11/18 | 18,0 % | −4,7 % |
| **ES · última hora de la víspera** | IS | [H018-IS-REAL-002](resultados/H-018-vispera-festivo/H018-IS-REAL-002-es-hora/ficha.md) | 2009–2020 | Diferencia ventana − resto | 1,57 pb/hora | [-4,21; 7,32] · cruza 0 | 7/12 | 0,6 % | −1,5 % |

<a id="h-019"></a>

## H-019 · Noviembre-abril rinde más que mayo-octubre

[receta](estrategias/H-019.md) · [notas](conocimiento/H-019.md) · planes: `experimentos/H-019-halloween/` · resultados: `resultados/H-019-halloween/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **SPY · Nov-Abr** | IS | [H019-IS-REAL-001](resultados/H-019-halloween/H019-IS-REAL-001-spy/ficha.md) | 2009–2020 | Diferencia ventana − resto | 4,45 pb/día | [-0,57; 9,81] · cruza 0 | 8/12 | 181,2 % | −33,7 % |
|  | OOS | [H019-OOS-REAL-001](resultados/H-019-halloween/H019-OOS-REAL-001-spy/ficha.md) | 2021–2026 | Diferencia ventana − resto | -2,08 pb/día | [-11,14; 6,76] · cruza 0 | 2/6 | 39,9 % | −18,7 % |
|  | Total | [H019-TOT-REAL-001](resultados/H-019-halloween/H019-TOT-REAL-001-spy/ficha.md) | 2009–2026 | Diferencia ventana − resto | 2,34 pb/día | [-2,13; 6,91] · cruza 0 | 10/18 | 288,2 % | −33,7 % |
| **QQQ · Nov-Abr** | IS | [H019-IS-REAL-002](resultados/H-019-halloween/H019-IS-REAL-002-qqq/ficha.md) | 2009–2020 | Diferencia ventana − resto | 2,52 pb/día | [-3,39; 8,96] · cruza 0 | 7/12 | 235,4 % | −28,5 % |
| **IWM · Nov-Abr** | IS | [H019-IS-REAL-003](resultados/H-019-halloween/H019-IS-REAL-003-iwm/ficha.md) | 2009–2020 | Diferencia ventana − resto | 6,63 pb/día | [-1,57; 15,55] · cruza 0 | 8/12 | 204,9 % | −41,0 % |
| **DIA · Nov-Abr** | IS | [H019-IS-REAL-004](resultados/H-019-halloween/H019-IS-REAL-004-dia/ficha.md) | 2009–2020 | Diferencia ventana − resto | 4,45 pb/día | [-0,66; 9,64] · cruza 0 | 8/12 | 168,7 % | −36,7 % |

<a id="h-propia-001"></a>

## H-PROPIA-001 · RAY largo 28 días cuando el volumen de Raydium dobla su nivel normal

[receta](estrategias/H-PROPIA-001.md) · [notas](conocimiento/H-PROPIA-001.md) · planes: `experimentos/H-PROPIA-001-ray-volumen/` · resultados: `resultados/H-PROPIA-001-ray-volumen/`

| variante | muestra | experimento | periodo | mide | valor | IC 95 % | años + | ROI 100 % | DD 100 % |
|---|---|---|---|---|---:|---|---:|---:|---:|
| **VOL×2** | IS | [HPROPIA001-IS-REAL-001](resultados/H-PROPIA-001-ray-volumen/HPROPIA001-IS-REAL-001-vol-x2/ficha.md) | 2022–2026 | Retorno neto medio por operación | 37,51 % / operación | [9,41; 68,22] | 3/5 | 3.664,8 % | −54,1 % |
