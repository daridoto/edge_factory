# Convenciones del laboratorio

Decisiones que se toman **una vez** y aplican a todas las hipótesis, para que los agentes no las pregunten en cada receta. Se aplican siempre; si el usuario cambia alguna en la conversación, se edita aquí.

Si una receta necesita apartarse de una convención, lo dice en "Decisiones de implementación" citando el número.

| # | tema | valor |
|---|---|---|
| C1 | Unidad de coste | Los costes se expresan **por lado** (entrada y salida por separado). Una operación intradía completa paga 2 lados. Si la fuente da un coste "por operación" o "de ida y vuelta", se divide entre 2. |
| C2 | Tamaño del tick | ES: 0,25 puntos. NQ: 0,25 puntos. SPY y ETF: 0,01 $. "1 tick" en una fuente = 1 tick por lado, convertido a pb con el precio de entrada sin ajustar. |
| C3 | Coste por defecto | Si ni la hipótesis ni las fichas citan coste: **1 tick por lado** (C2). |
| C4 | Fuera de posición | La rentabilidad es 0 (sin tipo de interés ni T-bills). |
| C5 | Calendario de sesiones | Las sesiones del fichero (columna `Date` del SPY) se consideran conocidas de antemano, incluidos los cierres no programados (p. ej. el huracán Sandy). No se excluyen ventanas por ello. |
| C6 | Rolls del ES | Se salta cualquier tramo de retorno que cruce la barra del domingo 18:00 inmediatamente anterior al tercer viernes de mar/jun/sep/dic. La regla se aplica a todos los años, aunque solo esté verificada desde 2022 (ver datos.md). |
| C7 | Barras que faltan | Si falta una barra necesaria, se salta esa sesión. No se interpola. Se cuentan las sesiones saltadas por motivo. |
| C8 | Instrumentos equivalentes | Dentro de cada grupo se puede usar cualquiera sin que cuente como proxy: {S&P 500, SPY, ES} · {Nasdaq 100, QQQ, NQ} · {Russell 2000, IWM} · {Dow Jones, DIA}. Para diario se prefiere el ETF (sesión NYSE, ajustado). Para intradía se usa el futuro (único dato intradía). |
| C9 | Frecuencia | Una frecuencia más fina sirve para construir una más gruesa (15 min → 30 min, 1 h o diario). Una más gruesa nunca sustituye a una más fina, salvo como proxy citado en la fuente. |
| C10 | Tamaño de posición | 1 unidad por defecto; el plan puede fijar una fracción de la equity al entrar (`fraccion`, ≤ 1; en H-001 el usuario fijó 30 %). Sin apalancamiento, sin stops ni objetivos. |
| C11 | Anualización | 252 sesiones por año. |
| C12 | Muestra (IS/OOS) | IS 2009-09-27 → 2020-12-31 inclusive. OOS y holdout solo con autorización explícita del usuario (ver `CLAUDE.md`). |
| C13 | Proxies | Un proxy solo se usa si lo nombra la hipótesis o una ficha. Si la fuente dice que no está validado, el triaje lo marca `proxy` y se comenta con el usuario antes de ejecutar. |
