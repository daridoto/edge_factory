---
id: H-010
---

# H010-IS-REAL-002 · Plan anterior al cálculo

Variante de la receta ([estrategias/H-010.md](../../estrategias/H-010.md)): r1 desde la apertura de las 9:30 ET, sin el overnight (W2990924896 p. 10). Todo lo demás, igual que [H010-IS-REAL-001](H010-IS-REAL-001-r1-r13.md). Elegida por el usuario el 2026-10-06 tras ver 001 (segundo intento de H-010). Muestra IS. OOS no autorizado.

## Especificación ejecutable

```toml
id = "H010-IS-REAL-002"
hipotesis = "H-010"
variante = "ES · r1 apertura → r13"
version = "real-is-v1"
pregunta = "¿Predice el signo del retorno 9:30 → 10:00 ET el de 15:30 → 16:00 ET en el ES?"
receta = "estrategias/H-010.md"
cambio = "Igual que H010-IS-REAL-001, con r1 desde la apertura de las 9:30 (sin overnight)."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "r1 apertura → r13"
ventana = ["15:30", "16:00"]
senal = ["09:30", "10:00"]
senal_dias = [0, 0]
direccion = "senal"

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"
prediccion = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si el retorno 9:30 → 10:00 ET es > 0, corto si no."
salida = "A las 16:00 ET (cierre de la barra de 15:45)."
tamano = "1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte."
costes = "1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado."

[bootstrap]
unidad = "sesión"
bloque = 5
motivo = "Una operación por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo."

[conclusiones]
supuestos = [
  "Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.",
  "ES en lugar de SPY (C8); retorno simple con precios de operación, con rebote bid-ask.",
  "r1 = precio 10:00 / precio 9:30 − 1 (cierres de las barras de 09:45 y 09:15), sin overnight.",
  "Si falta una barra necesaria, no se opera ese día.",
]
limites = [
  "La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).",
  "El coste de 1,2 pb del paper es el spread de SPY, no el del ES.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
]
siguiente = "Señal combinada r1 + r12 y filtro por volatilidad (VIX), en IS. OOS bloqueado."
```
