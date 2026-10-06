---
id: H-007
---

# H007-OOS-REAL-004 · Plan anterior al cálculo

Base: [H007-IS-REAL-006](H007-IS-REAL-006-nq-odplus-btd.md) (NQ · OD+ BtD). Receta: [estrategias/H-007.md](../../estrategias/H-007.md).

## Muestra y autorización
- **OOS 2021-01-01 → 2026-05-28** (último dato del NQ). No queda holdout.
- **Autorización literal del usuario (2026-10-06):** «autorizo usar 2021-2026 del NQ para el núcleo 006 y la variante OD+ en tendencia bajista». Registrada en `conocimiento/H-007.md` y `proteccion.AUTORIZADAS_OOS`.
- El ejecutor exige la especificación de H007-IS-REAL-006 sin cambios (salvo identidad y conclusiones). Si hay tendencia, su media arranca con los precios IS previos.

## Criterios
Sin criterios previos, por decisión del usuario.

## Especificación ejecutable

```toml
id = "H007-OOS-REAL-004"
muestra = "OOS"
base = "H007-IS-REAL-006"
variante = "NQ · OD+ BtD"
hipotesis = "H-007"
version = "real-oos-v1"
pregunta = "¿Rinde el NQ entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?"
receta = "estrategias/H-007.md"
cambio = "OOS 2021-01-01 → 2026-05-28 de H007-IS-REAL-006 (NQ · OD+ BtD), sin cambiar nada de su especificación."

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
  "Parámetros elegidos tras ver el IS (y conociendo el OOS del ES): el OOS mide si sobreviven a esa elección.",
  "Toda la muestra posterior a la IS se usa aquí: no queda holdout del NQ.",
]
siguiente = "Decidir con el usuario a la vista del OOS; no queda holdout del NQ."
```
