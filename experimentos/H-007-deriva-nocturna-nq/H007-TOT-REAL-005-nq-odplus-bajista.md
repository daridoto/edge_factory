---
id: H-007
---

# H007-TOT-REAL-005 · Plan anterior al cálculo

Base: [H007-IS-REAL-008](H007-IS-REAL-008-nq-odplus-bajista.md) (NQ · OD+ bajista). Receta: [estrategias/H-007.md](../../estrategias/H-007.md).

## Muestra y autorización
- **Total 2009-09-27 → 2026-05-28** (IS + OOS seguidas, para la vista Total del dashboard). No queda holdout.
- **Autorización literal del usuario (2026-10-06):** «autorizo usar 2021-2026 del NQ para el núcleo 006 y la variante OD+ en tendencia bajista». Registrada en `conocimiento/H-007.md` y `proteccion.AUTORIZADAS_OOS`.
- El ejecutor exige la especificación de H007-IS-REAL-008 sin cambios (salvo identidad y conclusiones). Si hay tendencia, su media arranca con los precios IS previos.

## Criterios
Sin criterios previos, por decisión del usuario.

## Especificación ejecutable

```toml
id = "H007-TOT-REAL-005"
muestra = "Total"
base = "H007-IS-REAL-008"
variante = "NQ · OD+ bajista"
hipotesis = "H-007"
version = "real-tot-v1"
pregunta = "¿Rinde el NQ entre las 01:30 y las 03:30 ET cuando está por debajo de su media de 200 sesiones?"
receta = "estrategias/H-007.md"
cambio = "Total 2009-09-27 → 2026-05-28 de H007-IS-REAL-008 (NQ · OD+ bajista), sin cambiar nada de su especificación."

[datos]
dataset = "NQ 15min"

[tendencia]
hora = "16:15"
sesiones = 200

[sesion]
nombre = "OD+ · bajista"
ventana = ["01:30", "03:30"]
filtro_serie = { serie_max = 0.0 }

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el precio de las 16:15 de la sesión previa está en o por debajo de su media de 200 sesiones."
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
  "Si falta una barra necesaria (ventana o señal), no se opera esa noche.",
]
limites = [
  "Parámetros elegidos tras ver el IS (y conociendo el OOS del ES): el OOS mide si sobreviven a esa elección.",
  "Toda la muestra posterior a la IS se usa aquí: no queda holdout del NQ.",
]
siguiente = "Decidir con el usuario a la vista del OOS; no queda holdout del NQ."
```
