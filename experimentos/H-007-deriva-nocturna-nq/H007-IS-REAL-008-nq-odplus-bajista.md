---
id: H-007
---

# H007-IS-REAL-008 · Plan anterior al cálculo

Regla que sale de [H007-IS-REAL-007](H007-IS-REAL-007-nq-btd-tendencia.md): en tendencia bajista rinden más todas las noches y BtD no aporta. Se congela en IS (NQ, 2009-09-27 → 2020-12-31) como base de su OOS.

- **Opera:** OD+ 01:30–03:30 ET todas las noches lun-vie con el precio de las 16:15 de la sesión previa ≤ su media de 200 sesiones. Sin BtD.
- **Evidencia:** retorno bruto medio por operación; resto = noches en tendencia alcista (las de sin tendencia, fuera).

## Especificación ejecutable

```toml
id = "H007-IS-REAL-008"
variante = "NQ · OD+ bajista"
hipotesis = "H-007"
version = "real-is-v3"
pregunta = "¿Rinde el NQ entre las 01:30 y las 03:30 ET cuando está por debajo de su media de 200 sesiones?"
receta = "estrategias/H-007.md"
cambio = "OD+ todas las noches con tendencia bajista (precio 16:15 de la sesión previa ≤ su media de 200 sesiones), sin BtD; congelada en IS antes de su OOS."

[datos]
dataset = "NQ 15min"

[tendencia]
hora = "16:15"
sesiones = 200

[sesion]
nombre = "OD+ · bajista"
ventana = ["01:30", "03:30"]
filtro_serie = { serie_max = 0.0 }

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el precio de las 16:15 de la sesión previa está en o por debajo de su media de 200 sesiones."
salida = "Vender al precio de las 03:30 ET (cierre de la barra de 03:15)."
tamano = "1 unidad del índice (1 USD por punto); referencia al 100 % del capital aparte."
costes = "1 tick (0,25 puntos) por operación completa: 0,125 puntos por lado."

[bootstrap]
unidad = "sesión"
bloque = 5
motivo = "Una operación como máximo por sesión; bloques de 5 sesiones (una semana) conservan la dependencia de corto plazo."

[conclusiones]
supuestos = [
  "Hora ET con horario de verano ya aplicado; ts marca el inicio de la barra.",
  "Retorno simple con precios de operación, no mid quotes: hay rebote bid-ask.",
  "Si falta una barra necesaria (ventana o señal), no se opera esa noche.",
]
limites = [
  "Regla sacada del IS del NQ (H007-IS-REAL-007): sesgo de selección declarado.",
  "Pocas noches bajistas (unas 340 en IS) y las primeras 200 sesiones sin tendencia quedan fuera.",
  "Conocemos el OOS del ES, que se mueve casi igual que el NQ: el OOS del NQ no es del todo a ciegas.",
  "La muestra empieza en 2009; el paper cubre 1998-2020.",
  "La regla de roll anterior a 2022 no está verificada (C6).",
  "Sin corrección por comparaciones múltiples (variantes vistas en el dashboard).",
]
siguiente = "OOS 2021-2026 autorizado por el usuario el 2026-10-06 (H007-OOS-REAL-005)."
```
