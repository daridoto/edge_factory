---
id: H-018
---

# H018-IS-REAL-001 · Plan anterior al cálculo

Receta: [estrategias/H-018.md](../../estrategias/H-018.md). Muestra IS 2009-09-27 → 2020-12-31. OOS no autorizado.

## Qué se mide
- **Estadístico:** retorno diario medio de SPY en la víspera de los 8 festivos menos el del resto de sesiones, en pb/día, con desglose por festivo. Retornos close-to-close ajustados por dividendos.
- **Operativa:** largo 1 acción del cierre anterior a la víspera al cierre de la víspera. Coste 0,01 USD por acción y lado. Referencia al 100 % del capital.
- **Robustez:** bootstrap por bloques de 12 meses; estadístico por año natural y sin cada año; costes ×2.
- **Referencia:** W2943226912, S&P 500 1999-2017: significativo al 5 %, concentrado en Viernes Santo, Labor Day y Navidad.

## Piezas nuevas del lab (genéricas, con test)
- `laboratorio/festivos.py`: cierres observados de NYSE por regla; ventana `festivos` (valores = festivos; etiqueta = festivo).

## Especificación ejecutable

```toml
id = "H018-IS-REAL-001"
hipotesis = "H-018"
variante = "SPY · víspera"
version = "real-is-v1"
pregunta = "¿Rinde más SPY en la sesión previa a un festivo que en el resto de sesiones?"
receta = "estrategias/H-018.md"
cambio = "Primer ensayo: víspera de los 8 festivos de W2943226912 en SPY."

[datos]
dataset = "SPY 1d"
periodo = "1d"

[ventana]
tipo = "festivos"
valores = ["ano_nuevo", "presidentes", "viernes_santo", "memorial", "independencia", "trabajo", "accion_gracias", "navidad"]
nombre = "víspera"

[estadistico]
tipo = "media_vs_resto"
desglose = true

[operativa]
capital = 10000.0
coste_lado = 0.01
entrada = "Comprar al cierre de la sesión anterior a la víspera."
salida = "Vender al cierre de la víspera."
tamano = "1 acción por víspera; referencia al 100 % del capital aparte."
costes = "0,01 USD por acción y lado; sin comisión adicional ni impacto."

[bootstrap]
unidad = "mes"
bloque = 12
motivo = "Cada festivo cae una vez al año; bloques de 12 meses conservan un año completo de festivos."

[conclusiones]
supuestos = [
  "Víspera = última sesión antes de un cierre observado de NYSE por uno de los 8 festivos (reglas en festivos.py).",
  "Año Nuevo en sábado (2011) no es cierre: ese año no hay víspera de Año Nuevo.",
  "Retornos close-to-close ajustados por dividendos, antes de costes.",
]
limites = [
  "Unas 89 vísperas en la IS (10-12 por festivo): el intervalo será ancho y el desglose por festivo, ruidoso.",
  "Solapa con el cambio de mes (H-001) en Labor Day, Navidad y Año Nuevo.",
  "El intervalo no corrige la exploración previa de esta hipótesis en la literatura.",
]
siguiente = "Según el resultado: mirar el desglose por festivo y el solapamiento con TOM, en IS."
```
