---
hipotesis: H-PROPIA-001
nombre: RAY · temporada de DEX por volumen de Raydium
experimentos: [HPROPIA001-IS-REAL-001]
papers: [propia]
---
# H-PROPIA-001 · RAY largo 28 días cuando el volumen de Raydium dobla su nivel normal

**Idea** (del usuario, 2026-09-30): si la mediana de 7 días del volumen de Raydium (DefiLlama) es al menos el doble que la de 90 días, se compra RAYUSDT a la apertura siguiente. Se sale al cierre de t+28 o con un stop del −25 %. Costes del 0,2 % por lado. Más volumen trae más comisiones, y con ellas más recompras de RAY (12 % de las fees). La hipótesis completa es la que pegó el usuario en la conversación.

## Muestra y autorización
- Los datos no tocan la IS del lab (2009-09-27 → 2020-12-31): `RAY_diario.csv` empieza el 2021-08-10 y el volumen de Raydium, el 2022-08-15.
- **Autorización literal del usuario (2026-09-30):** «directamente backtestea la estrategia eso nos servira para contrastar y ver si nos da lo mismo, ademas no hagas caso al contrato si quieres hablemos aqui los periodos de muestra para que estes listo o propon alguno, creo que usamos todo el historico porque en cripto no hay tanto rangos de tiempo». Vale solo para este contraste de H-PROPIA-001, que usa todo el histórico hasta el 2026-09-29.
- El usuario ya fijó el stop y el día de salida mirando todo el histórico, así que ese periodo es in-sample. El único fuera de muestra limpio es el seguimiento en tiempo real desde el 2026-09-30.

## Hallazgos nuestros
- **2026-09-30 · El contraste independiente reproduce sus cifras.** Se hizo con un script fuera del lab, en el scratchpad, y sin `resultados/`. Salen 16 operaciones cerradas y 1 abierta (entrada el 2026-09-21). Winrate 62 %, media +37,5 %, mediana +11,1 %, t 2,44, payoff 3,95 y PF 6,58. Exceso medio frente a BTC de +31,0 % (mediana +14,1 %). Placebo de 16 entradas aleatorias con separación mayor de 28 días: el resultado real queda en el percentil 99 (p95 del placebo +30,0 %). Sin stop: media +37,4 % y t 2,42.
- **Para cuadrar hay que copiar dos detalles de su implementación:**
  - El enfriamiento deja entrar el mismo día t+28. Si se exige t+29 salen 13 operaciones y la media sube a +47 %.
  - Las ventanas de 7 y 90 se cuentan por filas con dato y se saltan los 4 huecos de DefiLlama. Si se exige que los 90 días naturales estén completos, desaparecen las señales de 2022-11, 2023-01 y 2025-05.
  - Las dos variantes se decidieron sobre los datos, así que son sensibles.
- **Drawdown:** −44 % componiendo operación a operación con el 100 % del capital. El −54 % del usuario es el diario, marcando a mercado dentro de cada operación: confirmado en el lab (−54,1 %).
- **Concentración:** 5 operaciones (de +90 % a +146 %) explican casi todo el resultado. Tres de los cinco stops o pérdidas grandes (2022-11, 2025-01 y 2025-05) llegan en mercados laterales o bajistas.
- `raydium_volumen_usd` de `RAY_diario.csv` y `RAY_volumen_usd` de DefiLlama son la misma serie; solo difieren en el redondeo.
- **2026-09-30 · En el lab (HPROPIA001-IS-REAL-001) salen las mismas cifras.** Se usa la muestra IS cripto (2021-08-10 → 2026-09-29), autorizada solo para esta hipótesis; la simulación arranca el 2022-08-15, primer dato de volumen. Media +37,51 %/op, IC bootstrap 9,4 a 68,2, mediana +11,08 %, t 2,44, placebo en el percentil 98,85 (p95 30,98 %) y exceso frente a BTC de +31,0 %. Con valoración diaria el **max DD es −54,1 %**, el mismo que dio el usuario. Estaba abierto al final: la cuenta seguía 11 días bajo máximos. Payoff 1,83 y PF 3,06 **en USDT componiendo**, más bajos que en % por operación (3,95 y 6,58): las pérdidas grandes de 2024-07, 2025-01 y 2025-05 llegan con la cuenta ya multiplicada. Queda 1 señal sin cerrar (2026-09-20).
- La primera señal del lab es el 2022-11-14 y la del usuario, el 2022-11-12, por cómo se cuentan los primeros 90 datos. Las dos acaban en stop: no cambia nada.

## Preguntas abiertas
- Seguimiento en tiempo real desde el 2026-09-30 con los criterios de refutación del usuario.
