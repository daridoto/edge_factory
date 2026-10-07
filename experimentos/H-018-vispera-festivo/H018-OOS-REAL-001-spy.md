---
id: H-018
---

# H018-OOS-REAL-001 · Plan anterior al cálculo

Base: [H018-IS-REAL-001](H018-IS-REAL-001-spy.md) (víspera de festivo en SPY). Receta: [estrategias/H-018.md](../../estrategias/H-018.md).

## Muestra y autorización
- **OOS 2021-01-01 → 2026-05-28** (OOS clásico de `proteccion.py`). Juneteenth (desde 2022) no es uno de los 8 festivos: su víspera cuenta como resto.
- **Autorización literal del usuario (2026-10-07):** «cambiale el nombre y sometelo a OOS te doy la autorizacion», y en la pregunta de qué experimento, «SPY víspera (001)». Vale solo para la base H018-IS-REAL-001: planes H018-OOS-REAL-001 y H018-TOT-REAL-001. H018-IS-REAL-002 (ES por horas) no está autorizado.
- El ejecutor exige que la especificación sea idéntica a la de 001 (salvo identidad y conclusiones). Métricas de cuenta en la referencia al 100 %.

## Criterios
Sin criterios previos fijados por el usuario: se mira el resultado y se decide en la conversación.

## Referencia IS (001)
+3,42 pb/día (víspera − resto), IC 95 % [−9,03; 15,77], 6/12 años positivos.

## Especificación ejecutable

```toml
id = "H018-OOS-REAL-001"
muestra = "OOS"
base = "H018-IS-REAL-001"
hipotesis = "H-018"
variante = "SPY · víspera"
version = "real-oos-v1"
pregunta = "¿Rinde más SPY en la sesión previa a un festivo que en el resto de sesiones?"
receta = "estrategias/H-018.md"
cambio = "OOS 2021-01-01 → 2026-05-28 de H018-IS-REAL-001, sin cambiar nada de su especificación."

[datos]
dataset = "SPY 1d"
periodo = "1d"

[ventana]
tipo = "festivos"
valores = ["ano_nuevo", "presidentes", "viernes_santo", "memorial", "independencia", "trabajo", "accion_gracias", "navidad"]
nombre = "víspera"

[estadistico]
tipo = "media_vs_resto"
desglose = true

[operativa]
capital = 10000.0
coste_lado = 0.01
entrada = "Comprar al cierre de la sesión anterior a la víspera."
salida = "Vender al cierre de la víspera."
tamano = "1 acción por víspera; referencia al 100 % del capital aparte."
costes = "0,01 USD por acción y lado; sin comisión adicional ni impacto."

[bootstrap]
unidad = "mes"
bloque = 12
motivo = "Cada festivo cae una vez al año; bloques de 12 meses conservan un año completo de festivos."

[conclusiones]
supuestos = [
  "Víspera = última sesión antes de un cierre observado de NYSE por uno de los 8 festivos (reglas en festivos.py).",
  "Año Nuevo en sábado (2011) no es cierre: ese año no hay víspera de Año Nuevo.",
  "Retornos close-to-close ajustados por dividendos, antes de costes.",
]
limites = [
  "Unas 89 vísperas en la IS (10-12 por festivo): el intervalo será ancho y el desglose por festivo, ruidoso.",
  "Solapa con el cambio de mes (H-001) en Labor Day, Navidad y Año Nuevo.",
  "El intervalo no corrige la exploración previa de esta hipótesis en la literatura.",
]
siguiente = "Decidir con el usuario qué hacer con H-018 a la vista del OOS."
```
