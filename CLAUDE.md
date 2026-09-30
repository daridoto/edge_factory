# edge_factory · laboratorio de validación y dashboard

Manual para cualquier IA que trabaje aquí. El estado actual y el siguiente paso están en [ESTADO.md](ESTADO.md).

## Qué es
Recibe hipótesis de trading del repo de papers y las valida con datos históricos, solo in-sample (IS). Su salida la lee el dashboard de `dashboard/`, que tiene su propio manual: [dashboard/CLAUDE.md](dashboard/CLAUDE.md).

```
papers/hipotesis/H-NNN.md ─► triaje ─► receta ─► plan ─► ejecutor ─► resultados/<ID>/
(repo /Users/tommy/dev/quant/papers)                                  resumen.json · equity.csv · operaciones.csv · ficha.md
                                                                              │
                                                                   dashboard/ (solo lee)
```

La IA traduce, implementa y mide; **no puntúa ni recomienda**. El usuario decide en la conversación: no marca columnas ni cambia estados.

## Reglas
1. **Solo IS: 2009-09-27 → 2020-12-31.** OOS y holdout nunca se usan (backtests, métricas, parámetros, conclusiones) sin un mensaje explícito del usuario que autorice ese uso concreto. Pedir implementar, validar o hacer una ficha no lo autoriza. La autorización se registra literalmente y no se extiende a otras variantes. No se crean banderas ni atajos. Los ficheros mixtos se pueden abrir si se filtra IS **antes** de leer precios. Las fechas viven solo en `laboratorio/proteccion.py`, y el contrato rechaza cualquier otra muestra.
2. **`data/` es de solo lectura** y no está en git. Lo que se sabe de los datos está en [.claude/contexto/datos.md](.claude/contexto/datos.md); no hace falta abrirlos.
3. **Sobre resultados, se cita `resultados/indice.csv` o el campo de `resumen.json`.** Si el dato no está ahí, se dice que no consta; no se responde de memoria.
4. **No se crea un `.py` por hipótesis.** Una hipótesis es una especificación TOML dentro de su plan. Si falta una pieza (dataset, ventana, estadístico), se añade de forma genérica a `laboratorio/` con su test.
5. **Lo que se descubre en la conversación** (hallazgos, razonamientos, definiciones, preguntas abiertas) se añade a `conocimiento/` en el momento: una nota por hipótesis o por concepto, con fecha y fuente, sin borrar lo anterior. No va a ESTADO.md.
6. Las fichas son siempre `exploratoria`. Nunca se presentan datos sintéticos como evidencia. La siguiente comprobación se propone, no se ejecuta.
7. Responder en español y de forma concisa.

## Flujo y agentes
| paso | agente (`.claude/agents/`) | entrada → salida | cuándo lanzarlo |
|---|---|---|---|
| 1 | `triaje` | hipótesis → [triaje/indice.md](triaje/indice.md): compatible / proxy / bloqueada según los datos | cuando lleguen hipótesis nuevas del repo de papers |
| 2 | `estratega` | hipótesis → `estrategias/H-NNN.md`: receta en pseudocódigo con citas; `lista` o `bloqueada` | antes de cuantificar una hipótesis sin receta |
| 3 | `investigador` | receta → `experimentos/<ID>.md`: plan con bloque TOML | cuando el usuario elige una hipótesis |
| 4 | `investigador` o en línea | plan → `python -m laboratorio ejecutar` → `resultados/<ID>/` | cuando el usuario da por bueno el plan |

Cada agente arranca sin contexto y relee sus fuentes. Por eso, dentro de una conversación con el usuario suele ser más barato hacer el paso en línea, siguiendo la definición del agente. Los agentes compensan en lotes (triar muchas hipótesis) o en tareas largas. Un agente nuevo solo se registra al iniciar sesión.

Entre pasos se habla con el usuario: qué hipótesis, cómo se cuantifica y si se ejecuta. Modelos de plan: [H001](experimentos/H001-IS-REAL-001.md) (diario) y [H007](experimentos/H007-IS-REAL-001.md) (intradía).

## Comandos
```sh
.venv/bin/python -m laboratorio ejecutar experimentos/<ID>.md   # escribe resultados/<ID>/ (no sobrescribe) e indice.csv
.venv/bin/python -m laboratorio ficha resultados/<ID>           # valida y regenera ficha.md
.venv/bin/python -m laboratorio indice                          # reconstruye resultados/indice.csv
.venv/bin/python -m unittest discover -s tests                  # tests (datos sintéticos)
```
Entorno: `.venv/` con Python 3.11 y pydantic (`requirements.txt`).

## Mapa (leer solo lo que haga falta)
| ruta | qué es |
|---|---|
| `.claude/contexto/` | `datos.md` (catálogo de datos), `convenciones.md` (C1–C13: costes, rolls, tamaño…), `familias.md` |
| `triaje/`, `estrategias/`, `experimentos/` | índice de triaje, recetas y planes |
| `conocimiento/` | hallazgos y definiciones acumulados: `H-NNN.md` por hipótesis y `conceptos/`; enlaces `[[...]]` (bóveda de Obsidian). Leer la nota de una hipótesis antes de trabajar en ella |
| `resultados/` | un directorio por experimento y `indice.csv` con una fila por experimento. Se versiona |
| `laboratorio/` | `ejecutar` (lee el TOML) → `datos` (datasets y periodos) → `catalogo` (ventanas y estadísticos) → `backtest` → `robustez` (batería fija) → `motor` (contabilidad, métricas, E/S) → `presentacion` (ficha). `contratos` (pydantic) y `proteccion` (IS) |
| `esquemas/` | JSON Schema de la salida, exportados desde `contratos.py` (su docstring explica la salida y sus garantías). Es lo que lee el dashboard |
| `dashboard/` | Interfaz de lectura (Vite + JS). Lee `resultados/` a través de `dashboard/public/lab`; no escribe en el lab. Trabajar en él: [dashboard/CLAUDE.md](dashboard/CLAUDE.md) |

## Al empezar y al terminar
- **Al empezar:** leer [ESTADO.md](ESTADO.md) y decir en qué punto estamos y cuál es el siguiente paso.
- **Al terminar un bloque de trabajo:** actualizar ESTADO.md (siguiente paso, estado, pendientes y una línea en el registro). Lo estable va a este fichero; lo que cambia, a ESTADO.md.
