---
id: H-007
---

# H007-IS-REAL-006 · Plan anterior al cálculo

Réplica en el NQ del núcleo [H007-IS-REAL-003](../H-007-deriva-nocturna-es/H007-IS-REAL-003-odplus-btd.md) (OD+ · BtD), **sin tocar nada**: misma ventana, misma señal (la última hora del propio NQ), mismo coste por lado en puntos y misma batería. Solo IS 2009-09-27 → 2020-12-31; OOS no autorizado.

- Petición del usuario (2026-10-06): probar el núcleo en otro mercado, «unicamente en IS».
- El NQ no se ha mirado antes de congelar este plan.
- Coste: 1 tick del NQ también es 0,25 puntos; con el NQ a ~2-4 veces el precio del ES, pesa menos en pb.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-006"
variante = "NQ · OD+ BtD"
hipotesis = "H-007"
version = "real-is-v3"
pregunta = "¿Rinde el NQ entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?"
receta = "estrategias/H-007.md"
cambio = "Núcleo de H007-IS-REAL-003 copiado sin cambios en el NQ: réplica en otro mercado, solo IS."

[datos]
dataset = "NQ 15min"

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
  "Núcleo elegido tras ver el IS del ES; en el NQ no se ha mirado nada antes de congelar este plan.",
  "El NQ se mueve muy parecido al ES: no es una muestra independiente.",
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
  "Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).",
]
siguiente = "Decidir con el usuario a la vista del IS; el OOS del NQ no está autorizado."
```
