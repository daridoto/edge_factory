---
id: H-PROPIA-003
hipotesis: "[[H-PROPIA-003]]"
enunciado: "En el ES, la última media hora sigue el signo del día desde la apertura (ETF apalancados y cobertura de los dealers de opciones)."
familia: momentum
condicion: signo apertura → 15:30
horizonte: intradía
sentido: largo/corto
instrumento: ES
dataset: ES 15min
coste: "1 tick (0,25 puntos) por operación completa, como H-010"
estado: lista
---

# H-PROPIA-003 · Momentum al cierre por el signo del día

**Familia:** momentum · intradía · largo/corto. Idea propia del usuario (2026-10-09), sin paper propio: `respaldo: [propia]`. Pariente de [[H-073]] (W3124869677) y de [[H-010]]. Hallazgos en [[H-PROPIA-003]] de `conocimiento/`.

## Receta
```
DATOS     ES 15min (hora ET, ts = inicio de barra)
MUESTRA   IS clásica (proteccion.py)
SEÑAL(t)  r_dia = precio 15:30 de t / precio 9:30 de t − 1
ENTRADA   15:30 ET: largo si r_dia > 0; si no, corto (literal del usuario: r_dia = 0 va corto)
SALIDA    16:00 ET (cierre de la barra de 15:45)
MEDIDA    retorno con signo por operación (pb), IC bootstrap; regresión del retorno 15:30 → 16:00 sobre r_dia
```
