---
id: H-007
---

# H007-IS-REAL-007 · Plan anterior al cálculo

Pregunta sobre el mecanismo con el núcleo del NQ ([H007-IS-REAL-006](H007-IS-REAL-006-nq-odplus-btd.md)), **solo IS** 2009-09-27 → 2020-12-31.

## Por qué
BtD apuesta a que el precio se revierte tras una caída. Si la caída es presión de liquidez pasajera (tendencia alcista), debería revertirse más; si es venta informativa y persistente (bajista), menos. En contra: en mercado bajista el market maker corre más riesgo y podría cobrar más prima. El resultado no está decidido de antemano.

## Qué se mide
- **Tendencia:** precio del NQ a las 16:15 de la sesión previa frente a su media de 200 sesiones (filtro estándar, sin elegir). Alcista si está por encima.
- **Evidencia:** en las noches BtD, retorno bruto medio con tendencia alcista menos con bajista, bootstrap por bloques de 5 sesiones.
- **Control:** la misma diferencia en las noches sin BtD. Si la tendencia afecta igual a las dos, lo que se ve es la deriva general del mercado, no la reversión.
- La operativa (equity, ROI) es la de 006: la tendencia solo parte la evidencia, no filtra ni dimensiona.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-007"
variante = "NQ · OD+ BtD × tendencia"
hipotesis = "H-007"
version = "real-is-v3"
pregunta = "Tras una última hora vendedora, ¿rebota más el NQ de 01:30 a 03:30 ET en tendencia alcista que en bajista?"
receta = "estrategias/H-007.md"
cambio = "Misma operativa que 006; la evidencia parte las noches BtD por tendencia (precio 16:15 frente a su media de 200 sesiones), con control en las noches sin BtD."

[datos]
dataset = "NQ 15min"

[tendencia]
hora = "16:15"
sesiones = 200

[sesion]
nombre = "OD+ · BtD"
ventana = ["01:30", "03:30"]
senal = ["15:15", "16:15"]
filtro_senal = "negativa"

[estadistico]
tipo = "media_vs_resto"
particion = "serie"
umbral = 0.0
lados = ["alcista", "bajista"]
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
  "La idea sale del OOS del ES (2022, mercado bajista): se declara; aquí solo se usa IS del NQ.",
  "En 2009-2020 el NQ estuvo casi siempre en tendencia alcista: el grupo bajista es pequeño y su IC, ancho.",
  "Las primeras 200 sesiones no tienen tendencia y quedan fuera de la comparación.",
  "El NQ se mueve muy parecido al ES: no es una muestra independiente.",
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
  "Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).",
]
siguiente = "Interpretar con el usuario; para entender el mecanismo, no para operar. OOS no autorizado."
```
