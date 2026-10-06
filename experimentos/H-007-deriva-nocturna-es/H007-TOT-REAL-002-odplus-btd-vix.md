---
id: H-007
---

# H007-TOT-REAL-002 · Plan anterior al cálculo

Base: [H007-IS-REAL-004](H007-IS-REAL-004-odplus-btd-vix.md) (OD+ · BtD · VIX > 20 ×2). Receta: [estrategias/H-007.md](../../estrategias/H-007.md).

## Muestra y autorización
- **Total 2009-09-27 → 2026-05-28** (IS + OOS seguidas, para la vista Total del dashboard). No queda holdout.
- **Autorización literal del usuario (2026-10-06):** «esta perfecto, lo que resta es ahora hacer OOS con la variante con VIX, por mera curiosidad la verdad y tambien del core, es decir unicamente de OD+». Registrada en `conocimiento/H-007.md` y `proteccion.AUTORIZADAS_OOS`.
- El ejecutor exige la especificación de H007-IS-REAL-004 sin cambios (salvo identidad y conclusiones).

## Criterios
Sin criterios previos, por decisión del usuario: se mira el resultado y se decide en la conversación.

## Especificación ejecutable

```toml
id = "H007-TOT-REAL-002"
muestra = "Total"
base = "H007-IS-REAL-004"
hipotesis = "H-007"
version = "real-tot-v1"
pregunta = "Dentro del núcleo OD+ · BtD, ¿rinde más el ES las noches con VIX previo > 20?"
receta = "estrategias/H-007.md"
cambio = "Total 2009-09-27 → 2026-05-28 de H007-IS-REAL-004 (OD+ · BtD · VIX > 20 ×2), sin cambiar nada de su especificación."

[datos]
dataset = "ES 15min"
serie = "VIX 1d"

[sesion]
nombre = "OD+ · BtD · VIX>20 ×2"
ventana = ["01:30", "03:30"]
senal = ["15:15", "16:15"]
filtro_senal = "negativa"

[tamano]
umbral = 20.0
multiplicador = 2.0

[estadistico]
tipo = "media_vs_resto"
particion = "tamano"
unidad = "pb/operación"

[sensibilidad]
umbrales = [15.0, 20.0, 25.0, 30.0]
multiplicadores = [1.5, 2.0, 3.0]

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET, lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0."
salida = "Vender al precio de las 03:30 ET."
tamano = "1 unidad del índice; 2 unidades si el VIX al cierre de la sesión previa es > 20. Referencia al 100 % del capital (×2 = 200 %) aparte."
costes = "1 tick (0,25 puntos) por operación completa y unidad: 0,125 puntos por lado."

[bootstrap]
unidad = "sesión"
bloque = 5
motivo = "Una operación como máximo por sesión; bloques de 5 sesiones conservan la dependencia de corto plazo y los regímenes de VIX."

[conclusiones]
supuestos = [
  "Los de H007-IS-REAL-003.",
  "VIX: cierre diario de la sesión previa (16:15 ET), conocido antes de la entrada.",
  "Al 100 % con ×2 la exposición es del 200 % del capital (apalancamiento).",
]
limites = [
  "Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.",
  "Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.",
]
siguiente = "Decidir con el usuario a la vista del OOS; no queda holdout."
```
