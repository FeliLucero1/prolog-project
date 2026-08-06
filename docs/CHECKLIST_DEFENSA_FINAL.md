# Checklist de defensa final

## 1) Preparación técnica (antes de exponer)

- [ ] Activar entorno virtual: `source .venv/bin/activate`
- [ ] Actualizar assets locales: `python3 frontend/prepare_assets.py`
- [ ] Correr pruebas de Prolog:
  - `swipl -q -f test_sintaxis.pl -t halt`
  - `swipl -q -f tests/prolog_logic_tests.pl -g run_tests -t halt`
- [ ] Correr pruebas de bridge Python:
  - `python3 -m unittest tests/test_prolog_bridge.py -v`
- [ ] Correr benchmark local:
  - `python3 benchmarks/run_benchmarks.py`
- [ ] Validar componente funcional comparativo (Racket):
  - `racket functional/funcional_racket.rkt`
  - `raco test functional/funcional_racket.rkt`
- [ ] Levantar frontend:
  - `streamlit run frontend/app.py --server.port 8501`

## 2) Guion breve de demo (8-10 minutos)

1. **Contexto del problema**  
   Explicar por qué fichajes es un problema de restricciones.

2. **Paradigma lógico aplicado**  
   Mostrar consultas:
   - `puede_firmar/2`
   - `mejor_fichaje/2`
   - `combinacion_optima/2`

3. **Trazabilidad de decisión**  
   En frontend: usar "Modo explicación académica" para mostrar por qué un fichaje pasa/falla.

4. **Restricciones y química**  
   Mostrar efecto de presupuesto, edad, posición y química.

5. **Implementación funcional comparativa (Racket/Scheme)**  
   Ejecutar:
   - `racket functional/funcional_racket.rkt`
   - `raco test functional/funcional_racket.rkt`
   y mapear equivalencias con Prolog (`puede_firmar` ↔ `puede-firmar?`, etc.).

6. **Evidencia cuantitativa**  
   Mostrar `benchmarks/latest_benchmark.md`.

## 3) Preguntas difíciles (respuestas sugeridas)

- **¿Por qué Prolog para este problema?**  
  Porque el dominio es naturalmente declarativo y con múltiples restricciones.

- **¿Qué aporta la parte funcional?**  
  Muestra otra forma de resolver selección/ranking con funciones puras y composición.

- **¿Cómo validaron correctitud?**  
  Con pruebas automáticas Prolog + Python y verificación de casos borde.

- **¿Qué limitaciones tiene?**  
  Base de conocimiento acotada y simplificación de métricas deportivas.

## 4) Entregables que conviene mostrar

- `README.md`
- `docs/REVISION_PROGRAMA_UNNOBA.md`
- `docs/COMPARATIVA_PROLOG_RACKET.md`
- `docs/CHECKLIST_DEFENSA_FINAL.md`
- `Trabajo_Final_Prolog.docx`
- `benchmarks/latest_benchmark.md`
