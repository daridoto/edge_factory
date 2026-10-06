---
id: H-007
---

# H007-IS-REAL-004 · Plan anterior al cálculo

Receta: [estrategias/H-007.md](../estrategias/H-007.md). Núcleo: [H007-IS-REAL-003](H007-IS-REAL-003.md). Muestra IS 2009-09-27 → 2020-12-31 (C12). OOS no autorizado.

## Qué se congela
- **El núcleo de 003 sin cambios:** OD+ 01:30–03:30 ET y BtD (proxy).
- **Tamaño ×2 si el VIX al cierre de la sesión previa es > 20**; ×1 en el resto. Se operan las mismas noches que en 003.
- Origen: combinación elegida por el usuario en el dashboard el 2026-10-06. **El 20 y el ×2 se eligieron mirando el IS**: sesgo de selección declarado.

## Qué se mide
- **Evidencia (lo que aporta el VIX):** diferencia de retorno bruto medio por operación entre las noches con VIX > 20 y las de VIX ≤ 20 (pb/operación), con bootstrap por bloques de 5 sesiones. Si el intervalo incluye cero, el ×2 solo añade riesgo.
- **Contabilidad:** la del tamaño ×2 (ROI, DD, Sharpe) frente a 003.
- **Sensibilidad (se informa, no se elige):** la diferencia para umbrales 15 / 20 / 25 / 30 y la contabilidad para k ×1,5 / ×2 / ×3.
- Referencia exploratoria del dashboard (2026-10-06, al 100 %): 1.246 operaciones, 4,91 pb netos/op, WR 52 %, Sharpe 0,95, DD −7,0 %, ROI +82 %.

## Piezas del lab
- `laboratorio/sesion.py` (tamaño por umbral de `[datos].serie`, partición `tamano`) y `sensibilidad` en `resumen.json` (esquema 2.3) y en la ficha, con test. Las noches sin dato de VIX operan ×1 y quedan fuera de la comparación.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-004"
hipotesis = "H-007"
version = "real-is-v3"
pregunta = "Dentro del núcleo OD+ · BtD, ¿rinde más el ES las noches con VIX previo > 20?"
receta = "estrategias/H-007.md"
cambio = "Núcleo de 003 con tamaño ×2 si el VIX de la sesión previa supera 20; sensibilidad de umbral y multiplicador."

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
  "Umbral y multiplicador elegidos tras ver el IS en el dashboard: sesgo de selección; la sensibilidad lo acota, no lo elimina.",
  "Las noches con VIX > 20 se concentran en pocos regímenes (2010-2012, 2015, 2018, 2020): pocas unidades independientes.",
  "Los de H007-IS-REAL-003.",
]
siguiente = "Decidir con el usuario si el VIX se mantiene; OOS sigue bloqueado."
```
