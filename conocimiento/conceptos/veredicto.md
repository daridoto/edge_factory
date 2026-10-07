---
concepto: Veredicto de una hipótesis
fecha: 2026-10-07
fuente: conversación con el usuario
---
# Veredicto de una hipótesis

Cómo acaba una ficha. Dos capas (acordado con el usuario el 2026-10-07):

1. **Estado por fase** (IS, OOS, Total), con criterio fijo:
   - *se sostiene*: el IC 95 % no cruza cero y, en OOS, con el mismo signo que en IS.
   - *falsada*: el OOS cambia de signo respecto a IS.
   - *no concluyente*: el resto.
2. **Veredicto de la hipótesis**, que decide el usuario:
   - **candidata**: el OOS confirma el núcleo; pasa a la capa de cartera.
   - **en observación**: apunta bien pero falta algo (muestra, mecanismo).
   - **descartada**: el OOS no la confirma, o el IS no da nada.
   - **abierta**: sin OOS todavía.

La IA propone; solo se marca con la palabra del usuario, que se copia literal en `conocimiento/H-NNN.md`. En el dashboard: `estados` y `veredicto: {marca, motivo, fecha}` en el registro.

Primera candidata: [[H-018]].
