# NeuroNova Apps — estándar dimensional de referencia v1

Fuente de verdad: `neuronova-apps/neuronova-apps.github.io` (rama `main`), archivos `index.html`, `styles.css`, `presentation.css`. Valores obtenidos del CSS y su cascada; aún no medidos con navegador en diferentes resoluciones. No se altera la matriz.

## Tokens comunes de identidad
- Fondo `#06101d`, texto `#f5f8fc`, secundario `#aebdcd`, acento cian `#65ddff`, azul `#7f9cff`, violeta `#b28dff`.
- Fuente base: Inter y alternativas del sistema; line-height: `1.62`.
- Contenedor matriz: `width: min(calc(100% - 36px), 1180px)`; hasta 700 px `width: min(calc(100% - 28px), 1180px)`.
- Rango mínimo de soporte declarado por el body: 320 px.

## Header de la matriz
- `.header-inner`: altura **mínima** 66 px escritorio, 62 px <=700 px; flex, espacio entre elementos, `gap:24px`. No definir altura exacta.
- `.brand-symbol`: 38×38 px; radio 12 px. `.brand` gap 11 px.
- `.brand-copy strong`: 1rem; etiqueta `Apps` .82rem/peso 760.
- `.main-nav` gap 5 px; enlaces padding 8px 12px, radio 10 px, tamaño .92rem y peso 720.
- Botón menú móvil 42×42 px; menú colapsado hasta 700 px. En ese breakpoint, menú desplegado comienza en `top:62px`.
- Header sticky, `top:0`, fondo `rgba(5,14,26,.78)`, `backdrop-filter:blur(18px) saturate(140%)`, borde inferior translúcido.

## Body
- Secciones `.section`: padding vertical 96 px escritorio, 72 px <=700 px; se exceptúan portadas, héroes y pantallas de juego.
- Catálogo consolidado (la capa `presentation.css` prevalece): tarjetas con padding 18px, radio 22px, gap 16px; grid minmax(280px,340px) en pantallas amplias, 1 columna <=700 px.
- El cuerpo de cada juego, formulario, simulador o reproductor conserva su sistema de layout, tamaño de tablero, controles y accesibilidad particulares.
- Botones de las apps no deben heredar tamaños ni clases genéricas de la portada sin validación visual y funcional.

## Footer matriz
- `.site-footer`: margen superior 20px, padding 70px 0 24px; fondo `rgba(2,8,15,.52)`, borde superior 1px.
- `.footer-grid`: 3 columnas proporción `1.5fr .65fr 1fr`, gap 60px, padding-bottom 48px.
- Textos pie marca .9rem; títulos de sección .78rem; enlaces .88rem.
- `.footer-bottom`: flex horizontal, gap 20px, padding-top 22px, borde superior, fuente .76rem.
- <=980px: dos columnas `1.2fr .8fr`, último bloque en nueva fila.
- <=700px: una columna, gap 34px; bloque final en columna.
- **La altura total es variable:** preservar estructura, márgenes, proporciones y comportamiento, no imponer idéntico alto en píxeles cuando difiere el contenido.

## Reglas para futura aplicación
1. La matriz principal es referencia institucional; categorías, páginas informativas y políticas deben aproximarse a su shell de forma controlada.
2. Las siete webs interactivas conservan la identidad propia, navegación interna y funcionalidad; adaptar solamente elementos compartibles sin forzar un único CSS global.
3. Para privacidad, uniformizar el marco (cabecera/pie/contenedor), no copiar contenido legal entre aplicaciones.
4. Ensayar anchos 320, 375, 414, 700, 768, 980, 1024, 1180 y 1440 px. Verificar reflujo, foco, contraste y ausencia de overflow.
5. Cada modificación a la matriz será PR aislado; el agente únicamente genera diagnósticos y propuestas. No cambiar código de apps ni políticas sin evidencia.
6. **Estado**: estándar CSS definido; implementación transversal y verificación visual todavía pendientes.

## Nota de consistencia
Las páginas de categoría usan actualmente otro ancho máximo (1120 px) y header min-height 74 px con padding vertical, por lo que no cumplen aún literalmente el valor matriz. Esta diferencia requiere una migración deliberada con comprobación responsiva: no reemplazar valores globales a ciegas.
