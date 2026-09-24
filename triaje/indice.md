# Triaje de hipótesis por datos

Actualizado: 2026-09-22 · compatibles: 11 · proxy: 5 · bloqueadas: 20

| id | enunciado (corto, ≤ 12 palabras) | familia | dataset | veredicto | motivos |
|---|---|---|---|---|---|
| [[H-001]] | Cambio de mes (días -1 a +3) rinde más que el resto | estacionalidad | SPY 1d | compatible | — |
| [[H-007]] | ES: la hora 2:00-3:00 ET es la de mayor rentabilidad media | estacionalidad | ES 15min | compatible | C-ROLL |
| [[H-010]] | Primera media hora predice con el mismo signo la última | momentum | ES 15min | compatible | C-EQUIV, C-ROLL |
| [[H-011]] | Penúltima media hora predice la última, complementaria a la primera | momentum | ES 15min | compatible | C-EQUIV, C-ROLL |
| [[H-013]] | Momentum intradía más fuerte en días de alto volumen | momentum | ES 15min | compatible | C-EQUIV, C-ROLL |
| [[H-017]] | Anomalía de viernes/jueves solo dentro de la ventana de cambio de mes | estacionalidad | SPY 1d | compatible | — |
| [[H-019]] | Noviembre-abril rinde más que mayo-octubre (efecto Halloween) | estacionalidad | SPY 1d | compatible | — |
| [[H-029]] | Momentum intradía más fuerte cuando la primera media hora es positiva | momentum | ES 15min | compatible | C-ROLL |
| [[H-030]] | Momentum intradía más fuerte con spread Corwin-Schultz alto | momentum | ES 15min | compatible | C-ROLL |
| [[H-031]] | El retorno overnight predice la última media hora | momentum | ES 15min | compatible | C-ROLL |
| [[H-032]] | Momentum intradía más fuerte los lunes | momentum | ES 15min | compatible | C-EQUIV, C-ROLL |
| [[H-002]] | Efecto cambio de mes mayor en pequeña que en gran capitalización | estacionalidad | IWM + SPY 1d | proxy | P-OTRO |
| [[H-008]] | Desequilibrio vendedor al cierre predice subida del ES a 2:00-4:00 | reversion | ES 15min | proxy | P-CAMPO, C-NOVALID, C-ROLL |
| [[H-009]] | Reversión nocturna tras desequilibrio vendedor mayor con VIX alto | reversion | ES 15min + VIX 1d | proxy | P-CAMPO, P-OTRO, C-NOVALID |
| [[H-012]] | Momentum intradía más fuerte con alta volatilidad en la primera media hora | momentum | ES 15min | proxy | P-FREQ, C-EQUIV, C-ROLL |
| [[H-018]] | La sesión previa a un festivo rinde más que el resto | estacionalidad | SPY 1d | proxy | C-FESTIVOS, C-EQUIV |
| [[H-003]] | Deriva positiva del S&P 500 en las 24 h previas al FOMC | evento | SPY 1d | bloqueada | F-FOMC, C-COBERTURA |
| [[H-004]] | Deriva pre-FOMC mayor si la media de las 8 anteriores es alta | evento | SPY 1d | bloqueada | F-FOMC, C-EQUIV |
| [[H-005]] | Deriva pre-FOMC mayor con VIX retardado alto | evento | SPY + VIX 1d | bloqueada | F-FOMC, C-EQUIV |
| [[H-006]] | Deriva pre-FOMC mayor con pendiente baja de la curva del Tesoro | evento | SPY 1d | bloqueada | F-FOMC, F-EXTERNO, C-EQUIV |
| [[H-014]] | Momentum intradía más fuerte en días de noticias macro | momentum | ES 15min + macro | bloqueada | F-MACRO, C-EQUIV, C-ROLL |
| [[H-015]] | Efecto cambio de mes mayor en REITs que en el índice general | estacionalidad | — | bloqueada | F-MERCADO |
| [[H-016]] | Efecto cambio de mes mayor en acciones tipo lotería | estacionalidad | — | bloqueada | F-UNIVERSO |
| [[H-020]] | BIST 100: miércoles y viernes rinden menos que lunes | estacionalidad | — | bloqueada | F-MERCADO |
| [[H-021]] | Prima en días de grandes anuncios macro; nula el resto | evento | SPY 1d + macro | bloqueada | F-FOMC, F-MACRO, C-COBERTURA, C-EQUIV |
| [[H-022]] | Deriva del día previo al FOMC solo con sentimiento alto | evento | SPY 1d | bloqueada | F-FOMC, P-OTRO, C-NOVALID, C-EQUIV |
| [[H-023]] | Deriva pre-FOMC concentrada cuando el VIX cae en las 24 h previas | evento | ES 15min | bloqueada | F-FOMC, F-EXTERNO |
| [[H-024]] | Desde 2011, deriva pre-FOMC solo con rueda de prensa | evento | SPY 1d | bloqueada | F-FOMC, C-EQUIV |
| [[H-025]] | Desde 2011, overnight de ~20 pb la noche previa al FOMC | evento | SPY 1d | bloqueada | F-FOMC |
| [[H-026]] | Semanas pares del ciclo FOMC rinden más que las impares | evento | SPY 1d | bloqueada | F-FOMC, C-COBERTURA |
| [[H-027]] | Tras semana muy negativa, rebote mayor en semana par del ciclo FOMC | reversion | SPY 1d | bloqueada | F-FOMC, C-COBERTURA, C-EQUIV |
| [[H-028]] | Acciones tipo lotería rinden más en la ventana pre-FOMC | evento | — | bloqueada | F-FOMC, F-UNIVERSO |
| [[H-033]] | Mala noticia de NFP en buenos tiempos: la bolsa sube | evento | SPY 1d + macro | bloqueada | F-EXTERNO, C-EQUIV |
| [[H-034]] | Bolsa cae ~1 % por cada 20 pb de sorpresa de tipos FOMC | evento | ES 15min | bloqueada | F-FOMC, F-EXTERNO, P-FREQ, C-EQUIV |
| [[H-035]] | Picos de volatilidad de 5 min tras comunicado y rueda de prensa FOMC | sin_encaje | ES 15min | bloqueada | F-FREQ, F-FOMC |
| [[H-036]] | Acciones lotería infrarreaccionan a resultados publicados en el cambio de mes | evento | — | bloqueada | F-EXTERNO, F-UNIVERSO |

## Qué desbloquearía más
| dato que falta | hipótesis bloqueadas solo por él |
|---|---|
| calendario FOMC (fechas de anuncios programados) | H-003, H-004, H-005, H-022, H-025, H-026, H-027 |
| calendario FOMC con rueda de prensa | H-024 |
| REITs | H-015 |
| universo de acciones individuales | H-016 |
| BIST 100 | H-020 |

## Detalle

### H-001 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índice amplio de renta variable EE. UU. | OK (SPY) | "en un índice amplio de renta variable (o un ETF que lo replique)" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario" |
| campo | OHLCV | OK | "rendimiento close-to-close medio" |
| calendario | días hábiles del mes | OK (sesiones SPY) | "el último día hábil (Día -1) y los tres primeros del mes siguiente" |

### H-007 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | ES | OK (ES) | "en el E-mini S&P 500 (contrato más negociado)" |
| frecuencia | 1h (o 5min) | OK (C9: ES 15min → 1h) | "Con barras horarias (o de 5 minutos) del ES en sesión de 24 h" |
| campo | OHLCV | OK | "retorno medio por hora del día y su t" |

### H-010 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía (SPY) | OK (C8: ES) | "en SPY (y en otros ETFs líquidos de índices)" |
| frecuencia | 30min | OK (C9: ES 15min) | "Con barras de 30 minutos" |
| campo | OHLCV | OK | "r1 = close(10:00)/close_prev(16:00) − 1" |

### H-011 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía (SPY) | OK (C8: ES) | "en SPY el retorno 15:30-16:00 ET" |
| frecuencia | 30min | OK (C9: ES 15min) | "Con barras de 30 minutos" |
| campo | OHLCV | OK | "r12 = close(15:30)/close(15:00) − 1" |

### H-013 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía (SPY) | OK (C8: ES) | "Volumen de la primera media hora (barra 9:30-10:00) de SPY" |
| frecuencia | 30min | OK (C9: ES 15min) | datos: "OHLCV intradía (30 min o menos)" |
| campo | OHLCV (volumen) | OK | "Clasificar los días en terciles de volumen" |

### H-017 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índice amplio | OK (SPY) | "en un índice amplio la rentabilidad media de los viernes (y jueves)" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario" |
| campo | OHLCV | OK | "regresión de la rentabilidad close-to-close" |

### H-019 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índice amplio | OK (SPY) | "en un índice amplio la rentabilidad close-to-close media" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario" |
| campo | OHLCV | OK | "dummy = 1 de noviembre a abril" |

### H-029 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (ES) | "en SPY (o un futuro del S&P 500)" |
| frecuencia | 30min | OK (C9: ES 15min) | "Con barras de 30 minutos" |
| campo | OHLCV | OK | "separar los días por el signo de r1" |

### H-030 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | no especificado | OK (ES, como en H-010) | "Con OHLCV intradía" |
| frecuencia | intradía sin frecuencia (→ 15min) | OK (ES 15min) | "Con OHLCV intradía: estimar el spread de Corwin-Schultz" |
| campo | máximos y mínimos (estimador Corwin-Schultz) | OK (OHLCV) | datos: "el estimador de Corwin-Schultz solo usa máximos y mínimos" |

Notas: el texto no nombra instrumento (la evidencia es solo de Bitcoin, que no está en el Inventario: "Solo documentado en Bitcoin; aplicarlo a índices es una extrapolación"). Se asigna ES por continuidad con H-010. El "spread" es un estimador calculado con OHLC, no el campo bid/ask, por eso no se marca como F-CAMPO ni P-CAMPO.

### H-031 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (ES) | "en SPY (o un futuro de índice)" |
| frecuencia | intradía sin frecuencia (→ 15min); barra de 30 min | OK (C9: ES 15min) | "Con OHLCV intradía: r_ON = open(t)/close(t-1) − 1" |
| campo | OHLCV | OK | "r_FH = close(apertura + 30 min)/open(t) − 1" |

### H-032 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (C8: ES) | "en el S&P 500 la pendiente y el R²" |
| frecuencia | 30min | OK (C9: ES 15min) | "Con barras de 30 minutos" |
| campo | OHLCV | OK | "r1 desde el cierre del viernes" |

### H-002 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | deciles de capitalización CRSP (pequeña y gran) | PROXY (IWM y SPY) | Test mínimo: "un ETF de pequeña capitalización y otro de gran capitalización (proxy de los deciles CRSP)" |
| frecuencia | 1d | OK (1d) | "Con OHLCV diario" |
| campo | OHLCV | OK | "diferencia entre el rendimiento medio de la ventana TOM" |

### H-008 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | ES | OK (ES) | "en el E-mini S&P 500 un volumen firmado relativo (RSV)" |
| frecuencia | 15min (ventanas 15:15-16:15 y horas nocturnas) | OK (ES 15min) | "retorno de la barra 15:15-16:15" |
| campo | volumen firmado | PROXY (OHLCV) | Test mínimo: "Proxy OHLCV intradía (no validado por el paper): signo o magnitud del retorno de la barra 15:15-16:15; posición del cierre en el rango (C−L)/(H−L) ponderada por volumen" |

### H-009 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | ES | OK (ES) | "en el E-mini S&P 500 la respuesta del retorno de 2:00-3:00 ET" |
| frecuencia | 1h (2:00-3:00) y 15:15-16:15 | OK (C9: ES 15min) | "Regresar el retorno de 2:00-3:00 ET sobre RSV de cierre" |
| campo | volumen firmado | PROXY (OHLCV) | Test mínimo: "sustituir RSV por uno de los proxies OHLCV de H-008" |
| externo | VIX a las 16:15 (intradía) | PROXY (VIX 1d) | Test mínimo: "el VIX de las 16:15 por el cierre diario del VIX" |

### H-012 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía (SPY) | OK (C8: ES) | "en SPY la pendiente y el R²" |
| frecuencia | 30min (r1, r13) | OK (C9: ES 15min) | "estimar la regresión de r13 sobre r1 en cada tercil" |
| frecuencia | 1min (volatilidad realizada) | PROXY (barra de 30 min) | Test mínimo: "proxy con barras de 30 min: \|r1\| o el rango (high − low)/open de la barra 9:30-10:00" |
| campo | OHLCV | OK | "rango (high − low)/open" |

### H-018 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 (y en índices de ADR)" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario y el calendario de festivos" |
| campo | OHLCV | OK | "rentabilidad close-to-close media de la sesión anterior" |
| calendario | festivos NYSE | PROXY (huecos de sesión del SPY) | regla fija (datos.md); también en la hipótesis: "aproximarlo por huecos de sesiones mezcla festivos con otros cierres" |

### H-003 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (SPY) | "en el S&P 500 (SPY o E-mini como sustituto)" |
| frecuencia | 1d (variante diaria) | OK (SPY 1d) | "Diario: rendimiento close(D-1) → close(D)" |
| campo | OHLCV | OK | "close(D-1) → close(D)" |
| calendario | FOMC (reuniones programadas) | FALTA | "en los días de anuncio FOMC programado" |
| periodo | 1980-1993, 1994-marzo 2011, abril 2011 en adelante | OK parcial (desde 2006) | "submuestras 1980-1993, 1994-marzo 2011 y abril 2011 en adelante" |

### H-004 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento de la ventana pre-FOMC" |
| frecuencia | 1d | OK (SPY 1d) | "close-to-close del día del anuncio con OHLCV diario" |
| campo | OHLCV | OK | "Calcular MA8 con las 8 reuniones previas" |
| calendario | FOMC | FALTA | datos: "+ calendario FOMC externo" |

### H-005 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento de la ventana pre-FOMC" |
| frecuencia | 1d | OK (SPY 1d) | "close-to-close del día del anuncio" |
| externo | VIX diario | OK (VIX 1d) | "sobre el nivel del VIX al cierre anterior a la ventana" |
| calendario | FOMC | FALTA | datos: "serie diaria del VIX y calendario FOMC" |

### H-006 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento de la ventana pre-FOMC" |
| frecuencia | 1d | OK (SPY 1d) | "close-to-close del día del anuncio" |
| externo | curva del Tesoro | FALTA | "sobre la pendiente de la curva del Tesoro (diferencia entre un tipo largo y uno corto)" |
| calendario | FOMC | FALTA | datos: "rendimientos de bonos del Tesoro ... y calendario FOMC" |

### H-014 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía (SPY) | OK (C8: ES) | "en SPY el R² y la pendiente" |
| frecuencia | 30min | OK (C9: ES 15min) | datos: "OHLCV intradía (30 min o menos)" |
| calendario | CPI | OK (fichero macro) | enunciado: "(MCSI, PIB, IPC, actas del FOMC)" |
| calendario | MCSI | FALTA | "días de publicación de MCSI, PIB, IPC y actas del FOMC" |
| calendario | PIB | FALTA | ídem |
| calendario | actas FOMC | FALTA | ídem |

### H-015 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | REITs | FALTA | "Con OHLCV diario de un ETF o índice de REITs" |
| instrumento | índice amplio del mismo país | OK (SPY) | "y de un índice amplio del mismo país" |
| frecuencia | 1d | OK (1d) | "Con OHLCV diario" |

### H-016 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales (universo amplio) | FALTA | "Con OHLCV diario de un universo amplio de acciones y de un índice" |
| frecuencia | 1d | OK (1d) | ídem |

Notas: la ficha W2532958920 menciona como proxy con índices "comparar ... un índice de acciones pequeñas, baratas y volátiles con un índice de grandes compañías". Ese índice (pequeñas + baratas + volátiles) no está en el Inventario; IWM solo recoge tamaño y la propia hipótesis advierte que "un proxy con un solo rasgo (p. ej. solo precio bajo o solo pequeña capitalización) no reproduce la señal". Si el usuario acepta IWM frente a SPY como proxy, pasaría a `proxy` (P-OTRO, C-NOVALID) y quedaría muy cerca de H-002.

### H-020 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | BIST 100 | FALTA | "Con OHLCV diario del BIST 100" |
| frecuencia | 1d | OK (1d) | ídem |

### H-021 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento close-to-close medio" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario" |
| calendario | NFP | OK (fichero macro) | "días con anuncio de NFP/empleo, IPP, FOMC, PIB o ISM" |
| calendario | PPI | OK (fichero macro) | ídem |
| calendario | FOMC | FALTA | ídem |
| calendario | PIB | FALTA | ídem |
| calendario | ISM | FALTA | ídem |
| periodo | 1961-2014 y 1997-2014 | OK parcial (SPY desde 2006, macro 2009-2020) | "Submuestras 1961-2014 (solo los anuncios disponibles) y 1997-2014" |

### H-022 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento en exceso del día anterior" |
| frecuencia | 1d | OK (SPY 1d) | "Rendimiento close-to-close del día anterior a cada anuncio (OHLCV diario + calendario FOMC)" |
| externo | sentimiento (CSI o BWI) | PROXY (precios del SPY) | Test mínimo: "Proxy no validado por el paper: estado de sentimiento construido con precios" |
| calendario | FOMC | FALTA | ídem |

### H-023 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (ES) | "Con barras intradía del S&P 500 (o E-mini)" |
| frecuencia | intradía (14:00-14:00) | OK (ES 15min) | "rendimiento 14:00-14:00" |
| externo | VIX intradía | FALTA | "y del VIX: ... cambio del VIX en la misma ventana" |
| calendario | FOMC | FALTA | "para cada anuncio programado" |

### H-024 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 desde abril de 2011" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario, variante close(D-1) → open(D) y close(D-1) → close(D)" |
| calendario | FOMC con rueda de prensa | FALTA | "marcar los que tienen rueda de prensa (calendario de la Fed)" |
| periodo | desde abril de 2011 | OK | "Para los anuncios programados desde abril de 2011" |

### H-025 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (SPY) | "en el S&P 500 (SPY o E-mini)" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario y el calendario FOMC" |
| campo | OHLCV (open y close) | OK | "close de D-1 a open de D" |
| calendario | FOMC | FALTA | ídem |
| periodo | desde marzo de 2011 | OK | "en días de anuncio desde marzo de 2011" |

### H-026 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 o ETF amplio | OK (SPY) | "en el S&P 500 (o un ETF amplio)" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario y el calendario de reuniones programadas" |
| calendario | FOMC | FALTA | ídem |
| periodo | 1982-1993, 1994-2016, 2017 en adelante | OK parcial (desde 2006) | "Submuestras 1982-1993, 1994-2016 y 2017 en adelante" |

### H-027 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento del día t" |
| frecuencia | 1d | OK (SPY 1d) | "Con OHLCV diario: rentabilidad acumulada de t-5 a t-1" |
| calendario | FOMC | FALTA | datos: "OHLCV diario + calendario FOMC" |
| periodo | 1994-2016 y posteriores | OK parcial (desde 2006) | "Submuestras 1994-2016 y posteriores" |

### H-028 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales (universo amplio) | FALTA | "Con OHLCV diario de un universo amplio de acciones" |
| frecuencia | 1d | OK (1d) | "ventana close(t-1) → close(t)" |
| calendario | FOMC | FALTA | "en días FOMC frente a días sin anuncio" |

Notas: la ficha W4385460904 apunta un proxy a nivel índice ("hipótesis del usuario, no del paper"): "comparar el drift pre-FOMC de un índice de alta beta o small cap frente a uno de baja volatilidad". El índice de baja volatilidad no está en el Inventario, así que no se toma como proxy disponible.

### H-033 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "en el S&P 500 el rendimiento close-to-close del día del informe de empleo" |
| frecuencia | 1d | OK (SPY 1d) | ídem |
| calendario | NFP | OK (fichero macro) | "Calendario y sorpresas de NFP" |
| externo | sorpresas NFP | FALTA | "(dato publicado menos mediana de la encuesta previa)" |
| externo | otro: estado de la economía ("buenos tiempos") | FALTA | "hay que fijar una definición ex ante, p. ej. la del paper original de Boyd et al." |

Notas: la hipótesis no dice con qué datos se definen los "buenos tiempos"; se marca FALTA porque ninguna fuente nombra un sustituto del Inventario. Por eso H-033 no aparece en "Qué desbloquearía más" bajo sorpresas.

### H-034 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (C8: ES) | "en el S&P 500 la rentabilidad entre 10 minutos antes y 20 minutos después" |
| frecuencia | 5min | PROXY (30min desde ES 15min) | datos: "OHLCV intradía (5-30 min)" |
| externo | sorpresas de tipos | FALTA | "sobre una medida de sorpresa de tipos en la misma ventana (series tipo Kuttner o mps)" |
| calendario | FOMC con hora | FALTA | "Con barras intradía de 5 minutos y la hora de cada anuncio" |

Notas: la ventana [-10 min, +20 min] no se puede cortar exactamente con barras de 15 min; la aproximación de 30 min se toma porque `datos` nombra el rango "5-30 min".

### H-035 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 intradía | OK (ES) | "en el S&P 500 (o E-mini)" |
| frecuencia | 5min | FALTA | "Con barras de 5 minutos" |
| calendario | FOMC con hora (comunicado y rueda de prensa) | FALTA | datos: "calendario FOMC con hora del comunicado y de la rueda de prensa" |

Notas: familia `sin_encaje` porque la hipótesis predice volatilidad, no dirección ni momento de una posición ("No predice dirección, solo volatilidad").

### H-036 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales | FALTA | "OHLCV diario de las acciones (y de un índice para rentabilidades anormales)" |
| externo | resultados empresariales (fechas y sorpresas) | FALTA | "Con fechas y sorpresas de resultados" |
| frecuencia | 1d | OK (1d) | ídem |
