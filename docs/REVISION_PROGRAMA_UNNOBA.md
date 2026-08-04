# Revisión del proyecto vs Programa de la asignatura (UNNOBA)

## 1) Fuentes comparadas

- Proyecto: sistema Prolog + frontend Streamlit + documentación del repositorio.
- Programa oficial: `ProgramaLogFuncional_concursado.pdf` (UNNOBA, Programación Lógica y Funcional).

## 2) Cobertura por unidad del programa

### Unidad I (Paradigma declarativo)

**Cobertura:** Alta.

- Modelado declarativo con hechos y reglas (`src/conocimiento.pl`, `src/reglas.pl`).
- Diferenciación entre enfoque imperativo y declarativo explicada en `README.md`.

### Unidad II (Lógica formal, resolución, unificación)

**Cobertura:** Media/Alta.

- Uso práctico de unificación y resolución en consultas Prolog.
- Se explica el comportamiento declarativo y de búsqueda.
- No hay desarrollo teórico formal completo (Herbrand/formas normales) en código, lo cual es aceptable para proyecto aplicado, pero conviene defenderlo en exposición oral.

### Unidad III (Programación lógica en Prolog)

**Cobertura:** Alta.

- Hechos, reglas, consultas, recursión, listas, backtracking.
- Restricciones compuestas (presupuesto, cupos, edad, reglas de liga).
- Optimización con predicados de combinaciones.

### Unidad IV y V (Paradigma y programación funcional)

**Cobertura previa:** Baja (solo mención conceptual en README).  
**Cobertura actual:** Media, con soporte práctico agregado.

- Se incorporó `functional/funcional_racket.rkt` con:
  - funciones puras,
  - listas,
  - recursión/fold,
  - funciones de orden superior (`map`, `filter`, `sort`),
  - composición para recomendación.
- Esto reduce riesgo de que el trabajo quede "solo Prolog" ante un tribunal que espere evidencia de ambos paradigmas.

## 3) Hallazgos críticos detectados y corregidos

1. **Regla duplicada de `combinacion_valida/2`**  
   Existían dos definiciones; la primera no exigía `cumple_reglas_liga/2`, permitiendo aceptar combinaciones inválidas para liga.  
   **Estado:** Corregido en `src/reglas.pl`.

2. **Definición duplicada de `combinacion_optima/2`**  
   Generaba advertencias de orden de cláusulas y confusión semántica.  
   **Estado:** Corregido en `src/reglas.pl`.

3. **Warning de variables singleton en `quimica_entre/3`**  
   Había variables no usadas en la cláusula de fallback.  
   **Estado:** Corregido en `src/reglas.pl`.

## 4) Validaciones ejecutadas

- `swipl -q -f "test_sintaxis.pl" -t halt`  
  Resultado: pruebas básicas correctas.
- Consulta de consistencia post-fix para verificar que `combinacion_valida/2` no omita reglas de liga.
- `python3 -m py_compile frontend/app.py frontend/prolog_bridge.py frontend/visual_data.py frontend/prepare_assets.py generate_trabajo_docx.py`  
  Resultado: sin errores de sintaxis.
- Validación de bridge Prolog-Python:
  - equipos Prolog: 6
  - jugadores en base Prolog: 54
- Validación de datos visuales:
  - equipos con escuadra Transfermarkt guardada: 20
  - jugadores cacheados en escuadras: 411
  - assets de logos locales: 20 PNG + fallback SVG

## 5) Riesgo académico residual (y cómo mitigarlo)

1. **Predominio de parte lógica sobre la funcional**
   - Mitigación aplicada: archivo funcional en Racket + documentación.
   - Recomendación de defensa: mostrar en vivo una ejecución de Prolog y otra de Racket.

2. **Dependencia parcial de scraping externo para assets**
   - Mitigación aplicada: almacenamiento local en `frontend/assets`.
   - Recomendación: correr `python3 frontend/prepare_assets.py` antes de demo final.

## 6) Conclusión

El proyecto **sí es defendible** para la asignatura y aplica de forma clara los contenidos centrales de programación lógica.  
Tras las correcciones realizadas, también queda mejor cubierto el componente funcional exigido por el programa.

En su estado actual, el trabajo es **mucho menos cuestionable** técnica y académicamente que antes de esta revisión.
