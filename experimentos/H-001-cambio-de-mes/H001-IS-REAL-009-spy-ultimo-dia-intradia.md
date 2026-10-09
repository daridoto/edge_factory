# H001-IS-REAL-009 · Último día del mes, apertura → cierre

Plan fijado el 2026-10-08 antes del cálculo. Variante solicitada por el usuario: únicamente la última sesión bursátil, sin exposición nocturna. Autorización en conversación: «vale entonces podemos probar que pasa con entry en apertura y exit en la salida para ver si eso de por si presetna ventaja no?»; salida interpretada como cierre según el intercambio previo. SPY y QQQ por separado, solo IS.

Retorno Open → Close del último día frente al mismo retorno del resto de sesiones. No es una réplica del TOM de cuatro días del paper, ni demuestra un mecanismo. Una operación por mes completo, sin filtros ni búsqueda de parámetros. C1–C5, C10–C12: costes por lado, efectivo sin remunerar, calendario observado; tamaño de referencia 99,9 % para dejar margen a costes. No se retienen dividendos nocturnos: Open y Close usan el mismo ajuste del día.

```toml
id = "H001-IS-REAL-009"
hipotesis = "H-001"
version = "real-is-intradia-v1"
variante = "SPY · último día · Open-Close"
pregunta = "¿Rinde más SPY de apertura a cierre en el último día bursátil del mes que en las demás sesiones?"
receta = "estrategias/H-001.md"
cambio = "MVP intradía solicitado: último día bursátil, apertura a cierre, sin overnight ni filtros."

[datos]
dataset = "SPY 1d"
periodo = "1d"
tramo = "apertura_cierre"

[ventana]
tipo = "dias_de_mes"
valores = [-1]
nombre = "último día · Open-Close"

[estadistico]
tipo = "media_vs_resto"

[operativa]
capital = 10000.0
coste_lado = 0.01
fraccion = 0.999
entrada = "Comprar al Open del último día bursátil de cada mes completo IS."
salida = "Vender al Close de esa misma sesión; sin posición nocturna."
tamano = "99,9 % de equity por operación, acciones fraccionarias; margen restante para costes, sin apalancamiento."
costes = "0,01 USD por acción y lado (C1–C3), Open negociado reconstruido con el factor Close/Unadjusted Close del día."

[bootstrap]
unidad = "mes"
bloque = 3
motivo = "Evento mensual: bloques circulares de 3 meses; 5000 réplicas, semilla fija del laboratorio."

[conclusiones]
supuestos = [
  "Solo IS según proteccion.py; se excluye septiembre de 2009 por incompleto.",
  "Último día identificado por calendario observado (C5); una operación por mes.",
  "Evidencia bruta Open-Close comparada con Open-Close del resto, incluidos los tres primeros días del mes.",
  "Open y Close ajustados con el mismo factor diario; no se cobra el gap nocturno ni dividendos por tenencia nocturna.",
  "Ejecución idealizada en Open y Close; efectivo sin remunerar, sin stops ni filtros de volumen.",
]
limites = [
  "Selección exploratoria tras estudiar previamente TOM: el intervalo no corrige esa exploración.",
  "Precio de apertura/cierre del proveedor, no garantía de ejecución en subasta; costes simplificados sin impacto.",
  "Con OHLC diario no se mide el drawdown intradía; drawdown de la curva a cierre.",
  "C5 presupone conocidos los cierres no programados; no es una simulación exacta del calendario disponible en tiempo real.",
  "No establece causalidad ni autoriza OOS; tamaño elegido para lectura sobre capital, no optimizado.",
]
siguiente = "Revisar con el usuario el resultado antes de proponer o ejecutar otra variante."
```
