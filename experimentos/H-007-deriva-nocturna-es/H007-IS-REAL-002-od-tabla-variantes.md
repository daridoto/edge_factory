---
id: H-007
---

# H007-IS-REAL-002 · Plan anterior al cálculo

Receta: [estrategias/H-007.md](../../estrategias/H-007.md). La señal BtD sale de [estrategias/H-008.md](../../estrategias/H-008.md). Muestra IS 2009-09-27 → 2020-12-31 (C12). OOS no autorizado.

## Qué cambia frente a H007-IS-REAL-001
- **La evidencia, la operativa y la batería son las mismas** (OD 02:00–03:00, 1 unidad, 1 tick). La base tiene que reproducir el 001; el motor lo exige operación a operación.
- **Se añade `variantes.csv`**: una fila por noche y ventana con lo necesario para combinar variantes en vivo en el dashboard (toggles), sin un experimento por combinación:
  - **Ventanas:** OD 02:00–03:00 (base) y OD+ 01:30–03:30 (paper, Tabla IX).
  - **Señal BtD (proxy):** retorno 15:15–16:15 ET de la sesión lun-vie anterior (viernes → lunes). El paper usa el RSV tick a tick, que no tenemos (H-008, decisión 1).
  - **VIX:** cierre diario de la sesión anterior (16:15 ET), para filtrar por umbral o dimensionar.
  - **Desfase:** si la noche cae entre los cambios de hora de EE. UU. y Europa.
- Origen: diseño acordado con el usuario el 2026-10-05 sobre un prototipo (ver `conocimiento/H-007.md`).

## Qué no se hace
- Las combinaciones del dashboard **no** pasan por la batería del lab: son exploratorias, sin bootstrap. La que interese se congela después como experimento propio.
- Ni OOS ni elección de parámetros: el umbral del VIX y el multiplicador de tamaño los mueve el usuario en el dashboard.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-002"
hipotesis = "H-007"
version = "real-is-v2"
pregunta = "¿Rinde más el ES entre las 2:00 y las 3:00 ET que en cualquier otra hora?"
receta = "estrategias/H-007.md"
cambio = "Misma evidencia que 001 y tabla de variantes por noche (OD+, BtD con proxy, VIX, desfase) para combinar en el dashboard."

[datos]
dataset = "ES 15min"
periodo = "1h"
excluir_horas = [17]

[ventana]
tipo = "hora"
valores = [2]
nombre = "02:00-03:00"

[estadistico]
tipo = "media_ventana"
desglose = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al cierre de la barra de 01:45 ET (precio de las 02:00), de lunes a viernes."
salida = "Vender al cierre de la barra de 02:45 ET (precio de las 03:00)."
tamano = "1 unidad del índice (1 USD por punto, no el multiplicador de 50 USD del contrato); sin apalancamiento."
costes = "1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado."

[bootstrap]
unidad = "día"
bloque = 5
motivo = "Observaciones diarias; bloques de 5 días (una semana) conservan la dependencia de corto plazo."

[variantes]
ventanas = { OD = ["02:00", "03:00"], "OD+" = ["01:30", "03:30"] }
base = "OD"
senal = ["15:15", "16:15"]
serie = "VIX 1d"

[conclusiones]
supuestos = [
  "Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.",
  "Retorno simple con precios de operación, no mid quotes como el paper: hay rebote bid-ask.",
  "Precios sin ajustar por roll; la ventana 02:00-03:00 no cruza la barra del domingo 18:00.",
  "Si falta una barra necesaria, no se opera ni se mide esa hora.",
  "Variantes: la señal BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado del paper.",
]
limites = [
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6); no afecta a la ventana, sí a horas del domingo.",
  "La simulación usa 1 unidad del índice: la rentabilidad de cuenta no mide el edge.",
  "No se ejecutan la t con Bonferroni, las submuestras por día de la semana ni la prueba de desfase horario.",
  "Las combinaciones de variantes del dashboard no tienen bootstrap ni batería de robustez.",
]
siguiente = "Congelar como experimento propio la combinación de variantes que el usuario elija y pasarla por la batería en IS. OOS sigue bloqueado."
```
