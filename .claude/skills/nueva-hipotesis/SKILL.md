---
name: nueva-hipotesis
description: Añadir una hipótesis al dashboard (datos del lab + entrada en el registro) o actualizar sus fases y estados, incluida la misma hipótesis en varios activos (comparativa). Úsala cuando el usuario diga "añade H-00X", "añade H-00X en QQQ/IWM…", "sube el OOS de…", "marca … como falsada" o similar.
---

# Añadir o actualizar una hipótesis

1. **Datos:** no se copian. El dashboard lee `dashboard/public/lab/<experimento>/` (enlace a `resultados/`). Comprueba que el experimento existe en `resultados/indice.csv`.
2. **Registro:** añade o edita la entrada en `dashboard/public/data/hipotesis.json`:
   - `nombre`: `EFECTO · ACTIVO`, corto, en mayúsculas (se pinta en VT323).
   - `efecto`: etiqueta corta del grupo que se compara con el resto (p. ej. `TOM`).
   - `reglas`: 2–4 pares clave → valor, en minúsculas y sin punto final (`"Entrada": "cierre · penúltima sesión del mes"`).
   - `experimentos`: `{ "IS": "<ID del experimento>" }`, p. ej. `H001-IS-REAL-001`.
   - `costes`: una línea.
   - `estados`: `inconclusive` | `holds` | `falsified` por fase (`IS`, `OOS`, `Total`).
   - **Varios activos de una hipótesis** (p. ej. H-001 en SPY, QQQ, IWM, DIA): una entrada por activo con `id` `H-NNN-ACTIVO`, `hipotesis: "H-NNN"`, `nombre` `EFECTO · ACTIVO` y mismas `efecto`, `reglas` y `costes`. Con 2 o más entradas del mismo `hipotesis`, la portada las agrupa en una fila y `#H-NNN` abre la comparativa (`src/comparativa.js`) sin tocar código. Orden del registro = color (`--series-1…4`): máximo 4 activos; con más, hay que ampliar y validar la paleta.
3. **Formato distinto:** si la ficha no encaja, adapta **solo** `dashboard/src/data.js` para que devuelva fases con la forma
   `{ key, state, start, end, equity: [[fecha, equity, exposición]], trades: [{ net, cost }], research }`.
   No toques `dashboard/src/ficha.js` para casos particulares.
4. **Verifica:** `npx vite build` sin errores (dentro de `dashboard/`) y abre `http://localhost:5173/#<ID>`. Comprueba que los KPIs de IS coinciden con las métricas del motor.
5. **Diseño:** si hace falta mostrar algo nuevo, sigue `dashboard/docs/DISENO.md` (tokens, método → cifras → gráfico, sin scroll).
