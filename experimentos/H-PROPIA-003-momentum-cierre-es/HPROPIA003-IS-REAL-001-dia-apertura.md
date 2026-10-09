---
id: H-PROPIA-003
---

# HPROPIA003-IS-REAL-001 · Plan anterior al cálculo

Regla del usuario (2026-10-09), receta [estrategias/H-PROPIA-003.md](../../estrategias/H-PROPIA-003.md): a las 15:30 ET, largo si el ES está por encima de la apertura de las 9:30 y corto si no; salida a las 16:00. Se ejecuta a la vez que [H073-IS-REAL-001](../H-073-letf-momentum-tarde-es/H073-IS-REAL-001-price-21.md), la regla del paper. Muestra IS. OOS no autorizado.

## Especificación ejecutable

```toml
id = "HPROPIA003-IS-REAL-001"
hipotesis = "H-PROPIA-003"
variante = "ES · día desde apertura → 15:30-16:00"
version = "real-is-v1"
pregunta = "¿Sigue el ES de 15:30 a 16:00 ET el signo del movimiento 9:30 → 15:30 del mismo día?"
receta = "estrategias/H-PROPIA-003.md"
cambio = "Primer ensayo de la regla del usuario."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "día apertura → 15:30-16:00"
ventana = ["15:30", "16:00"]
senal = ["09:30", "15:30"]
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
entrada = "A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si precio 15:30 > precio 9:30, corto si no."
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
  "Apertura = cierre de la barra de 09:15 (precio a las 9:30); 15:30 = cierre de la barra de 15:15.",
  "Retorno simple con precios de operación, con rebote bid-ask; señal = 0 va corta (literal del usuario).",
  "Si falta una barra necesaria, no se opera ese día.",
]
limites = [
  "Sin dato de exposición de los ETF apalancados ni de gamma de los dealers: la señal es solo el precio.",
  "W3124869677 no encuentra efecto con entrada a partir de las 15:00 sin umbral de ±2 %.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
]
siguiente = "Comparar con H073-IS-REAL-001 (regla del paper). OOS bloqueado."
```
