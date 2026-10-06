---
id: H-007
---

# H007-IS-REAL-005 · Plan anterior al cálculo

Receta: [estrategias/H-007.md](../estrategias/H-007.md). Muestra IS 2009-09-27 → 2020-12-31 (C12).

## Qué se congela
- **Solo la ventana OD+** 01:30–03:30 ET (paper, Tabla IX), todas las noches lun-vie: sin BtD, sin VIX y sin filtro de desfase. Tamaño 1 unidad y referencia al 100 %.
- Origen: el usuario pide el OOS de «únicamente OD+» (2026-10-06); se congela antes en IS para tener la base del OOS.

## Qué se mide
- **Evidencia:** retorno bruto medio por operación (pb/operación), bootstrap por bloques de 5 sesiones. Sin grupo de comparación: se opera todas las noches.
- Referencia exploratoria (recálculo del 2026-10-06, al 100 %): 2.903 operaciones, 1,25 pb netos/op, WR 48 %, Sharpe 0,72, DD −8,2 %, ROI +42 %.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-005"
hipotesis = "H-007"
version = "real-is-v4"
pregunta = "¿Rinde el ES entre las 01:30 y las 03:30 ET?"
receta = "estrategias/H-007.md"
cambio = "OD+ 01:30-03:30 sola: sin BtD ni VIX, todas las noches lun-vie."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "OD+"
ventana = ["01:30", "03:30"]

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie."
salida = "Vender al precio de las 03:30 ET (cierre de la barra de 03:15)."
tamano = "1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte."
costes = "1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado."

[bootstrap]
unidad = "sesión"
bloque = 5
motivo = "Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo."

[conclusiones]
supuestos = [
  "Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.",
  "Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.",
  "Si falta una barra necesaria, no se opera esa noche.",
]
limites = [
  "OD+ es la ventana del paper (Tabla IX), vista ya en el dashboard (H007-IS-REAL-002).",
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
  "Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).",
]
siguiente = "OOS de OD+ sola (H007-OOS-REAL-003), autorizado por el usuario el 2026-10-06."
```
