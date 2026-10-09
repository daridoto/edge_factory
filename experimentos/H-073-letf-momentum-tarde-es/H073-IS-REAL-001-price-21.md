---
id: H-073
---

# H073-IS-REAL-001 · Plan anterior al cálculo

Regla «price-21» del paper W3124869677 (pp. 24-26), receta [estrategias/H-073.md](../../estrategias/H-073.md): si el ES acumula al menos ±2 % desde el cierre anterior hasta las 14:45 ET, entra en esa dirección y sale al cierre. Pedida por el usuario el 2026-10-09 junto a su propia regla ([HPROPIA003-IS-REAL-001](../H-PROPIA-003-momentum-cierre-es/HPROPIA003-IS-REAL-001-dia-apertura.md)). Muestra IS. OOS no autorizado.

## Especificación ejecutable

```toml
id = "H073-IS-REAL-001"
hipotesis = "H-073"
variante = "ES · price-21 (±2 % a las 14:45)"
version = "real-is-v1"
pregunta = "¿Sigue el ES de 14:45 al cierre el signo de un movimiento ≥ |2 %| desde el cierre anterior?"
receta = "estrategias/H-073.md"
cambio = "Primer ensayo: regla price-21 del paper."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "price-21"
ventana = ["14:45", "16:00"]
senal = ["16:00", "14:45"]
senal_dias = [-1, 0]
direccion = "senal"
umbral_senal = 0.02

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"
prediccion = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "A las 14:45 ET (cierre de la barra de 14:30), lun-vie, si |precio 14:45 / cierre 16:00 previo − 1| ≥ 2 %: largo si > 0, corto si < 0."
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
  "ES en lugar de la cesta del S&P 500 (C8); cierre previo = cierre de la barra de 15:45 de la sesión lun-vie anterior.",
  "Resto de la evidencia: sesiones con |señal| < 2 %, con la misma dirección por signo (contraste de refutación del paper).",
  "Si falta una barra necesaria o la señal cruza un roll, no se opera ese día.",
]
limites = [
  "Pocas operaciones esperadas (el paper: 128 días en 2006-2011, con la crisis); la IS empieza en 2009.",
  "El paper no incluye costes; aquí 1 tick por operación.",
  "Solo la ventana 21; 19 y 20 sin probar. La regla de roll anterior a 2022 no está verificada (C6).",
]
siguiente = "Comparar con HPROPIA003-IS-REAL-001. OOS bloqueado."
```
