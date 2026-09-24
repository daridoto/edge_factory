# Handoff

## Estado (24/09/2026)

- Migrado dentro del lab (`edge_factory/dashboard/`). Lee `../resultados` a través de `public/lab`; ya no hay copias de datos.
- Portada con todas las hipótesis y ficha por hipótesis (`#H-NNN`). H-001 y H-007 con datos reales de IS.
- `src/metrics.js` coincide con `resumen.json` en las 10 métricas de ambas hipótesis.
- Comparativa `#H-001`: H-001 en SPY, QQQ, IWM y DIA con 30 % de la equity por operación (H001-IS-REAL-005 a 008).
- **De ejemplo todavía:** las réplicas del bootstrap (generadas desde el IC). El OOS de ejemplo de H-001 se retiró el 2026-09-24: solo se muestra IS real.

## Decisiones tomadas

- **Vanilla + Vite, sin React:** cabe en pocos ficheros legibles.
- **Una pantalla sin scroll** en la ficha: se compacta dentro de los gráficos antes que añadir alto.
- **Fases como capas de la misma ficha:** una fase = un experimento del lab de la misma hipótesis con otra muestra (`experimentos` en el registro).
- **`data.js` como única frontera** con el formato del lab. Una hipótesis nueva no toca código: solo registro. Si obliga a tocarlo, va a `data.js`, nunca a `ficha.js`.

## Pendiente

| Necesidad | Qué hace falta | Dónde |
|---|---|---|
| Réplicas reales del bootstrap | que `resumen.json` (o un CSV) exporte el vector de réplicas | lab |
| Componentes con clave fija | hoy `data.js` los lee por posición (ventana, resto) | lab |
| OOS / Holdout reales | muestra y autorización del usuario; el contrato hoy solo admite IS | lab + registro |
| Notas por hipótesis | preguntas del usuario que el lab recoge y responde con un experimento | por diseñar |
| Desglose (p. ej. media por hora en H-007) | decidir si y cómo se muestra | dashboard |
