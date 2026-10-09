---
id: H-073
---

# H073-IS-REAL-003 · Plan anterior al cálculo

Regresión continua en lugar del umbral de ±2 % (propuesta del usuario, 2026-10-09): retorno de la última media hora (15:30 → 16:00 ET) sobre el movimiento del día (cierre anterior → 15:30, el retorno diario que rebalancean los ETF apalancados) y su interacción señal·|señal|. Todas las sesiones, sin umbral. En el NQ no se ha mirado antes esta pregunta (solo H-007, otra ventana). Fijado antes de calcular: el mecanismo predice β1 ≥ 0 y β2 ≥ 0; se miran signo y t de Newey-West de ambos, R² y R²_OS. Mismo plan en ES (002) y NQ (003). Muestra IS. OOS no autorizado.

## Especificación ejecutable

```toml
id = "H073-IS-REAL-003"
hipotesis = "H-073"
variante = "NQ · regresión día → 15:30-16:00"
version = "real-is-v1"
pregunta = "¿Predice el movimiento del día (cierre anterior → 15:30 ET), y más cuanto mayor es, el retorno de 15:30 a 16:00 en el NQ?"
receta = "estrategias/H-073.md"
cambio = "Umbral de ±2 % sustituido por regresión continua con interacción señal·|señal|; ventana 15:30 → 16:00."

[datos]
dataset = "NQ 15min"

[sesion]
nombre = "día → 15:30-16:00"
ventana = ["15:30", "16:00"]
senal = ["16:00", "15:30"]
senal_dias = [-1, 0]
direccion = "senal"

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"
prediccion = true
interaccion = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "A las 15:30 ET (cierre de la barra de 15:15), lun-vie: largo si precio 15:30 / cierre 16:00 previo > 1, corto si no."
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
  "Señal = precio 15:30 / cierre 16:00 de la sesión lun-vie anterior − 1; regresión en todas las sesiones con señal y precios.",
  "Modelo: r(15:30→16:00) = α + β1·señal + β2·señal·|señal|; pendiente marginal β1 + 2·β2·|señal|.",
  "La operativa (largo/corto por signo) solo traduce la señal a dinero; la prueba es la regresión.",
  "Si falta una barra necesaria o la señal cruza un roll, no se opera ese día.",
]
limites = [
  "Sin datos de exposición de los ETF apalancados: la señal es solo el precio.",
  "ES y NQ están muy correlacionados: no son pruebas independientes. RTY no tiene datos intradía.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
]
siguiente = "Comparar ES y NQ. OOS bloqueado."
```
