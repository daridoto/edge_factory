# Catálogo de datos históricos

Raíz: `data/` en este repo (**solo lectura**, ignorada por git). Es una copia local de `/Users/tommy/Documents/data_historica`, a la que los asistentes no tienen acceso. Todas las rutas de este catálogo son relativas a `data/`.

Este catálogo existe para que los agentes no tengan que abrir los datos. Recoge lo comprobado por inspección el 2026-09-22; lo que no se ha comprobado está marcado como **no verificado**.

## Muestra in-sample (IS)

**2009-09-27 → 2020-12-31**, ambos inclusive, confirmada por el usuario para H-001 (C12). Coincide con los ficheros preparados con sufijo `IS` (`indices/nq/predata/nq_*_IS_adj.csv` y `macro/eventos_macro_IS_2009_2020.csv`). El resto de ficheros son mixtos (llegan a 2026): se abren y se filtra IS antes de cualquier cálculo (ver `CLAUDE.md`).

## Inventario (tabla para el triaje)

Lo que hay, sin matices. El detalle de cada dataset está más abajo.

| instrumento | clase | frecuencia | campos | desde | hasta | hora |
|---|---|---|---|---|---|---|
| SPY | renta variable EE. UU., gran capitalización (S&P 500) | 1d | OHLCV + dividendos (ajustado) | 2006-07-17 | 2026-07-15 | sesión NYSE |
| QQQ | renta variable EE. UU., tecnológicas (Nasdaq 100) | 1d | OHLCV (formato no verificado) | 2006-07-17 | 2026-07-15 | sesión NYSE |
| IWM | renta variable EE. UU., pequeña capitalización (Russell 2000) | 1d | OHLCV (formato no verificado) | 2006-07-17 | 2026-07-15 | sesión NYSE |
| DIA | renta variable EE. UU., gran capitalización (Dow Jones) | 1d | OHLCV (formato no verificado) | 2006-07-17 | 2026-07-15 | sesión NYSE |
| Russell 2000 (índice) | renta variable EE. UU., pequeña capitalización | 1d | OHLCV (formato no verificado) | 2006-07-17 | 2026-07-15 | sesión NYSE |
| ES (E-mini S&P 500) | futuro de índice EE. UU., gran capitalización | 15min | OHLCV, sin ajustar por roll | 2009-09-27 | 2026-05-28 | ET, 24 h (Globex) |
| NQ (E-mini Nasdaq 100) | futuro de índice EE. UU., tecnológicas | 15min | OHLCV + ajustado (ajuste verificado solo desde 2022) | 2009-09-27 | 2026-05-28 | ET, 24 h (Globex) |
| VIX | volatilidad implícita S&P 500 | 1d | OHLC (volumen 0) | 2006-07-17 | 2026-07-15 | sesión |
| TSLA | acción individual EE. UU. | 1d | no inspeccionado | 2010-06-29 | 2026-05-29 | — |
| SOLUSDT | cripto | 1d | OHLCV | 2020-08-11 | 2026-06-01 | — |
| Eventos macro EE. UU. | calendario con hora | evento | NFP, CPI, PPI, JOLTS, REAL_EARNINGS, PRODUCTIVITY, ECI | 2009-01 | 2020-12 | hora EE. UU. |

**No hay:** calendario FOMC; PIB, ISM, MCSI ni actas; barras de menos de 15 min; bid/ask, spread o volumen firmado (compras/ventas); VIX intradía; universo de acciones individuales (solo TSLA); REITs; mercados fuera de EE. UU. (salvo cripto); curva del Tesoro; sentimiento; sorpresas (consenso frente a dato); resultados empresariales. Los festivos de NYSE solo se pueden derivar de los huecos de sesión del SPY.

## Datasets

### SPY diario (Norgate): referencia para hipótesis diarias de renta variable EE. UU.
- Ruta: `etf/indices/SP500 SPY - Temp. 1d - Date 2006-07-17 a 2026-07-15 - Norgate.csv`.
- Columnas: `Date,Open,High,Low,Close,Volume,Turnover,Unadjusted Close,Dividend`.
- Precios OHLC **ajustados por dividendos** (Close 2006-07-17 = 85,40 frente a `Unadjusted Close` 123,34). Rentabilidad close-to-close = rentabilidad total.
- Una fila por sesión de NYSE, solo lunes-viernes, sin NaN.
- Sin hora: el open es la apertura de las 9:30 ET y el close el cierre de las 16:00 ET.

### ES (E-mini S&P 500) 15 minutos: referencia para hipótesis intradía
- Ruta: `indices/ES_15min_2009-2026.csv`. Columnas `ts,open,high,low,close,volume`. 2009-09-27 18:00 → 2026-05-28 03:15.
- `indices/ES - E-mini S&P 500 - Temp. 15MIN ... sin encabezado ...`: **bruto** original en TXT sin cabecera (`MM/DD/YYYY,HH:MM,o,h,l,c,v`). Se conserva como fuente; para trabajar se usa el CSV tratado.
- **Hora: ET (hora de Nueva York), con horario de verano ya aplicado.** El pico de volumen de la apertura de contado cae en la barra `09:30` tanto en enero como en julio.
- **La etiqueta `ts` marca el inicio de la barra.** La barra `09:30` cubre 09:30-09:45. Por tanto:
  - "precio a las 10:00" = `close` de la barra `09:45`
  - "precio a las 16:00" = `close` de la barra `15:45`
  - "retorno 15:30-16:00" = `close(15:45) / close(15:15) − 1`
- Sesión Globex de ~23 h: abre a las 18:00 ET (domingo a jueves). Casi no hay barras en 17:00-17:45 (pausa diaria). Las barras 16:15-16:45 aparecen menos que el resto (~4 000 frente a ~4 150 de una hora normal), así que hay sesiones en las que faltan.
- **Precios sin ajustar por roll.** El roll cae en la barra del **domingo 18:00 de la semana de vencimiento** (trimestral: mar/jun/sep/dic). En los 15 rolls de 2022-2026 (localizados con el `adj_factor` del NQ), el salto mediano del ES en esa barra es de **89 pb**, frente a 5 pb en un domingo 18:00 normal. Cualquier retorno que cruce ese domingo (overnight del viernes al lunes, retorno "desde el cierre anterior" del lunes) está contaminado en esas sesiones. La regla exacta para los rolls anteriores a 2022 está **no verificada**.
- Las barras de fin de semana o festivo pueden faltar. Si falta una barra necesaria para una señal, ese día no hay operación: no se interpola.

### ES diario: **no usar para rentabilidades diarias**
- Ruta: `indices/ES_daily_2009-2026.csv`. Es la agregación **por día natural** de las barras de 15 min (open y close coinciden al 100 % con la primera y la última barra del día natural), no por sesión: hay filas de domingo y el "close" del lunes es el de las 23:45. No tiene significado de sesión.

### NQ (E-mini Nasdaq 100)
- `indices/nq/DATOS-DATA-NQ-20260624-15MIN-TXT.txt`: **bruto** original en TXT (mismo formato que el bruto del ES). Se conserva como fuente; para trabajar se usa el CSV tratado.
- `indices/nq/nq_15m_ohlcv.csv`: tratado; mismas horas que el ES más columnas `*_adj` y `adj_factor`. El `adj_factor` solo cambia en 15 rolls desde 2022-09-11. Antes de esa fecha es constante, así que el ajuste de 2009-2022 está **no verificado**.
- `indices/nq/nq_1d_adj.csv`: diario (misma construcción por día natural que el ES diario, **no verificado**).
- `indices/nq/predata/nq_{1d,2h,4h}_IS_adj.csv`: remuestreos IS (2009-09-27 → 2020-12-31) preparados por el usuario. Columnas `fecha,open,high,low,close` (sin volumen).

### Otros índices y ETF diarios (Norgate, 2006-07-17 → 2026-07-15)
- `etf/indices/`: QQQ, IWM, DIA y SPY. `indices/`: Russell 2000 (índice, distinto del IWM). Los cuatro de `etf/indices/` son ETF (precios a escala de ETF, ajustados por dividendos). Formato supuesto igual al SPY (**no verificado**).

### Macro
- `macro/eventos_macro_IS_2009_2020.csv`: `fecha,hora,tipo`. La hora es de EE. UU. con formato `08:30 AM`. Tipos: NFP, JOLTS, PPI, CPI, REAL_EARNINGS (144 cada uno), PRODUCTIVITY (131), ECI (48). **No incluye FOMC**, PIB, ISM ni actas.
- `macro/Indice de volatilidad VIX - Temp. 1d ... Norgate.csv`: VIX diario OHLC; volumen a 0.
- `macro/CPIhistreleasedates.pdf`: fechas de publicación del IPC (sin procesar).

### Otros
- `equities/TSLA ...` (TradingView BATS, diario): **no inspeccionado**.
- `cripto/SOLUSDT ...` (Binance, diario): CSV exportado con indicadores mezclados (medias, RSI, columnas duplicadas `2Y-MA`). Solo son útiles `time,open,high,low,close,Volume`.

## Qué falta (bloquea hipótesis)
- **Calendario FOMC** (fechas y horas de los anuncios, con y sin rueda de prensa): H-003-006, H-021-028, H-035.
- Calendario de festivos de NYSE: se puede derivar de la lista de sesiones del SPY, pero los huecos de sesión mezclan festivos con otros cierres (p. ej. el huracán Sandy en 2012 o funerales de Estado).
- Curva del Tesoro, sentimiento, sorpresas de tipos y de NFP, I/B/E/S, acciones individuales, REITs y BIST 100.
