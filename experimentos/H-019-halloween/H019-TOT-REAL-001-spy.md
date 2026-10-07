---
id: H-019
---

# H019-TOT-REAL-001 · Plan anterior al cálculo

Base: [H019-IS-REAL-001](H019-IS-REAL-001-spy.md) (Halloween en SPY). Receta: [estrategias/H-019.md](../../estrategias/H-019.md).

## Muestra y autorización
- **Total 2009-09-27 → 2026-05-28**: IS + OOS seguidas, para la vista Total del dashboard.
- **Autorización literal del usuario (2026-10-07):** «pasemos SPY a OOS, te doy mi autorizacion» (H-019 en SPY). Vale solo para la base H019-IS-REAL-001 (SPY): planes H019-OOS-REAL-001 y H019-TOT-REAL-001. QQQ, IWM y DIA no están autorizados.
- El ejecutor exige que la especificación sea idéntica a la de 001 (salvo identidad y conclusiones). Métricas de cuenta en la referencia al 100 %.

## Criterios
Sin criterios previos fijados por el usuario: se mira el resultado y se decide en la conversación.

## Referencia IS (001)
+4,45 pb/día (invierno − verano), IC 95 % [−0,57; 9,81], 8/12 años positivos.

## Especificación ejecutable

```toml
id = "H019-TOT-REAL-001"
muestra = "Total"
base = "H019-IS-REAL-001"
hipotesis = "H-019"
variante = "SPY · Nov-Abr"
version = "real-tot-v1"
pregunta = "¿Rinde más SPY de noviembre a abril que de mayo a octubre?"
receta = "estrategias/H-019.md"
cambio = "Total 2009-09-27 → 2026-05-28 (IS + OOS) de H019-IS-REAL-001, sin cambiar nada de su especificación."

[datos]
dataset = "SPY 1d"
periodo = "1d"

[ventana]
tipo = "meses"
valores = [11, 12, 1, 2, 3, 4]
nombre = "Nov-Abr"

[estadistico]
tipo = "media_vs_resto"

[operativa]
capital = 10000.0
coste_lado = 0.01
entrada = "Comprar al cierre de la última sesión de octubre."
salida = "Vender al cierre de la última sesión de abril (o de la muestra)."
tamano = "1 acción por semestre; referencia al 100 % del capital aparte."
costes = "0,01 USD por acción y lado; sin comisión adicional ni impacto."

[bootstrap]
unidad = "mes"
bloque = 12
motivo = "La hipótesis es semestral; bloques de 12 meses conservan un año de dependencia."

[conclusiones]
supuestos = [
  "Invierno = sesiones de noviembre a abril; verano = mayo a octubre.",
  "Retornos close-to-close ajustados por dividendos, antes de costes.",
  "El invierno 2020-21 queda cortado el 31-12-2020: cuenta en el estadístico y la operación se cierra ahí.",
]
limites = [
  "Solo 11 inviernos completos en la IS: el intervalo será ancho.",
  "El intervalo no corrige la exploración previa de esta hipótesis en la literatura.",
  "Sin comisiones adicionales, impacto ni dividendos fuera de posición.",
]
siguiente = "Decidir con el usuario qué hacer con H-019 a la vista del OOS."
```
