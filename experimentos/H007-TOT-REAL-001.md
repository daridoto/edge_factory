---
id: H-007
---

# H007-TOT-REAL-001 · Plan anterior al cálculo

Base: [H007-IS-REAL-003](H007-IS-REAL-003.md) (núcleo OD+ · BtD). Receta: [estrategias/H-007.md](../estrategias/H-007.md).

## Muestra y autorización
- **Total 2009-09-27 → 2026-05-28**: IS + OOS seguidas, para la vista Total del dashboard (equity encadenada, bootstrap y años sobre toda la muestra). No queda holdout.
- **Autorización literal del usuario (2026-10-06):** «autorizo usar 2021-2026 primero unicamente con el nucleo 003 para ver como reacciona fuera de muestra el nucleo y ya luego nos planteamos si testeamos o no el nucleo con el vix». Vale solo para H007-IS-REAL-003; el 004 (VIX) no está autorizado.
- El ejecutor exige que la especificación sea idéntica a la de 003 (salvo identidad y conclusiones) y solo admite fechas dentro de la muestra Total de `proteccion.py`.

## Criterios
Sin criterios previos, por decisión del usuario (2026-10-06): se mira el resultado y se decide en la conversación.

## Referencia IS (003)
3,97 pb/op brutos, IC 95 % [2,42; 5,50], 12 de 12 años positivos; descartadas 1,61 pb. Al 100 %: ROI +37,5 %, DD −3,9 %, Sharpe 0,91.

## Especificación ejecutable

```toml
id = "H007-TOT-REAL-001"
muestra = "Total"
base = "H007-IS-REAL-003"
hipotesis = "H-007"
version = "real-tot-v1"
pregunta = "¿Rinde el ES entre las 01:30 y las 03:30 ET tras una última hora vendedora en la sesión previa?"
receta = "estrategias/H-007.md"
cambio = "Total (IS + OOS) 2009-09-27 → 2026-05-28 del núcleo H007-IS-REAL-003, sin cambiar nada de su especificación."

[datos]
dataset = "ES 15min"

[sesion]
nombre = "OD+ · BtD"
ventana = ["01:30", "03:30"]
senal = ["15:15", "16:15"]
filtro_senal = "negativa"

[estadistico]
tipo = "media_ventana"
particion = "filtro"
unidad = "pb/operación"

[operativa]
capital = 10000.0
coste_lado = 0.125
entrada = "Comprar al precio de las 01:30 ET (cierre de la barra de 01:15), lun-vie, si el retorno 15:15-16:15 ET de la sesión previa es < 0."
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
  "BtD es un proxy de precio (retorno 15:15-16:15), no el volumen firmado (RSV) del paper.",
  "Si falta una barra necesaria (ventana o señal), no se opera esa noche.",
]
limites = [
  "Ventana y filtro elegidos tras ver el IS (H007-IS-REAL-002): el OOS mide si sobrevive a esa elección.",
  "Toda la muestra posterior a la IS se usa aquí: no queda holdout para el ES.",
]
siguiente = "Decidir con el usuario si se lleva a OOS el núcleo con VIX (004); necesita su propia autorización."
```
