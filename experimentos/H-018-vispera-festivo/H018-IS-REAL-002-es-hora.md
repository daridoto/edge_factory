---
id: H-018
---

# H018-IS-REAL-002 · Plan anterior al cálculo

Receta: [estrategias/H-018.md](../../estrategias/H-018.md). Muestra IS 2009-09-27 → 2020-12-31. OOS no autorizado. Huella de mecanismo, no validación: la IS de H-018 ya está vista (H018-IS-REAL-001).

## Qué se mide
- **Pregunta de mecanismo:** si la subida de la víspera viene de cortos que recompran antes del cierre (Fabozzi et al., 1994, citado en W2943226912), debería concentrarse en la última hora de la sesión de contado.
- **Estadístico:** en las vísperas de los 8 festivos, retorno medio del ES de 15:00 a 16:00 ET menos el de las demás horas de 0:00 a 15:00 del mismo día, en pb/hora; desglose por hora.
- **Comparación:** la hora 15:00-16:00 en todos los días rinde +0,25 pb/hora (desglose de H007-IS-REAL-001).
- **Operativa:** largo 1 unidad del índice de 15:00 a 16:00 ET en cada víspera; coste 1 tick por operación.
- **Robustez:** batería fija; bootstrap por día (las vísperas distan semanas entre sí).

## Piezas nuevas del lab (genéricas, con test)
- `solo_vispera` en `[ventana]`: deja solo los periodos de las vísperas (calendario por regla, `festivos.vispera_regla`, porque el ES cotiza en algunos festivos).

## Especificación ejecutable

```toml
id = "H018-IS-REAL-002"
hipotesis = "H-018"
variante = "ES · última hora de la víspera"
version = "real-is-v1"
pregunta = "¿Se concentra la subida de la víspera de festivo en la última hora de la sesión (15:00-16:00 ET)?"
receta = "estrategias/H-018.md"
cambio = "Huella del cierre de cortos: perfil horario del ES en las vísperas de H018-IS-REAL-001."

[datos]
dataset = "ES 15min"
periodo = "1h"
excluir_horas = [16, 17, 18, 19, 20, 21, 22, 23]

[ventana]
tipo = "hora"
valores = [15]
nombre = "15:00-16:00"
solo_vispera = ["ano_nuevo", "presidentes", "viernes_santo", "memorial", "independencia", "trabajo", "accion_gracias", "navidad"]

[estadistico]
tipo = "media_vs_resto"
desglose = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al cierre de la barra de 14:45 ET (precio de las 15:00) de cada víspera."
salida = "Vender al cierre de la barra de 15:45 ET (precio de las 16:00)."
tamano = "1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte."
costes = "1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado."

[bootstrap]
unidad = "día"
bloque = 1
motivo = "Las vísperas distan semanas entre sí: sin dependencia que conservar entre días."

[conclusiones]
supuestos = [
  "Víspera por regla (8 festivos de NYSE); hora ET con horario de verano; ts marca el inicio de la barra.",
  "Resto = horas 0:00-15:00 del mismo día de víspera; la tarde-noche del día anterior (16:00-24:00) no entra.",
  "Precios sin ajustar por roll; la ventana no cruza la barra del domingo.",
]
limites = [
  "Los días de cierre anticipado (13:00 ET: Nochebuena y a veces 3 de julio) no tienen barra de 15:00: esas vísperas solo cuentan en el resto.",
  "Unas 89 vísperas: el intervalo será ancho.",
  "Es una huella indirecta: sin datos de posiciones cortas no se distingue el cierre de cortos de otros compradores de fin de sesión.",
]
siguiente = "Según el resultado: comparar con la duración del cierre (festivos de fin de semana largo frente a uno), en IS."
```
