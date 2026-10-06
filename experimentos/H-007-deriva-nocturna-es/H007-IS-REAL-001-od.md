---
id: H-007
---

# H007-IS-REAL-001 · Plan anterior al cálculo

Receta: [estrategias/H-007.md](../../estrategias/H-007.md). Muestra IS 2009-09-27 → 2020-12-31 (C12). OOS no autorizado.

## Qué se mide
- **Pregunta:** ¿el ES rinde de media positivo entre las 2:00 y las 3:00 ET, y más que en cualquier otra hora?
- **Estadístico:** retorno medio de la hora 2:00-3:00, en pb (partes A y B de la receta). Referencia del paper: ~1,5 pb/día.
- **Desglose:** retorno medio de cada una de las 23 horas (sin la 17, pausa diaria), para ver en qué puesto queda la de las 2:00.
- **Horas:** retorno de la hora h = close(h:45) / close((h−1):45) − 1. La hora 18 parte de 16:45; el domingo 18 se salta (fin de semana y roll, C6). Si falta una barra, no se interpola.
- **Operativa:** largo 1 unidad del índice de 02:00 a 03:00 ET, con 1 tick (0,25 puntos) por operación completa (0,125 por lado, C1).
- **Robustez:** bootstrap por bloques circulares de 5 días, por año, sin cada año y costes ×2.

## Qué no se hace en este ensayo
- La t y la corrección de Bonferroni de la receta: el intervalo bootstrap cumple ese papel.
- Submuestras por día de la semana y la prueba de las semanas de desfase horario (parte C).
- La variante OD+ (1:30-3:30) y la BtD, que está bloqueada por falta del RSV.

## Especificación ejecutable

```toml
id = "H007-IS-REAL-001"
hipotesis = "H-007"
version = "real-is-v1"
pregunta = "¿Rinde más el ES entre las 2:00 y las 3:00 ET que en cualquier otra hora?"
receta = "estrategias/H-007.md"
cambio = "Primera ejecución real."

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

[conclusiones]
supuestos = [
  "Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.",
  "Retorno simple con precios de operación, no mid quotes como el paper: hay rebote bid-ask.",
  "Precios sin ajustar por roll; la ventana 02:00-03:00 no cruza la barra del domingo 18:00.",
  "Si falta una barra necesaria, no se opera ni se mide esa hora.",
]
limites = [
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6); no afecta a la ventana, sí a horas del domingo.",
  "La simulación usa 1 unidad del índice: la rentabilidad de cuenta no mide el edge.",
  "No se ejecutan la t con Bonferroni, las submuestras por día de la semana ni la prueba de desfase horario.",
]
siguiente = "En IS, submuestras por día de la semana y prueba de las semanas de desfase horario (parte C de la receta). OOS sigue bloqueado."
```
