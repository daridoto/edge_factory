---
id: H-007
---

# H007-IS-REAL-003 · Plan anterior al cálculo

Receta: [estrategias/H-007.md](../../estrategias/H-007.md). La señal BtD sale de [estrategias/H-008.md](../../estrategias/H-008.md). Muestra IS 2009-09-27 → 2020-12-31 (C12). OOS no autorizado.

## Qué se congela (núcleo)
- **Ventana OD+** 01:30–03:30 ET (paper, Tabla IX), en lugar de OD 02:00–03:00.
- **BtD (proxy):** solo se opera si el retorno 15:15–16:15 ET de la sesión lun-vie anterior es < 0 (viernes → lunes). El paper usa el RSV, que no tenemos.
- Tamaño 1 unidad (como 001) y referencia al 100 % del capital. Sin VIX y sin filtro de desfase.
- Origen: combinación elegida por el usuario en el dashboard el 2026-10-06 tras ver las variantes de H007-IS-REAL-002. **Se eligió mirando el IS**: hay sesgo de selección y la ficha lo declara.

## Qué se mide
- **Evidencia:** retorno bruto medio por operación (pb/operación) en las noches operadas, con bootstrap por bloques de 5 sesiones.
- **Comparación declarada:** la misma media en las noches que el filtro descarta (BtD ≥ 0 o sin señal) dentro de OD+, y la diferencia, para ver si el filtro separa.
- Referencia exploratoria del dashboard (cálculo independiente del 2026-10-06, al 100 %): 1.246 operaciones, 2,59 pb netos/op, mediana 1,40 pb, WR 52 %, Sharpe 0,91, DD −3,9 %. El lab tiene que reproducirlo o explicar la diferencia.

## Piezas del lab
- `laboratorio/sesion.py` (operativa por sesión sobre la tabla de `variantes.py`), con test. Comprobación: sin filtro y con OD 02:00–03:00 reproduce el libro de H007-IS-REAL-001.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-003"
hipotesis = "H-007"
version = "real-is-v3"
pregunta = "¿Rinde el ES entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?"
receta = "estrategias/H-007.md"
cambio = "Núcleo congelado: ventana OD+ 01:30-03:30 y filtro BtD (proxy de precio); sin VIX."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "OD+ · BtD"
ventana = ["01:30", "03:30"]
senal = ["15:15", "16:15"]
filtro_senal = "negativa"

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0."
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
  "BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.",
  "Si falta una barra necesaria (ventana o señal), no se opera esa noche.",
]
limites = [
  "Ventana y filtro elegidos tras ver el IS en el dashboard (H007-IS-REAL-002): sesgo de selección.",
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
  "Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).",
]
siguiente = "H007-IS-REAL-004: añadir el tamaño por VIX sobre este núcleo. OOS sigue bloqueado."
```
