# Guía Rápida de Inicio

## Carga Rápida del Sistema

```bash
# Iniciar SWI-Prolog
swipl

# Cargar el sistema
?- [src/sistema_compras].
```

## Consultas Básicas Inmediatas

```prolog
% 1. Verificar si un equipo puede firmar a un jugador
?- puede_firmar('Real Madrid', 'Robert Lewandowski').

% 2. Ver recomendaciones
?- recomendar('Barcelona', Jugador).

% 3. Mejor fichaje
?- mejor_fichaje('Liverpool', Jugador).

% 4. Listar jugadores disponibles
?- jugadores_disponibles('Manchester City', Lista).

% 5. Filtrar por posición
?- jugadores_por_posicion('Real Madrid', delantero, Lista).
```

## Estructura de Archivos

- `src/conocimiento.pl` - Base de datos (jugadores, equipos)
- `src/reglas.pl` - Lógica del sistema
- `src/sistema_compras.pl` - Archivo principal
- `examples/consultas.pl` - Más ejemplos de consultas
- `examples/ejecucion_ejemplo.txt` - Salidas esperadas

## Notas Importantes

- Presiona `;` para ver más soluciones (backtracking)
- Presiona `.` o Enter para aceptar una solución
- Usa `halt.` para salir de SWI-Prolog

## Verificación rápida antes de entregar

```bash
# Sintaxis base
swipl -q -f test_sintaxis.pl -t halt

# Tests lógicos (plunit)
swipl -q -f tests/prolog_logic_tests.pl -g run_tests -t halt

# Tests bridge Python-Prolog
python3 -m unittest tests/test_prolog_bridge.py -v

# Benchmark simple de consultas
python3 benchmarks/run_benchmarks.py

# (Opcional) Validar parte funcional comparativa
racket functional/funcional_racket.rkt
raco test functional/funcional_racket.rkt
```

