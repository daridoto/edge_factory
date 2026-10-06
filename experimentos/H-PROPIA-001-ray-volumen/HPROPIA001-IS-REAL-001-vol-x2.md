---
id: H-PROPIA-001
---

# HPROPIA001-IS-REAL-001 · Plan anterior al cálculo

Receta: [estrategias/H-PROPIA-001.md](../../estrategias/H-PROPIA-001.md). Plan fijado el 2026-09-30. Las reglas y los parámetros son los del usuario, sin cambios. Ya se había hecho un contraste independiente fuera del lab ([[H-PROPIA-001]]): sus cifras se conocían antes de fijar el plan.

**Autorización de la muestra (literal, 2026-09-30):** «directamente backtestea la estrategia eso nos servira para contrastar y ver si nos da lo mismo, ademas no hagas caso al contrato si quieres hablemos aqui los periodos de muestra para que estes listo o propon alguno, creo que usamos todo el historico porque en cripto no hay tanto rangos de tiempo». Después: «hazlo quieor ver esta joya en el dashboard ya mismo». Muestra IS cripto: 2021-08-10 → 2026-09-29, solo para H-PROPIA-001. Lo posterior es seguimiento en tiempo real (OOS).

## Qué se mide
- **Estadístico:** retorno neto medio por operación, en %. Se añaden la mediana, la t, el exceso frente a BTC y el percentil frente a un placebo de fechas aleatorias.
- **Operativa:** largo con el 100 % de la equity, a la apertura siguiente a la señal. Salida por stop del −25 % o por tiempo a t + 28. Coste del 0,2 % por lado. Capital de 10.000 USDT. La cuenta se valora al cierre diario (UTC).
- **Robustez:** bootstrap por operación (bloque 1), estadístico por año, sin cada año y con costes ×2.

## Qué no se hace en este ensayo
- Sensibilidad del umbral, de las ventanas, de la tenencia o del stop.
- Otros tokens y la cesta de DEX.
- Deslizamiento en los gaps del stop más allá de la apertura.

## Especificación ejecutable

```toml
id = "HPROPIA001-IS-REAL-001"
hipotesis = "H-PROPIA-001"
version = "real-is-v1"
pregunta = "¿Rinde RAY en los 28 días siguientes a que el volumen de Raydium doble su nivel normal?"
receta = "estrategias/H-PROPIA-001.md"
cambio = "Primer ensayo: reglas del usuario sin cambios."

[datos]
dataset = "RAY 1d"
serie = "Raydium volumen 1d"
referencia = "BTC 1d"

[senal]
tipo = "ratio_medianas"
nombre = "VOL×2"
corta = 7
larga = 90
umbral = 2.0
enfriamiento = 28

[estadistico]
tipo = "media_operacion"
unidad = "% / operación"

[operativa]
capital = 10000.0
moneda = "USDT"
coste_pct = 0.002
fraccion = 1.0
tenencia = 28
stop = 0.25
entrada = "Largo a la apertura del día siguiente a la señal (mediana 7 d / mediana 90 d del volumen de Raydium ≥ 2)."
salida = "Stop −25 % (al stop, o a la apertura si abre por debajo); si no, al cierre del día t + 28."
tamano = "100 % de la equity, una operación a la vez, sin apalancamiento; 28 días sin señales tras cada una."
costes = "0,2 % del nocional por lado."

[placebo]
sorteos = 2000
semilla = 7301

[bootstrap]
unidad = "operación"
bloque = 1
motivo = "Las operaciones no se solapan (enfriamiento = tenencia); con 16 operaciones no caben bloques más largos."

[conclusiones]
supuestos = [
  "Velas diarias UTC de Binance spot; el volumen de DefiLlama se da por conocido al cierre UTC de su día.",
  "Las medianas cuentan días con dato: los 4 huecos de DefiLlama se saltan, como en la implementación del usuario.",
  "El stop se ejecuta exactamente al nivel salvo gap de apertura; sin más deslizamiento.",
  "Exceso frente a BTC: del cierre del día de señal (≈ apertura de entrada) al cierre del día de salida.",
]
limites = [
  "Parámetros (stop, día 28) elegidos por el usuario mirando todo el histórico: la muestra IS no es independiente de ellos.",
  "Un solo token y pocas operaciones: el resultado depende de unas pocas operaciones grandes.",
  "DefiLlama no es point-in-time: el volumen se revisa hacia atrás.",
  "Rentabilidad y drawdown con el 100 % de la equity en un token muy volátil: miden la cuenta, no el edge.",
]
siguiente = "Seguimiento en tiempo real desde el 2026-09-30 con los criterios de refutación del usuario (≥ 10 operaciones)."
```
