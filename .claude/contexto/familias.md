# Familias de sistemas

Etiqueta para saber a simple vista de qué tipo de sistema se trata. Cada estrategia lleva **una familia principal**. Lo que decide la familia es **qué determina la dirección y el momento de la posición**, no el mecanismo del paper.

| familia | qué decide la posición | ejemplo |
|---|---|---|
| `momentum` | La dirección de un movimiento de precio **ya ocurrido**, apostando a que **continúa** | signo de la primera media hora → misma dirección en la última |
| `reversion` | La dirección de un movimiento de precio ya ocurrido, apostando a que **se deshace** | tras una caída al cierre, largo esa noche |
| `breakout` | Que el precio **rompa un nivel** (máximo o mínimo de N barras, rango de apertura, banda) | largo si supera el máximo de los 30 primeros minutos |
| `estacionalidad` | El **calendario o el reloj**, sin mirar el precio (día del mes o de la semana, hora del día, mes, víspera de festivo) | largo del último día hábil al tercero del mes siguiente |
| `evento` | Un **evento externo programado** (FOMC, NFP, IPC...) y su calendario | largo la noche previa al FOMC |

## Etiquetas complementarias
- `condicion`: filtro que activa o modula la señal sin cambiar la familia. Valores: `volatilidad`, `volumen`, `evento`, `calendario`, `sentimiento` o `ninguna`. Ejemplo: "momentum intradía más fuerte en días de noticias macro" → `familia: momentum`, `condicion: evento`.
- `horizonte`: `intradia` (se abre y se cierra en la misma sesión), `overnight` (del cierre a la apertura) o `dias` (una o varias sesiones).
- `sentido`: `largo`, `corto` o `largo/corto`.

## Criterios de desempate
- Si la dirección la da el precio y la ventana el reloj (p. ej. primera media hora → última), manda el precio: `momentum` o `reversion`.
- Si la posición es siempre en el mismo sentido y solo cambia *cuándo*, es `estacionalidad` o `evento`, según sea el calendario o un evento externo.
- `estacionalidad` frente a `evento`: los festivos y el cambio de mes son calendario (`estacionalidad`); los anuncios de política monetaria o de datos son `evento`.
- Si ninguna encaja, escribir `familia: sin_encaje` y explicarlo en "Dudas abiertas". No crear familias nuevas por cuenta propia.
