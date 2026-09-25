# Dashboard de hipótesis

Dashboard de una sola pantalla para leer de un vistazo el resultado de una hipótesis cuantitativa: reglas, evidencia estadística, resultado económico y robustez, fase a fase (IS → OOS → Holdout). Hoy solo hay IS real; OOS y Holdout aparecen como pendientes.

## Stack

- Vite + JavaScript vanilla, sin framework. HTML en `index.html`.
- ECharts para los gráficos. El de equity va en canvas (miles de puntos); el resto, en SVG.
- CSS escrito a mano con tokens en `src/styles.css`. Sin Tailwind.
- `npm run dev` → http://localhost:5173 (`#H-001-QQQ` abre una ficha; `#H-001` la comparativa de sus instrumentos).

## Estructura

| Fichero | Papel |
|---|---|
| `public/data/hipotesis.json` | Registro: nombre, reglas, costes, estados, etiqueta del efecto y experimento del lab de cada fase. `hipotesis` agrupa las entradas de una misma hipótesis en varios instrumentos |
| `public/lab/` | Enlace (solo lectura) a `../resultados` del lab: `resumen.json`, `equity.csv`, `operaciones.csv` por experimento |
| `src/data.js` | Único punto que conoce el formato del lab → lo convierte en **fases** |
| `src/metrics.js` | KPIs económicos. Replica las convenciones del motor del lab (verificado al 5.º decimal) |
| `src/main.js` | Entrada: sin `#`, portada; `#<hipotesis>` con varias entradas, comparativa; `#<id>`, ficha |
| `src/home.js` | Portada: una fila por hipótesis; las de varios instrumentos, agrupadas (registro + experimentos sin registrar de `indice.csv`) |
| `src/ficha.js` | Ficha: cabecera, KPIs animados, gráficos y cambio de fase |
| `src/comparativa.js` | Comparativa: IC en escala común, equity superpuesta (%), matriz año × instrumento y tabla por instrumento |
| `docs/` | Diseño, handoff y ejemplos del formato del lab |

Forma de una fase (contrato interno; todo lo demás depende solo de esto):
`{ key, state, start, end, equity: [[fecha, equity, exposición]], trades: [{ net, cost }], research }`

## Reglas de diseño (no negociables)

- Leer `docs/DISENO.md` antes de tocar estilos o gráficos.
- **Solo los tamaños de la escala** `--fs-1…--fs-5`. Nunca un px suelto.
- **Fuentes:** sans para texto, mono para cifras, VT323 (`--display`) solo para el nombre.
- **Color:** monocromo. Rojo/verde/ámbar solo con significado (pérdida, ganancia, cautela). Excepción: `--series-1…4` identifican instrumentos en la comparativa (paleta validada para daltonismo, claro y oscuro).
- **Gráficos sin marco:** sin fondo ni borde, sobre el fondo de la página. Rejilla punteada.
- **Una pantalla, sin scroll**, en ventanas normales. Si algo no cabe, se compacta dentro de los gráficos antes que añadir alto.
- Patrón por bloque: **método → cifras → gráfico**. Nada de párrafos explicativos.

## Trampas conocidas

- **Un error dentro de un `formatter` de ECharts bloquea el gráfico:** después, todo `setOption` falla con "should not be called during main process" y parece que el filtro o el resaltado no funcionan. Revisar la consola antes de buscar el fallo en otra parte.
- En eje `type: 'time'`, `axisValue` es un número; la fecha en texto se toma del dato (`p.data[0]`).
- Sin navegador en el entorno de la IA: compilar (`npx vite build`) no prueba la interacción. Pedir al usuario que lo pruebe y pegue la consola.

## Cómo trabajar con el usuario

- Habla de diseño (jerarquía, densidad, tipografía, gráficos), no del formato de los datos.
- Respuestas concisas. Enseña el cambio con un esquema ASCII si ayuda.
- No añadir información por añadir: cada elemento tiene que responder a una pregunta de la hipótesis.
- Vive dentro del lab (`edge_factory/dashboard/`). **Desde aquí no se edita nada fuera de `dashboard/`**: el lab es dueño de `resultados/` y `esquemas/`; si cambia su formato, se adapta `data.js`, nunca el lab.
