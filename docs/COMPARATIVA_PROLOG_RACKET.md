# Comparativa formal: Prolog vs Racket (Scheme)

## 1) Objetivo comparativo

Este documento explicita el enfoque comparativo exigido por la materia: resolver el mismo problema de recomendación de fichajes con dos paradigmas declarativos diferentes:

- `src/*.pl`: versión lógica en Prolog.
- `functional/funcional_racket.rkt`: versión funcional en Racket (dialecto de Scheme).

## 2) Equivalencia funcional mínima entre implementaciones

| Problema | Prolog | Racket/Scheme |
|---|---|---|
| Determinar fichaje viable | `puede_firmar/2` | `puede-firmar?` |
| Listar candidatos válidos | `recomendar/2` | `recomendaciones` |
| Mejor candidato | `mejor_fichaje/2` | `mejor-fichaje` |
| Validar combinación | `combinacion_valida/2` | `comb-valida?` |
| Mejor combinación | `combinacion_optima/2` | `mejor-combinacion` |

## 3) Diferencias de enfoque

### Prolog (lógico)
- Se modela **qué** condiciones definen una solución.
- El motor resuelve con unificación y backtracking.
- Muy conciso para relaciones, restricciones y búsqueda.

### Racket/Scheme (funcional)
- Se modela **cómo** transformar estructuras inmutables.
- El flujo de búsqueda es explícito (filtros, ordenamientos, generación de subconjuntos).
- Mayor control sobre estrategia de datos y composición funcional.

## 4) Fragmentos representativos

### Prolog

```prolog
puede_firmar(Equipo, Jugador) :-
    puede_pagar(Equipo, Jugador),
    juega_posicion_necesaria(Jugador, Equipo),
    cumple_restricciones_edad(Jugador, Equipo).
```

### Racket

```racket
(define (puede-firmar? eq j)
  (and (puede-pagar? eq j)
       (cubre-necesidad? eq j)
       (cumple-edad? eq j)))
```

## 5) Evidencia de cobertura de contenidos de la materia

### Unidad II-III (lógica + Prolog)
- hechos, reglas, consultas, unificación, backtracking, recursión.

### Unidad IV-V (funcional + Scheme)
- funciones puras, inmutabilidad, funciones de orden superior (`map`, `filter`, `foldl`),
- recursión explícita para generación de combinaciones,
- separación dato/operación con structs y pipelines funcionales.

## 6) Cómo defender oralmente la comparación

1. Mostrar una consulta Prolog y su predicado equivalente funcional.  
2. Explicar que Prolog minimiza el control explícito del flujo y delega búsqueda al motor.  
3. Explicar que en Racket la búsqueda y poda son explícitas, con mayor control algorítmico.  
4. Concluir que ambos paradigmas son válidos, pero optimizan distintos objetivos cognitivos.

## 7) Ejecución recomendada para exposición

```bash
# Prolog
swipl -q -f test_sintaxis.pl -t halt
swipl -q -f tests/prolog_logic_tests.pl -g run_tests -t halt

# Funcional (requiere Racket instalado)
racket functional/funcional_racket.rkt
raco test functional/funcional_racket.rkt
```

> Nota: en esta máquina de desarrollo no se encontró `racket` instalado al momento de la última validación local.  
> Para la defensa final conviene instalarlo previamente y registrar una corrida en capturas o en consola.
