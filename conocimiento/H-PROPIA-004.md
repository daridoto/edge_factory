---
hipotesis: H-PROPIA-004
nombre: Reversión tras día grande (5 índices)
experimentos: []
papers: [propia]
---
# H-PROPIA-004 · Tras un día grande en un índice, el siguiente va en contra

**Idea** (pre-registrada por el usuario, 2026-10-09): tras un shock hay participantes obligados a operar sin mirar el precio (reducción de riesgo, llamadas de margen, coberturas) que empujan el precio más allá de lo justificado; quien da liquidez cobra cuando vuelve. Mecanismo de flujos forzados, como [[H-010]] y [[H-073]]. Viene de las observaciones del laboratorio AED `es_autocorrelacion` (ρ diaria ES −0,07, t HC1 −2,07) y `es_reversion_diaria` (regla sin filtro, DESCARTADA).

## Especificación (fijada antes de ver resultados)
- ES y NQ (diario Globex ajustado por roll del repo `aed`), DAX, FTSE 100 y Nikkei 225 (contado, Yahoo `^GDAXI`, `^FTSE`, `^N225`), cada uno con su calendario.
- σ60 = desviación típica de los 60 retornos anteriores a t (sin t). Día grande: |r_t| > 1 × σ60. Al cierre de t, en contra del día; cierre al cierre de t+1. Tamaño ∝ 1/σ60. Coste 1 pb por operación completa.
- Criterios: (1) media neta conjunta > 0 con t agrupado por fecha > 2; (2) media > 0 en ≥ 4 de 5 índices; (3) media tras > 2 σ60 > media tras 1–2 σ60; (4) DD máx. de la cartera a 6 % de vol < 10 %.

## Muestra y forma
- **Decisiones del usuario (2026-10-09):** script en `aed` (`estudios/reversion_dia_grande.py`, vista `#reversion_dia_grande/Cartera`, hallazgo A-002), no en `laboratorio/`: el motor no tiene cartera multiactivo, tamaño 1/σ60, t agrupado ni Yahoo. IS de `aed` (≤ 2019-12-31), no la clásica de aquí (≤ 2020-12-31): 2020 queda fuera.
- Señales desde 2009-12-22 (cuando los 5 tienen σ60; ES/NQ empiezan el 2009-09-28). Yahoo: filas sin cierre eliminadas en 2009-06 → 2019: DAX 5, FTSE 1, Nikkei 22 (festivos); sin duplicados.

## Resultado IS (2026-10-09, salida de consola del script)
- Por índice (neta pb a 1/σ60 · t HC1 · aciertos · ops): ES +8,57 · +1,72 · 52,1 % · 700; NQ +7,68 · +1,66 · 51,3 % · 725; DAX −3,14 · −0,73 · 50,2 % · 717; FTSE −10,54 · −2,27 · 46,3 % · 709; Nikkei −3,09 · −0,63 · 49,8 % · 683.
- Conjunto: −0,08 pb/op, t agrupado por fecha −0,03 (3 534 ops, 1 646 fechas). 1–2 σ60: −2,36 pb (t −0,92, n 2 732); > 2 σ60: +7,70 pb (t +0,98, n 802).
- Cartera escalada a posteriori a 6 % de vol (factor ×0,185; no cambia el Sharpe): Sharpe −0,01, DD máx. −16,8 %, 6/11 años positivos, 81,3 ops cada 60 días. Skew diario −0,93, por operación −0,22. Peor operación: Nikkei, salida 2011-03-15 (Fukushima), −1 113 pb a 1/σ60 = −2,06 % del capital a 6 %.
- **Criterios:** cumple el 3; fallan 1, 2 y 4. Veredicto del MVP: DESCARTADA (exploratorio, solo IS). Pendiente de la palabra del usuario según [[veredicto]].

## 2026-10-09 · Solo ES y NQ (decisión del usuario, a posteriori)
- **Petición del usuario:** «borra lo que acabas de hacer y deja unicamente el hecho para ES y NQ». Se borraron la descarga de Yahoo (DAX, FTSE, Nikkei) y sus datos en `aed`; el script quedó solo con ES y NQ. Las cifras de 5 índices de arriba se conservan como registro de la prueba pre-registrada.
- ES y NQ se eligieron después de ver que eran los dos positivos: **observación, no prueba; sin veredicto.**
- Resultado (consola del script): +8,12 pb/op, t agrupado por fecha +1,81 (t sin agrupar +2,39: ES y NQ se mueven juntos el mismo día), N 1 425. 1–2 σ60: +4,38 pb (t +1,07); > 2 σ60: +20,43 pb (t +1,60). Cartera a 6 % (×0,297): Sharpe +0,57, DD máx. −11,2 %, 7/11 años positivos, 33,0 ops cada 60 días. Skew diario +0,07, por operación −0,17. Peor operación: ES, salida 2018-02-05, −1 073 pb a 1/σ60 (−3,18 % del capital a 6 %).
- Criterios del pre-registro como referencia: 1 no (t 1,81), 3 sí, 4 no (−11,2 %); el 2 no aplica.

## 2026-10-09 · Validación OOS en ES (pendiente de la palabra del usuario)
- **Autorización literal del usuario:** «Validación out-of-sample de H-PROPIA-004 en ES. Una sola ejecución. Regla congelada, no la modifiques […] Datos: ES diario, serie ajustada por roll, SOLO periodo out-of-sample (2020-01-01 en adelante).» Al preguntarle por el holdout de `aed` (≥ 2024), eligió «Solo OOS 2020–2023»: el **holdout sigue sellado**. Vale solo para esta ejecución.
- **Criterios** (fijados por el usuario antes de ejecutar): (1) media neta OOS > 0; (2) t de la diferencia OOS − IS (+8,57 pb) > −2; (3) DD máx. < 10 % escalado a 4 % de vol.
- **Forma:** `aed/estudios/reversion_dia_grande_oos.py` (`AED_OOS=1`), regla de `reversion_dia_grande` sin cambios, coste 1 pb. Del IS solo se usaron los 60 retornos para el σ60 inicial y las 700 operaciones IS para el test de diferencia. El coste del CFD de Axi no está configurado en ningún sitio: no hubo segunda ejecución. Escalados a 4 % y 6 % de vol, a posteriori sobre el OOS.
- **Resultado** (consola del script; OOS 2020-01-02 → 2023-12-29, 1 034 sesiones): 301 operaciones (17,5 cada 60 sesiones), neta −4,25 pb/op (bruta −3,18), t HC1 −0,50, aciertos 46,2 %. Diferencia con IS −12,82 pb, t Welch −1,31. Skew por operación −0,28. Peor operación: salida 2020-03-12, −605 pb a 1/σ60 (−1,90 % del capital a 4 %). Sharpe neto −0,25. DD máx. −9,6 % a 4 % (×0,315) y −14,1 % a 6 % (×0,472). Años a 4 %: 2020 +2,1 %, 2021 +2,5 %, 2022 −2,8 %, 2023 −5,9 %.
- **Feb–abr 2020:** 32 operaciones, −10,5 pb/op, aciertos 53 %, −1,2 % a 4 %, DD dentro del tramo −5,8 %. Resto del OOS: 269 operaciones, −3,50 pb/op (t −0,48): el mal resultado no se debe al COVID.
- **Criterios:** 1 no; 2 sí; 3 sí (−9,6 %, cerca del límite). **DESCARTADA** (falla el 1). Pendiente de la palabra del usuario según [[veredicto]].
