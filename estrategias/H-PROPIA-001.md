---
id: H-PROPIA-001
hipotesis: "[[H-PROPIA-001]]"
enunciado: "En RAY (diario), cuando el volumen de Raydium dobla su nivel normal, el token rinde de media claramente positivo en los 28 días siguientes."
familia: evento
condicion: volumen del DEX
horizonte: semanas
sentido: largo
instrumento: RAY
dataset: RAY 1d + Raydium volumen 1d (DefiLlama)
coste: "0,2 % del nocional por lado (lo fija el usuario)"
estado: lista
---

# H-PROPIA-001 · RAY largo 28 días cuando el volumen de Raydium dobla su nivel normal

**Familia:** evento · volumen del DEX · semanas · largo. La hipótesis es propia del usuario y la pegó en la conversación del 2026-09-30. Hallazgos y autorización de muestra: [[H-PROPIA-001]] en `conocimiento/`.

## Contexto
Estudio de eventos del usuario sobre 23 tokens de DEX (Binance + DefiLlama): el volumen anómalo es un fenómeno de sector, y el DEX principal de cada cadena es el que más se beneficia. RAY es el DEX principal de Solana y tiene recompras ligadas al volumen (12 % de las fees). No hay paper: `respaldo: [propia]`.

## Receta
```
DATOS  RAY 1d · Binance spot, velas UTC (open, low, close)
       Raydium volumen 1d · DefiLlama (celdas vacías = sin dato; no es point-in-time)
       BTC 1d · btc_close de RAY_diario.csv, solo como referencia
MUESTRA  IS cripto 2021-08-10 → 2026-09-29 (proteccion.MUESTRAS); la simulación empieza con el primer dato de volumen
PARÁMETROS (fijados por el usuario)
    corta = 7 · larga = 90 días con dato (medianas) · umbral = 2
    tenencia = 28 días naturales desde la señal · stop = −25 % · enfriamiento = 28 días
    tamaño = 100 % de la equity, una operación a la vez · coste = 0,2 % por lado

SEÑAL(t) ← mediana(vol últimos 7 datos) / mediana(vol últimos 90 datos) ≥ 2
           (sin 90 datos no hay señal; tras una señal usada, la siguiente vale desde t + 28)
ENTRADA  apertura de la primera vela posterior a t
SALIDA   si abre ≤ entrada × 0,75 → apertura; si el mínimo ≤ entrada × 0,75 → al stop;
         si no, cierre de la última vela ≤ t + 28. Si t + 28 cae fuera de la muestra, no se opera.
MEDIDA   retorno neto por operación = salida·(1−c) / (entrada·(1+c)) − 1; media, mediana, t
         exceso frente a BTC (cierre de t → cierre del día de salida)
         placebo: mismo nº de operaciones en días aleatorios separados ≥ 28 días, 2000 sorteos
```
