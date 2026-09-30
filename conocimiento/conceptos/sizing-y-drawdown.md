# Sizing y drawdown

- **1 unidad** (1 acción o 1 punto): exposición del 1–4 % de la cuenta. El DD sale ~0,25 %, sin significado.
- **Fracción de la equity** (`fraccion` en `[operativa]`, C10): el tamaño crece y decrece con la cuenta. [[H-001]] usa el 30 % desde el 2026-09-24.
- **El sizing no cambia la ventaja** (efecto, IC, años). Solo escala la rentabilidad y el DD, casi en proporción.
- **DD de referencia de la estrategia = al 100 % del capital, sin apalancamiento.** Al 30 % sale ≈ 0,3 × ese DD.
  - Con el 100 % exacto la comisión de entrada no cabe: se usa el 99,9 %.
  - Guardarlo en `resumen.json` está aparcado por decisión del usuario (2026-09-25).
- En ES, el 30 % de 10.000 USD es una fracción de contrato: sirve para comparar, no es operable. Por eso [[H-007]] sigue con 1 punto.
