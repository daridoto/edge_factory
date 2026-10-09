---
hipotesis: H-PROPIA-003
nombre: Momentum al cierre por el signo del día (ES)
experimentos: [HPROPIA003-IS-REAL-001]
papers: [propia]
---
# H-PROPIA-003 · La última media hora sigue el signo del día desde la apertura

**Idea** (del usuario, 2026-10-09): «momentum al cierre por los etfs apalancados y los dealers de opciones, el trigger es a las 15:30, si el dia va al alza (precio > apertura de 9:30) entra largo si no entra corto, la entrada es a las 15:30 y la salida a las 16:00». Pariente de [[H-073]] (W3124869677: con entrada desde las 15:00 y sin umbral el efecto es < 0,01 %, p. 24) y de [[H-010]] (señal 9:30 → 10:00, descartada).

## Hallazgos
- **2026-10-09 · IS en ES 2009-2020** (`evidencia` y `robustez` de `resumen.json` de HPROPIA003-IS-REAL-001):
  - 2.810 operaciones (1.515 largos, 1.295 cortos). Retorno bruto medio con signo **+1,61 pb/op**, IC 95 % [+0,47; +2,85]; mediana 0; acierto 49,3 %. Largos +1,54, cortos +1,68.
  - β×100 3,63 (t NW 2,19), R² 0,67 %, R²_OS +0,39 % (desde 2014-09).
  - Por año, entre −0,67 (2017) y +6,18 (2011); negativo en 2009, 2016, 2017 y 2019. Sin cada año, entre +1,16 y +1,83.
  - Neto: +28,5 puntos con 702,5 de costes (1 tick por operación); profit factor 1,01. Al 100 %: ROI +5,3 % (+0,37 % anual), DD −10,7 % (2011-11 → 2018-10, sin recuperar), Sharpe 0,11.
  - Lectura (inferencia): el bruto es positivo con IC fuera de cero y aparece en largos y cortos, el triple que H010-002 (+0,56). Pero 1,6 pb son ≈ 1 tick del ES: el coste se lo come casi entero. Exploratorio, sin veredicto.
- **2026-10-09 · Lectura del usuario:** «salen curvas feisimas siempre, para la variante sin umbrales da un 0.37% anual es una basura y sin embargo para la que tiene umbrales da 119 op lo cual es una basura en cuanto a frecuencia». Sin veredicto todavía.
