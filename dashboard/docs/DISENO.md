# Sistema de diseño

Estética: **depth map**. Monocromo sobre negro, superficies hechas de puntos, retícula técnica. Referencia: pantallas de instrumento y nubes de puntos LiDAR.

## Tokens (`src/styles.css`, `:root`)

**Tipografía: cada tamaño tiene un papel**

| Token | Tamaño | Papel |
|---|---|---|
| `--fs-1` | 11px | Etiquetas, notas, ejes |
| `--fs-2` | 13px | Texto, subtítulos de bloque |
| `--fs-3` | 15px | Pregunta de la hipótesis |
| `--fs-4` | 14–17px (fluido) | Cifras KPI |
| `--fs-5` | 38px | Nombre (VT323) |

**Familias:** `--sans` (IBM Plex Sans) para texto · `--mono` (IBM Plex Mono) para cifras · `--display` (VT323) solo para el nombre.

**Texto:** `--ink` contenido · `--muted` etiquetas y secundario · `--faint` terciario (ejes, pie).

**Semántica:** `--pos` ganancia / se sostiene · `--neg` pérdida / falsada · `--caution` no concluyente. Desaturados; nunca decorativos.

## Patrones

- **Bloque:** método → cifras → gráfico.
- **KPI:** etiqueta (fs-1, muted) / cifra (fs-4, mono) / detalle (fs-1, muted). Cifras con signo en `--pos`/`--neg`.
- **Gráfico:** sin marco. Título fs-2 + subtítulo fs-1 en una línea. Rejilla punteada `[1, 3]`. Gráfico principal + tira secundaria con eje X compartido (equity/DD, histograma/IC, barras/puntos).
- **Superficies:** nube de puntos en 4 capas de profundidad (`DEPTH` en `main.js`): densa y brillante junto a la curva, tenue al alejarse. La curva real va encima, a 1,6px.
- **Barras:** columnas de filas de puntos (`dotBar`).
- **Estado:** línea de 2px arriba del todo con el color de la fase.

## Movimiento

- Cambio de fase: el tramo nuevo de la equity se traza de izquierda a derecha mientras el eje se amplía (`DRAW_MS`).
- Las cifras KPI cuentan hasta su valor nuevo (`DUR`).
- Todo se desactiva con `prefers-reduced-motion`.

## Qué no hacer

- Tamaños o colores sueltos fuera de los tokens.
- Tarjetas con fondo y borde para los gráficos.
- Texto explicativo en párrafos: si hace falta explicar, falta un gráfico o sobra el elemento.
- 3D o perspectiva: la profundidad se simula con densidad y brillo, nunca deformando escalas.
