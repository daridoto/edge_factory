# Prima de liquidez y libro de órdenes

Explicación construida en conversación con el usuario (2026-10-05) para entender el mecanismo de [[H-007]]. Fuente de la tesis: W3122771383 (Boyarchenko, Larsen y Whelan). Los ejemplos con cifras son ilustrativos.

## Libro de órdenes
- **Bid (mejor compra):** el precio más alto al que alguien compra ahora. **Ask (mejor venta):** el más bajo al que alguien vende.
- **Precio de mercado ≈ (bid + ask) / 2**, sin ponderar.
- Una orden a mercado grande «se come» niveles del libro y mueve el precio. Por la noche el libro es fino: cualquier orden lo mueve mucho.
- El precio puede moverse **sin que nadie opere**: basta con que quien pone las órdenes las cambie. Por la noche casi solo cotizan los market makers.

## Mecanismo (tesis del paper)
1. Un fondo vende fuerte al cierre de EE. UU. Los market makers son la contraparte y compran con descuento: el fondo paga la urgencia.
2. De noche, cargados y casi solos, **bajan su bid y su ask** (no quieren más y quieren atraer compradores). El precio queda por debajo de su valor justo.
3. A las 02:00 ET (apertura europea) llegan participantes sin inventario que ponen órdenes a precios normales. La competencia devuelve las cotizaciones a su nivel y el precio sube.
4. Es una **prima de riesgo/liquidez, no una ineficiencia**: si esa noche llega una mala noticia, el valor justo cae y se pierde (el win rate de H-007 es del 43 %).
5. Por eso [[H-008]] (BtD) opera solo tras un cierre vendedor: es cuando hay inventario que soltar.

## Acciones frente a futuros
- «Acciones» = las 500 del S&P 500 (el índice); SPY ≈ índice / 10; ES ≈ índice + carry (intereses − dividendos).
- Precios distintos, mismos movimientos en %: los arbitrajistas los alinean, así que el desequilibrio del cierre golpea a ambos.
- De noche solo cotiza el ES: allí está el riesgo y la prima. Se operaría en futuros (MES con 10.000 USD; 1 ES ≈ 13× de apalancamiento).
- El «valor justo» no se ve en ningún precio: solo se deduce después, por el rebote.

## Preguntas abiertas
- **¿Por qué un fondo necesita vender ~500 M USD a mercado y de inmediato al cierre?** (rebalanceos, reembolsos, cobertura, fondos apalancados…). Pendiente para la próxima sesión.

## Profundidad, estrategias de libro y datos (2026-10-05, conversación)
- **Profundidad:** cuánto volumen hay en cada nivel de precio a cada lado. Niveles de dato: L1 (mejor bid/ask), L2 (volumen agregado por nivel, p. ej. 10 niveles), L3/MBO (orden a orden, con colas).
- **Bid/ask** son las mejores órdenes límite *pendientes*. Quien compra a mercado paga el ask y quien vende a mercado cobra el bid. La diferencia es el spread.
- **Familias de estrategias de libro:** desequilibrio del libro / order flow imbalance (Cont, Kukanov y Stoikov, 2014), lectura de flujo (delta, absorción, icebergs), market making (Avellaneda y Stoikov, 2008; es la contraparte del mecanismo de H-007) y latencia/HFT.
- **Inferencia:** son ventajas de segundos que dependen de la latencia, la posición en la cola y el coste. Con cuenta retail el spread y las comisiones suelen comérselas.
- **Datos:** existen y se venden (Databento, CME DataMine, LOBSTER, Tardis.dev en cripto). Ocupan GB por día y obligan a simular colas y fills. El lab no tiene datos de libro y no se van a buscar más datos.

## Quién vende fuerte al cierre (2026-10-05, conversación)
Respuesta a la pregunta abierta. Fuente: la ficha W3122771383 del repo de papers para lo que mide el paper; el resto es cultura general sin contrastar en el lab.
- **Dato (paper):** el desequilibrio se mide en el **futuro ES**, no en acciones: RSV (volumen firmado / volumen total) entre 15:15 y 16:15 ET. Cada operación se clasifica como compra o venta según se cruce en el ask o en el bid. El paper no identifica quién vende.
- **Por qué al cierre:** el precio de cierre es la referencia del NAV de fondos índice y fondos de inversión, así que rebalanceos, suscripciones y reembolsos se ejecutan ahí. Además, a las 16:00 cierran las acciones y desde entonces el ES es casi el único instrumento para ajustar exposición.
- **Vendedores típicos (inferencia):** ETF apalancados e inversos que rebalancean cada día en la dirección del movimiento (venden si el día cae); dealers de opciones con gamma corta, que cubren vendiendo en caídas; fondos de volatilidad objetivo, risk parity y CTA, que recortan exposición cuando sube la volatilidad; llamadas de margen y desapalancamiento; rebalanceos de fin de mes o trimestre.
- **Conexión con [[H-008]]:** casi todos venden *más* en días de caída, lo que encaja con la asimetría del paper: las reversiones tras ventas son mucho mayores que tras subidas.
- **Pendiente:** comprobar la cifra de ~500 M USD; no consta en la ficha y era ilustrativa.

## Glosario de flujos de cierre (2026-10-05, conversación)
- **Volumen firmado:** en cada operación hay un comprador y un vendedor. El signo lo pone el **agresor**, quien usa una orden a mercado: si compra, la operación se cruza en el ask y suma (+); si vende, se cruza en el bid y resta (−). Ejemplo: 100 contratos comprados a mercado y 300 vendidos a mercado dan un volumen de 400, un volumen firmado de −200 y un RSV de −50 %.
- **NAV (valor liquidativo):** lo que vale la cartera del fondo por participación. Se calcula con los precios de cierre, y las entradas y salidas de partícipes se liquidan a ese valor.
- **ETF apalancado o inverso:** promete un múltiplo del movimiento *diario* (TQQQ ×3, SQQQ −3). Ejemplo ×3: 100 de capital y 300 de exposición; si el índice cae un 10 %, quedan 70 de capital y 270 de exposición, y para volver a ×3 (210) vende 60. El inverso, tras una caída, gana y tiene que ampliar su corto: también vende. Ambos operan al cierre y en la dirección del día. Es mecánico y se puede estimar a partir de su patrimonio.
- **Gamma de dealers:** la gamma mide cuánto cambia la cobertura (delta) de quien tiene opciones cuando el precio se mueve. Con gamma corta (vendió opciones), cubrirse obliga a vender cuando cae y comprar cuando sube, y amplifica el movimiento. Con gamma larga ocurre lo contrario y lo amortigua. Hay estimaciones públicas (GEX) a partir del open interest, pero son aproximadas y requieren datos de opciones, que el lab no tiene.
- **Volatilidad objetivo:** el fondo mantiene un riesgo fijo; si la volatilidad sube, reduce la posición. **Risk parity:** reparte el riesgo por igual entre acciones, bonos, etc. y también recorta cuando sube la volatilidad. **CTA:** fondos de tendencia en futuros que venden cuando el precio rompe a la baja.
- **Llamadas de margen:** afectan también a fondos apalancados con su prime broker (p. ej. Archegos, 2021), no solo a retail.
- **Corrección:** un rebalanceo de pesos fijos (por ejemplo una cartera 60/40) va *contra* el movimiento del periodo: si las acciones han caído, compra. Venderá solo si las acciones han subido más que los bonos. Los cambios de composición de índices sí se ejecutan al cierre.
- **Condicionar la prima (ficha del paper):** OD incondicional tiene Sharpe −0,5 después de costes; BtD, que opera solo tras un cierre vendedor, 1,1. Con el VIX en 30 la respuesta a un cierre vendedor es de 6,1 pb, y con el VIX en 12 es casi nula. El lab tiene VIX 1d (desde 2006) pero no volumen firmado: H-008 usa el retorno de 15:00 a 16:00 como proxy.
