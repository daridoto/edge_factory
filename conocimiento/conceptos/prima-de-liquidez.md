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
