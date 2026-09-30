# Volumen firmado (order flow)

- **Qué es:** contratos comprados menos vendidos, clasificando cada operación como compra o venta (quien cruza el spread). **RSV** = firmado / total ∈ [−1, 1] (W3122771383, ec. 6).
- **En el paper:** RSV de la hora 15:15–16:15 ET, el cierre de EE. UU. Si es < 0, los market makers se quedan largos y el rebote nocturno es mayor. Es la señal de BtD en [[H-007]].
- **Qué tenemos:** OHLCV. La **V es volumen total, sin signo.** No hay datos operación a operación.
- **Proxy posible:** firmar cada barra de 15 min por el signo de su movimiento (cierre − apertura) y ponderarla por su volumen. Es una técnica conocida, pero cuenta como **proxy**, no como la medida del paper.
