---
id: H-010
---

# H010-IS-REAL-004 · Plan anterior al cálculo

Variante: [H010-IS-REAL-002](H010-IS-REAL-002-r1-apertura.md) (r1 desde las 9:30) operando solo con el VIX de la sesión previa ≥ 20. El paper encuentra el efecto más fuerte con volatilidad alta (W3123013550 p. 11) y en 002 se concentraba en 2009-2013 y 2020. Elegida por el usuario el 2026-10-06 (cuarto intento de H-010). Muestra IS. OOS no autorizado.

## Qué se mide
- **Evidencia:** retorno bruto medio con signo en las sesiones operadas (VIX ≥ 20), pb/operación, bootstrap por bloques de 5 sesiones.
- **Comparación:** la misma media en las sesiones con VIX < 20 (descartadas) y la diferencia.

## Especificación ejecutable

```toml
id = "H010-IS-REAL-004"
hipotesis = "H-010"
variante = "ES · r1 apertura → r13 · VIX ≥ 20"
version = "real-is-v1"
pregunta = "¿Predice el signo del retorno 9:30 → 10:00 ET el de 15:30 → 16:00 ET en el ES cuando el VIX está alto?"
receta = "estrategias/H-010.md"
cambio = "Igual que H010-IS-REAL-002, operando solo si el VIX de la sesión previa es ≥ 20."

[datos]
dataset = "ES 15min"
serie = "VIX 1d"

[sesion]
nombre = "r1 apertura → r13"
ventana = ["15:30", "16:00"]
senal = ["09:30", "10:00"]
senal_dias = [0, 0]
direccion = "senal"
filtro_serie = { serie_min = 20.0 }

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"
prediccion = true

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "A las 15:30 ET (cierre de la barra de 15:15), lun-vie: si el VIX al cierre de la sesión previa es ≥ 20: largo si el retorno 9:30 → 10:00 ET es > 0, corto si no."
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
  "Si falta una barra necesaria o el VIX de la sesión previa, no se opera ese día.",
  "VIX: cierre de la sesión lun-vie anterior (16:15 ET), conocido antes de la entrada.",
]
limites = [
  "Variante elegida tras ver 001-003: el efecto de 002 se concentraba en años de volatilidad alta (sesgo de selección).",
  "Umbral 20 fijado antes de calcular (≈ mediana del VIX, el mismo de H-007); sin barrido de umbrales.",
  "La muestra empieza en 2009: sin la crisis financiera, que concentra el efecto en el paper (R² 0,8 % sin ella).",
  "El coste de 1,2 pb del paper es el spread de SPY, no el del ES.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
]
siguiente = "Decidir con el usuario si H-010 se descarta o se lleva a OOS. OOS bloqueado."
```
