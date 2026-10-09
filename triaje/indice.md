# Triaje de hipótesis por datos

Actualizado: 2026-10-09 · compatibles: 19 · proxy: 6 · bloqueadas: 37

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
| [[H-037]] | Volatilidad condicional del S&P 500 mínima el miércoles, máxima el viernes | sin_encaje | SPY 1d | compatible | C-COBERTURA, C-EQUIV |
| [[H-038]] | S&P 500: miércoles rinde más y lunes menos | estacionalidad | SPY 1d | compatible | C-COBERTURA, C-EQUIV |
| [[H-051]] | Tras varianza alta, la rentabilidad por unidad de varianza baja | sin_encaje | SPY 1d | compatible | — |
| [[H-052]] | Exposición escalada por 1/varianza del mes previo mejora el Sharpe | sin_encaje | SPY 1d | compatible | — |
| [[H-073]] | Movimiento ≥ ±2 % hasta 14:15-14:45: el cierre sigue el signo | momentum | ES 15min | compatible | C-EQUIV, C-ROLL |
| [[H-055]] | Bitcoin: la rentabilidad semanal predice la siguiente con el mismo signo | momentum | BTCUSDT 1d | compatible | C-COBERTURA |
| [[H-041]] | Rentabilidad pasada alta de una divisa predice asimetría más negativa | sin_encaje | EURUSD + JPYUSD 1d | compatible | C-COBERTURA |
| [[H-058]] | BTC, XRP y ETH: los sábados rinden menos | estacionalidad | BTC + ETH + XRP 1d | compatible | C-COBERTURA |
| [[H-002]] | Efecto cambio de mes mayor en pequeña que en gran capitalización | estacionalidad | IWM + SPY 1d | proxy | P-OTRO |
| [[H-008]] | Desequilibrio vendedor al cierre predice subida del ES a 2:00-4:00 | reversion | ES 15min | proxy | P-CAMPO, C-NOVALID, C-ROLL |
| [[H-009]] | Reversión nocturna tras desequilibrio vendedor mayor con VIX alto | reversion | ES 15min + VIX 1d | proxy | P-CAMPO, P-OTRO, C-NOVALID |
| [[H-012]] | Momentum intradía más fuerte con alta volatilidad en la primera media hora | momentum | ES 15min | proxy | P-FREQ, C-EQUIV, C-ROLL |
| [[H-018]] | La sesión previa a un festivo rinde más que el resto | estacionalidad | SPY 1d | proxy | C-FESTIVOS, C-EQUIV |
| [[H-056]] | Atención alta (Google, tuits) predice rentabilidad cripto mayor | sin_encaje | BTCUSDT 1d | proxy | P-OTRO, C-NOVALID |
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
| [[H-039]] | Carry de divisas: largo tipo alto, corto tipo bajo rinde positivo | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-040]] | Diferencial de tipos alto predice asimetría más negativa de la divisa | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-042]] | Semanas con VIX al alza: el carry de divisas pierde | sin_encaje | EURUSD + JPYUSD + VIX 1d | bloqueada | F-EXTERNO |
| [[H-043]] | Divisas con tipos parecidos tienen mayor correlación diaria | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-044]] | Risk-reversals de divisas crecen con el tipo de interés | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-045]] | Acciones con MAX alto del mes previo rinden menos | reversion | — | bloqueada | F-UNIVERSO |
| [[H-046]] | Controlando por MAX, volatilidad idiosincrática alta rinde más | sin_encaje | — | bloqueada | F-UNIVERSO |
| [[H-047]] | Reversión transversal a 1-5 días en acciones tiene rentabilidad positiva | reversion | — | bloqueada | F-UNIVERSO |
| [[H-048]] | Reversión a corto plazo rinde más con VIX retardado alto | reversion | VIX 1d | bloqueada | F-UNIVERSO |
| [[H-049]] | Reversión mensual concentrada en perdedores de los tres meses previos | reversion | — | bloqueada | F-UNIVERSO |
| [[H-050]] | Reversión mensual mayor cuando salen instituciones activas | reversion | — | bloqueada | F-UNIVERSO, F-EXTERNO |
| [[H-053]] | Factores escalados por 1/varianza dan alfa, mayor en momentum | sin_encaje | — | bloqueada | F-EXTERNO |
| [[H-054]] | Cartera multifactor condicionada a volatilidad del mercado supera a la incondicional | sin_encaje | — | bloqueada | F-UNIVERSO, F-EXTERNO |
| [[H-057]] | Búsquedas "Bitcoin hack" altas predicen rentabilidad baja de Bitcoin | sin_encaje | BTC 1d | bloqueada | F-EXTERNO |
| [[H-059]] | Expansión de crédito bancario eleva la probabilidad de crash bancario | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-060]] | Expansión de crédito predice rentabilidad baja del índice bancario | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |
| [[H-061]] | Predicción por crédito más fuerte con dividend yield bancario bajo | sin_encaje | — | bloqueada | F-MERCADO, F-EXTERNO |

## Qué desbloquearía más
| dato que falta | hipótesis bloqueadas solo por él |
|---|---|
| calendario FOMC (fechas de anuncios programados) | H-003, H-004, H-005, H-022, H-025, H-026, H-027 |
| calendario FOMC con rueda de prensa | H-024 |
| REITs | H-015 |
| universo de acciones individuales | H-016, H-045, H-046, H-047, H-048, H-049 |
| BIST 100 | H-020 |
| Google Trends semanal (búsquedas de Bitcoin) | H-057 |
| retornos de factores (librería de French, carry de divisas) | H-053 |

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

### H-037 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "Con OHLCV diario del S&P 500" |
| frecuencia | 1d | OK (SPY 1d) | ídem |
| campo | OHLCV (cierres) | OK | "log-retorno de cierre a cierre; ... GARCH(1,1) con dummies de día en la constante de la varianza" |
| periodo | antes y después de octubre de 1987 y posterior a 1997 | OK parcial (SPY desde 2006) | "Submuestras antes y después de octubre de 1987 y posteriores a 1997" |

Notas: familia `sin_encaje` porque la hipótesis predice volatilidad condicional por día, no dirección ni momento de una posición.

### H-038 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 | OK (C8: SPY) | "Con OHLCV diario del S&P 500" |
| frecuencia | 1d | OK (SPY 1d) | ídem |
| campo | OHLCV (cierres) | OK | "log-retorno de cierre a cierre sobre dummies de lunes a viernes" |
| periodo | antes y después de 1987 y posterior a 1997 | OK parcial (SPY desde 2006) | "Submuestras antes y después de 1987 y posteriores a 1997" |

### H-051 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índice amplio de renta variable | OK (SPY) | "en un índice amplio de renta variable" |
| frecuencia | 1d (agregada a mes) | OK (SPY 1d) | "Con OHLCV diario del índice: varianza realizada mensual" |
| campo | OHLCV (cierres) | OK | "con los retornos diarios de cierre (unos 22 días)" |

Notas: familia `sin_encaje`: describe la relación entre varianza y rentabilidad del mes siguiente, sin fijar dirección ni momento de una posición (la regla operativa es H-052).

### H-052 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índice amplio de renta variable | OK (SPY) | "en un índice amplio de renta variable" |
| frecuencia | 1d (agregada a mes) | OK (SPY 1d) | "Con OHLCV diario del índice: RV² mensual con retornos diarios de cierre" |
| campo | OHLC (costes de Abdi-Ranaldo) | OK | "neta de costes (estimador de Abdi-Ranaldo con OHLC diario" |

Notas: familia `sin_encaje`: la posición es siempre larga y lo que cambia es el tamaño según la varianza pasada, no la dirección ni el momento. La versión base implica apalancamiento (percentil 99 del peso: 6,4), que choca con C10 (sin apalancamiento); el Test mínimo nombra la variante "límite de apalancamiento a 1 o 1,5". Lo decide el estratega con el usuario.

### H-073 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | S&P 500 (cesta, índice o SPY) | OK (ES, C8) | Predicción: "en el S&P 500 (cesta de constituyentes, índice o SPY)" |
| frecuencia | 15 min | OK (ES 15min) | datos: "OHLCV intradía (15 min)" |
| campo | precio a 14:15/14:30/14:45 y cierre | OK | Test mínimo: "r_prev = precio(14:15/14:30/14:45)/cierre(t−1) − 1" |

Notas: triada en línea el 2026-10-09 a petición del usuario (fuera del lote H-037–H-061). La muestra original (2006-2011) solapa con la IS en 2009-2011.

### H-055 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | Bitcoin | OK (BTCUSDT 1d desde 2017-10-01) | Predicción: "en Bitcoin (y Ripple)" |
| frecuencia | 1d (agregada a semana) | OK (1d) | "Con OHLCV diario (cierre a 23:59:59 UTC): rentabilidades semanales de domingo a domingo" |
| campo | cierre | OK (`btc_close`) | "Regresión de r(t+k) sobre r(t)" |
| periodo | desde 2013 y posterior a mayo de 2018 | OK parcial (BTCUSDT desde 2017-10-01) | "Submuestra desde 2013 y datos posteriores a mayo de 2018" |

Notas: Ripple va entre paréntesis en la Predicción y el Test mínimo no lo exige; se toma como variante (no está en el Inventario). La serie BTC solo existe desde 2021-08-10, fuera de la IS general (2009-2020); la IS cripto (2021-08-10 → 2026-09-29) está autorizada solo para H-PROPIA-001, así que usarla aquí requiere autorización propia del usuario (datos.md).

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

### H-039 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | divisas desarrolladas frente al USD | FALTA | Predicción: "en divisas desarrolladas frente al USD una cartera de igual peso larga en las k divisas de mayor tipo" |
| externo | otro: diferencial de tipos a 3 meses | FALTA (el proxy nombrado, base futuro-spot de divisas, no está en el Inventario) | datos: "requiere otros datos (tipos interbancarios a 3 meses o forwards); proxy con OHLCV diario de spot y futuros de divisas (base futuro-spot)" |
| frecuencia | 1d (agregada a semana, mes o trimestre) | OK (1d) | "rebalanceada cada semana, mes o trimestre" |

Notas: familia `sin_encaje`: la dirección la da el diferencial de tipos, que no es precio, calendario ni evento programado.

### H-040 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | divisas desarrolladas frente al USD | FALTA | Test mínimo: "con OHLCV diario de cada par" |
| externo | otro: diferencial de tipos a 3 meses | FALTA (proxy base futuro-spot no está en el Inventario) | datos: "proxy con OHLCV diario de spot y futuros de divisas (base futuro-spot)" |
| frecuencia | 1d | OK (1d) | "la asimetría sale de OHLCV diario" |

Notas: familia `sin_encaje`: predice asimetría, no dirección ni momento de una posición.

### H-041 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | divisas desarrolladas frente al USD | OK parcial (solo EURUSD y JPYUSD) | datos: "OHLCV diario (pares de divisas frente al USD)" |
| frecuencia | 1d (agregada a trimestre) | OK (1d) | "rentabilidad trimestral z_t y asimetría de los cambios diarios" |
| campo | OHLCV | OK | ídem |

Notas: familia `sin_encaje` (predice asimetría). La ficha W2123888799 dice que el traslado a índices "puede probarse con OHLCV diario de índices y del VIX. Ese traslado no lo prueba el paper", y la hipótesis lo excluye: "esta hipótesis se limita a divisas". No se toma como proxy. Actualizado 2026-10-07: con EURUSD y JPYUSD pasa a compatible; el panel queda en 2 divisas (C-COBERTURA por universo parcial).

### H-042 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | divisas desarrolladas frente al USD | FALTA | "Con OHLCV diario de divisas y la serie diaria del VIX" |
| externo | VIX diario | OK (VIX 1d) | ídem |
| externo | otro: signo del diferencial de tipos | FALTA (proxy base futuro-spot no está en el Inventario) | "multiplicados por el signo del diferencial de tipos (o de la base futuro-spot como proxy)" |
| frecuencia | 1d (agregada a semana) | OK (1d) | "rentabilidad semanal de cada divisa frente al USD y ΔVIX semanal" |

Notas: familia `sin_encaje`: la relación principal es contemporánea ("describe pérdidas, no una regla predictiva"). La ficha W2123888799 sugiere probar con índices y VIX que "ΔVIX al alza coincide con pérdidas"; es un traslado que el paper no prueba y la hipótesis no lo nombra, así que no se toma como proxy. 2026-10-07: con EURUSD y JPYUSD sigue bloqueada; falta el signo del diferencial de tipos (ni tipos ni base futuro-spot).

### H-043 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | pares de divisas desarrolladas | FALTA | "Con OHLCV diario de cada divisa frente al USD" |
| externo | otro: diferencial absoluto de tipos | FALTA (proxy base futuro-spot no está en el Inventario) | "sobre el diferencial absoluto de tipos (o de bases futuro-spot como proxy)" |
| frecuencia | 1d | OK (1d) | "correlación de los cambios diarios por par en ventanas de 13 semanas" |

Notas: familia `sin_encaje`: predice correlación, no dirección ni momento.

### H-044 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | opciones de divisas desarrolladas | FALTA | "en las divisas desarrolladas los risk-reversals a 10 y 25 delta a un mes" |
| externo | otro: volatilidades implícitas por delta | FALTA | "Con volatilidades implícitas a un mes por delta y tipos (o forwards)" |
| externo | otro: tipos de interés o forwards | FALTA | ídem |

Notas: familia `sin_encaje` (describe precios de opciones). La ficha W2092529376 nombra como "sustituto muy imperfecto del risk-reversal" la asimetría realizada "de pares carry o de índices"; los índices están en el Inventario, pero la ordenación por tipo de interés de cada divisa sigue sin datos, así que no se desbloquea.

### H-045 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales EE. UU. (universo amplio) | FALTA | "Con OHLCV diario de un universo amplio de acciones" |
| frecuencia | 1d | OK (1d) | "MAX de cada acción con las rentabilidades de cierre a cierre del mes" |
| campo | capitalización (ponderación por valor) | PROXY (volumen en dólares, OHLCV) | Test mínimo: "por valor (proxy: volumen en dólares)" |

### H-046 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales EE. UU. | FALTA | "Con OHLCV diario de acciones y de un índice" |
| instrumento | índice de mercado | OK (SPY) | ídem |
| frecuencia | 1d | OK (1d) | "IVOL mensual como desviación típica de los residuos diarios frente al índice" |

Notas: familia `sin_encaje`: la dirección la da la volatilidad idiosincrática, no un movimiento de precio que continúe o se deshaga.

### H-047 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | componentes de un índice (acciones individuales) | FALTA | "Con OHLCV diario de los componentes" |
| instrumento | índice ponderado (ajuste y cobertura) | OK (SPY) | "rendimiento ajustado por mercado (frente al índice ponderado)" |
| frecuencia | 1d | OK (1d) | ídem |

Notas: la variante "Repetir con índices o ETF sectoriales" (también la propone la ficha W4234200146) no es la receta mínima y los ETF sectoriales no están en el Inventario.

### H-048 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | componentes o sectores (estrategia de H-047) | FALTA | "Construir la estrategia de H-047 (acciones individuales y, por separado, índices o ETF sectoriales)" |
| externo | VIX diario | OK (VIX 1d) | "Regresión diaria y mensual de su rentabilidad sobre el VIX desfasado 5 días" |
| frecuencia | 1d | OK (1d) | ídem |

### H-049 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales EE. UU. | FALTA | "Con OHLCV diario de acciones" |
| frecuencia | 1d (agregada a mes) | OK (1d) | "quintiles independientes por rentabilidad acumulada t−3…t−1 y por rentabilidad del mes t" |

Notas: la ficha W2590014621 menciona aplicarlo a "un universo de índices o ETFs" como "una extrapolación no testada en el texto"; no es un proxy nombrado.

### H-050 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales EE. UU. | FALTA | "Con 13F ... y OHLCV diario" |
| externo | otro: tenencias institucionales 13F | FALTA | datos: "requiere otros datos (tenencias institucionales 13F con clasificación activa/pasiva)" |
| frecuencia | 1d (agregada a mes) | OK (1d) | ídem |

Notas: el proxy que nombra la ficha W2590014621 ("el propio retorno 3M") reduce la hipótesis a H-049, que también exige el universo de acciones.

### H-053 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| externo | otro: retornos diarios y mensuales de factores (French, carry) | FALTA | datos: "requiere otros datos (retornos diarios y mensuales de factores, p. ej. librería de Ken French; factor carry de divisas)" |
| frecuencia | 1d (agregada a mes) | OK (1d) | "Con retornos diarios y mensuales de los factores" |

Notas: familia `sin_encaje` (tamaño por volatilidad, como H-052). La ficha W4403804186 (contradice) nombra como proxies no validados "índices o ETF de estilo", que no están en el Inventario, y "factores de precio" con "varios índices" (momentum transversal o low-beta entre índices). Con SPY, QQQ, IWM y DIA eso sería otra hipótesis y no los factores de la predicción; no se toma como proxy. La versión del factor de mercado ya es H-052.

### H-054 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | acciones individuales (CRSP) para construir los factores | FALTA | datos: "factores construidos con CRSP/Compustat; costes por acción con OHLC diario" |
| externo | otro: fundamentales (Compustat) | FALTA | ídem |
| instrumento | índice de mercado (volatilidad realizada) | OK (SPY) | "volatilidad realizada del mercado con retornos diarios del mes" |

Notas: familia `sin_encaje`. Los proxies de la ficha W4403804186 (ETF de estilo, factores de precio con varios índices) tienen la misma limitación que en H-053, y la propia hipótesis dice que "los ETF de estilo como proxy no permiten replicar la compensación de operaciones".

### H-056 · proxy
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | Bitcoin | OK (BTC 1d) | Predicción: "en Bitcoin la regresión de la rentabilidad de las semanas t+1 y t+2" |
| externo | sentimiento: Google Trends semanal | PROXY (volumen anómalo de BTCUSDT, añadido el 2026-10-07) | datos: "requiere otros datos (Google Trends semanal, recuento de tuits); proxy no validado con volumen anómalo de OHLCV" |
| frecuencia | 1d (agregada a semana) | OK (1d) | "OHLCV diario agregado a semanas" |

Notas: familia `sin_encaje`: la señal es la atención, que no es precio, calendario ni evento programado. El Test mínimo cita también Ripple y Ethereum, pero la Predicción solo exige Bitcoin. Con el volumen diario de BTCUSDT (2026-10-07) pasa a `proxy` (P-OTRO, C-NOVALID).

### H-057 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | Bitcoin | OK (BTC 1d) | "rentabilidad semanal de Bitcoin en t+1" |
| externo | sentimiento: Google Trends semanal ("Bitcoin hack", "Bitcoin") | FALTA | "Google Trends semanal de ambos términos" |
| frecuencia | 1d (agregada a semana) | OK (1d) | ídem |

Notas: familia `sin_encaje`, como H-056.

### H-058 · compatible
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | Bitcoin | OK (BTC 1d) | Predicción: "en BTC, XRP y ETH la rentabilidad diaria media de los sábados" |
| instrumento | Ripple (XRP) y Ethereum (ETH) | OK (ETH desde 2017-08); parcial (XRP solo 2025-07 → 2026-05, ~43 sábados) | ídem; Test mínimo: "por cripto" |
| frecuencia | 1d | OK (1d) | "Con OHLCV diario" |

Notas: la hipótesis exige las tres ("no consistente entre las tres criptomonedas" la refuta). Una versión solo con BTC sería factible con BTC 1d desde 2021-08-10, con la misma salvedad de autorización de la IS cripto que H-055. 2026-10-07: con BTCUSDT, ETHUSDT y XRPUSDT pasa a compatible (C-COBERTURA por XRP). Muestra por activo, sin fijar.

### H-059 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índices bursátiles bancarios de países desarrollados | FALTA | "Variable dependiente con OHLCV del índice bancario" |
| externo | otro: crédito bancario y PIB por país | FALTA | datos: "requiere otros datos (crédito bancario al sector privado y PIB por país, BIS / Schularick-Taylor)" |
| frecuencia | 1d (agregada a trimestre) | OK (1d) | "algún trimestre < −30 %" |

Notas: familia `sin_encaje`: la señal es una variable macro no programada. Los proxies de precio que propone la ficha W2185764662 (subida prolongada del índice bancario, ratio índice bancario / índice general) también necesitan un índice bancario, que no está en el Inventario.

### H-060 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índices bursátiles bancarios de países desarrollados | FALTA | "en índices bancarios de países desarrollados" |
| externo | otro: crédito bancario y PIB por país | FALTA | datos: "requiere otros datos (crédito bancario/PIB por país, dividendos y tipo a 3 meses para el exceso)" |
| frecuencia | 1d (agregada a 1-3 años) | OK (1d) | "retorno log en exceso (o de precio, con OHLCV) a 1-3 años" |

Notas: familia `sin_encaje`, como H-059. Dividendos y tipo corto no se cuentan como requisito porque el Test mínimo admite el retorno "de precio, con OHLCV".

### H-061 · bloqueada
| requisito | valor | estado | cita / dónde se nombra el proxy |
|---|---|---|---|
| instrumento | índices bursátiles bancarios por país | FALTA | "quintiles de dividend yield bancario por país" |
| externo | otro: crédito bancario y PIB por país | FALTA | datos: "requiere otros datos (crédito bancario/PIB por país, dividend yield del índice bancario)" |
| externo | otro: dividend yield del índice bancario | FALTA | ídem; Riesgos: "el dividend yield no sale de OHLCV" |
| frecuencia | 1d (agregada a 1-3 años) | OK (1d) | "regresión del retorno a 1-3 años no solapado" |

Notas: familia `sin_encaje`, como H-059.
