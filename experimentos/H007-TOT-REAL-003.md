---
id: H-007
---

# H007-TOT-REAL-003 · Plan anterior al cálculo

Base: [H007-IS-REAL-005](H007-IS-REAL-005.md) (OD+ sola). Receta: [estrategias/H-007.md](../estrategias/H-007.md).

## Muestra y autorización
- **Total 2009-09-27 → 2026-05-28** (IS + OOS seguidas, para la vista Total del dashboard). No queda holdout.
- **Autorización literal del usuario (2026-10-06):** «esta perfecto, lo que resta es ahora hacer OOS con la variante con VIX, por mera curiosidad la verdad y tambien del core, es decir unicamente de OD+». Registrada en `conocimiento/H-007.md` y `proteccion.AUTORIZADAS_OOS`.
- El ejecutor exige la especificación de H007-IS-REAL-005 sin cambios (salvo identidad y conclusiones).

## Criterios
Sin criterios previos, por decisión del usuario: se mira el resultado y se decide en la conversación.

## Especificación ejecutable

```toml
id = "H007-TOT-REAL-003"
muestra = "Total"
base = "H007-IS-REAL-005"
hipotesis = "H-007"
version = "real-tot-v1"
pregunta = "¿Rinde el ES entre las 01:30 y las 03:30 ET?"
receta = "estrategias/H-007.md"
cambio = "Total 2009-09-27 → 2026-05-28 de H007-IS-REAL-005 (OD+ sola), sin cambiar nada de su especificación."

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
  "Parámetros elegidos tras ver el IS: el OOS mide si sobreviven a esa elección.",
  "Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.",
]
siguiente = "Decidir con el usuario a la vista del OOS; no queda holdout."
```
