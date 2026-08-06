# Sistema Lógico de Compra de Jugadores de Fútbol en Prolog

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema declarativo** para modelar un mercado de transferencias de fútbol utilizando el paradigma de programación lógica en Prolog. El sistema permite evaluar, recomendar y optimizar la compra de jugadores considerando múltiples restricciones como presupuesto, cupos de extranjeros, necesidades de posición y restricciones de edad.

### Objetivos Académicos

- Demostrar el uso de **hechos y reglas** en programación lógica
- Aplicar **backtracking** para encontrar soluciones
- Implementar **restricciones** complejas
- Utilizar **listas y predicados recursivos**
- Realizar **filtrado por múltiples condiciones**
- Generar **combinaciones óptimas** mediante búsqueda

---

## 🏗️ Estructura del Proyecto

```
prolog/
├── src/
│   ├── conocimiento.pl      # Base de conocimiento (hechos)
│   ├── reglas.pl            # Reglas lógicas y predicados
│   └── sistema_compras.pl   # Archivo principal
├── frontend/
│   ├── app.py               # Interfaz web (Streamlit)
│   ├── prolog_bridge.py     # Conexión con SWI-Prolog
│   ├── visual_data.py       # Logos, fotos, rivales
│   └── requirements.txt
├── examples/
├── docs/
└── README.md
```

---

## 📦 Entrega del proyecto

Para dejar todo listo para entregar:

1. **Requisitos instalados:** SWI-Prolog y Python 3.10+.
2. **Probar consola Prolog:** `swipl` → `[src/sistema_compras].` → alguna consulta.
3. **Probar frontend:** desde la raíz del proyecto:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate   # o .venv\Scripts\activate en Windows
   pip install -r frontend/requirements.txt
   python3 frontend/prepare_assets.py
   streamlit run frontend/app.py
   ```
4. Abrir en el navegador la URL que indique Streamlit (p. ej. `http://localhost:8501`).
5. La portada de la app resume el proyecto; las pestañas permiten demostrar scouting, recomendaciones, combinación óptima, conocimiento y galería de jugadores.
6. El selector principal de equipo incluye el **Top 20 de clubes** y muestra la plantilla del equipo seleccionado con fotos y logos en local (siempre que se haya ejecutado `prepare_assets.py`).
7. Para equipos modelados en Prolog (como `Real Madrid`, `Barcelona`, `Manchester City`, `Bayern Munich`, `PSG`, `Liverpool`) se habilitan además análisis lógicos completos (fichaje, recomendaciones y combinación óptima).
8. Activar el **Modo explicación académica** en la barra lateral para justificar decisiones de fichaje con trazabilidad.
9. Ejecutar chequeo final:
   ```bash
   swipl -q -f test_sintaxis.pl -t halt
   swipl -q -f tests/prolog_logic_tests.pl -g run_tests -t halt
   python3 -m unittest tests/test_prolog_bridge.py -v
   python3 benchmarks/run_benchmarks.py
   ```

---

## 🚀 Instalación y Uso

### Requisitos

- **SWI-Prolog** (versión 8.0 o superior)
  - Descarga: https://www.swi-prolog.org/download/stable

### Frontend visual (recomendado para la demo)

Interfaz web para mostrar el sistema sin usar la consola de Prolog.

1. Instalar dependencias de Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r frontend/requirements.txt
   ```

2. Iniciar la app:
   ```bash
   streamlit run frontend/app.py
   ```

3. Abrir en navegador la URL que imprima Streamlit (normalmente `http://localhost:8501`).

**Qué incluye la interfaz:** resumen por equipo, evaluación de fichajes con explicación, recomendaciones con tabla y gráfica, mejor fichaje, combinación óptima con química, calculadora de química entre dos jugadores, comparador con radar (rendimiento, goles, asistencias, costo-eficiencia, proyección), galería de jugadores con búsqueda y filtro por posición, filtro por rivales y fotos (reales cuando hay URL cargada; avatar único para el resto).

### Carga del Sistema

1. Iniciar SWI-Prolog:
   ```bash
   swipl
   ```

2. Cargar el sistema:
   ```prolog
   ?- [src/sistema_compras].
   ```

3. Realizar consultas:
   ```prolog
   ?- puede_firmar('Real Madrid', 'Robert Lewandowski').
   ```

---

## 📚 Modelado del Dominio

### Hechos: Base de Conocimiento

El sistema se basa en **hechos** que representan información estática del dominio:

#### Jugadores
```prolog
jugador(Nombre, Posicion, Edad, Precio, Nacionalidad, Goles, Asistencias).
```

**Ejemplo:**
```prolog
jugador('Kylian Mbappé', delantero, 25, 180, francia, 35, 10).
```

#### Equipos
```prolog
necesita(Equipo, Posicion).
presupuesto(Equipo, Monto).
cupo_extranjeros(Equipo, Maximo).
nacionalidad_equipo(Equipo, Nacionalidad).
```

**Ejemplo:**
```prolog
presupuesto('Real Madrid', 200).
necesita('Real Madrid', delantero).
cupo_extranjeros('Real Madrid', 5).
```

### Reglas: Lógica del Sistema

Las **reglas** definen la lógica de negocio mediante predicados que relacionan hechos:

```prolog
puede_firmar(Equipo, Jugador) :-
    puede_pagar(Equipo, Jugador),
    juega_posicion_necesaria(Jugador, Equipo),
    cumple_restricciones_edad(Jugador, Equipo).
```

Esta regla **declara** las condiciones necesarias para que un equipo pueda firmar a un jugador, sin especificar **cómo** se evalúa (el motor de Prolog se encarga mediante backtracking).

---

## 🔍 Predicados Principales

### 1. `puede_firmar/2`
Verifica si un equipo puede firmar a un jugador considerando presupuesto, posición y edad.

```prolog
?- puede_firmar('Real Madrid', 'Robert Lewandowski').
true.
```

### 2. `recomendar/2`
Recomienda jugadores para un equipo ordenados por rendimiento (goles + asistencias).

```prolog
?- recomendar('Barcelona', Jugador).
Jugador = 'Erling Haaland' ;
Jugador = 'Kylian Mbappé' ;
...
```

### 3. `mejor_fichaje/2`
Encuentra el jugador con mayor rendimiento que puede ser firmado.

```prolog
?- mejor_fichaje('Liverpool', Jugador).
Jugador = 'Bukayo Saka'.
```

### 4. `combinacion_optima/2`
Genera la mejor combinación de jugadores que maximiza el rendimiento total (incluyendo química) respetando todas las restricciones (presupuesto, cupos, reglas de liga).

```prolog
?- combinacion_optima('Real Madrid', ListaJugadores).
ListaJugadores = [combinación óptima considerando química y restricciones].
```

### 5. `jugadores_disponibles/2`
Lista todos los jugadores que un equipo puede comprar.

```prolog
?- jugadores_disponibles('Manchester City', Lista).
Lista = ['Erling Haaland', 'Kevin De Bruyne', ...].
```

### 6. `jugadores_por_posicion/3`
Filtra jugadores disponibles por posición.

```prolog
?- jugadores_por_posicion('Real Madrid', delantero, Lista).
Lista = ['Robert Lewandowski', 'Karim Benzema', ...].
```

### 7. `quimica_entre/3`
Calcula la química entre dos jugadores.

```prolog
?- quimica_entre('Pedri', 'Gavi', Puntuacion).
Puntuacion = 9.
```

### 8. `rendimiento_con_quimica/2`
Calcula el rendimiento mejorado considerando química entre jugadores.

```prolog
?- rendimiento_con_quimica(['Pedri', 'Gavi'], Rendimiento).
Rendimiento = 20.9.
```

### 9. `cumple_reglas_liga/2`
Verifica si una combinación cumple todas las restricciones de liga.

```prolog
?- cumple_reglas_liga(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona').
true/false.
```

### 10. `analizar_combinacion/3`
Analiza una combinación mostrando todos sus aspectos.

```prolog
?- analizar_combinacion(['Pedri', 'Gavi'], 'Barcelona', Analisis).
Analisis = [costo=190, rendimiento_base=20, ...].
```

---

## 🧠 Conceptos de Programación Lógica Aplicados

### 1. Backtracking

Prolog utiliza **backtracking** automático para explorar todas las soluciones posibles. Cuando una consulta falla, retrocede y prueba alternativas.

**Ejemplo:**
```prolog
?- puede_firmar('Real Madrid', Jugador).
Jugador = 'Robert Lewandowski' ;  % Primera solución
Jugador = 'Karim Benzema' ;       % Backtracking encuentra otra
Jugador = 'Pedri' ;               % Y otra...
```

### 2. Unificación

La **unificación** permite que las variables se instancien con valores que hacen verdadera una consulta.

```prolog
?- jugador(Jugador, delantero, 25, Precio, _, _, _).
Jugador = 'Kylian Mbappé',
Precio = 180.
```

### 3. Recursión

Los predicados recursivos procesan listas y estructuras complejas:

```prolog
costo_total([], 0).
costo_total([Jugador|Resto], CostoTotal) :-
    precio_jugador(Jugador, Precio),
    costo_total(Resto, CostoSubtotal),
    CostoTotal is Precio + CostoSubtotal.
```

### 4. Restricciones

Las restricciones se modelan como condiciones que deben cumplirse:

```prolog
combinacion_valida(ListaJugadores, Equipo) :-
    todos_pueden_firmar(ListaJugadores, Equipo),
    cabe_en_presupuesto(ListaJugadores, Equipo),
    respeta_cupo_extranjeros(ListaJugadores, Equipo).
```

### 5. Generación de Combinaciones

El predicado `subconjunto/2` genera todas las combinaciones posibles mediante backtracking:

```prolog
subconjunto([], []).
subconjunto([X|Xs], [X|Ys]) :- subconjunto(Xs, Ys).
subconjunto(Xs, [_|Ys]) :- subconjunto(Xs, Ys).
```

---

## λ Complemento Funcional (Racket)

Para cubrir explícitamente contenidos del paradigma funcional del programa de la materia, se incluye:

- `functional/funcional_racket.rkt`
- `docs/COMPARATIVA_PROLOG_RACKET.md`

Este módulo funcional ahora implementa una versión comparativa real del problema:
- `puede-firmar?`, `recomendaciones`, `mejor-fichaje`, `comb-valida?`, `mejor-combinacion`
- modelado inmutable de datos (`struct jugador`, `struct equipo`)
- recursión explícita (`subconjuntos`) + funciones de orden superior (`map`, `filter`, `foldl`, `sort`)
- menú interactivo de consola para demo
- tests con `rackunit` (`raco test`)

Ejecutar:

```bash
racket functional/funcional_racket.rkt
raco test functional/funcional_racket.rkt
```

> Si `racket` no está instalado:
> - Ubuntu/Debian: `sudo apt install racket`

---

## 📊 Ejemplos de Ejecución

### Ejemplo 1: Verificar Fichaje

```prolog
?- puede_firmar('Real Madrid', 'Kylian Mbappé').
false.

?- puede_firmar('Real Madrid', 'Robert Lewandowski').
true.
```

**Explicación:** Mbappé cuesta 180M y excede el presupuesto de 200M si ya hay otros gastos, mientras que Lewandowski (25M) es asequible.

### Ejemplo 2: Recomendaciones

```prolog
?- recomendar('Barcelona', Jugador).
Jugador = 'Erling Haaland' ;
Jugador = 'Kylian Mbappé' ;
Jugador = 'Bukayo Saka' ;
...
```

**Explicación:** El sistema ordena jugadores por rendimiento (goles + asistencias) que pueden ser firmados.

### Ejemplo 3: Combinación Óptima

```prolog
?- combinacion_optima('Real Madrid', Lista).
Lista = ['Erling Haaland', 'Pedri', 'Ronald Araújo'].
```

**Explicación:** El sistema encuentra la combinación que maximiza el rendimiento total respetando presupuesto (200M) y cupo de extranjeros (5).

### Ejemplo 4: Filtrado por Posición

```prolog
?- jugadores_por_posicion('Real Madrid', delantero, Lista).
Lista = ['Robert Lewandowski', 'Karim Benzema', 'Cristiano Ronaldo'].
```

### Ejemplo 5: Análisis de Presupuesto

```prolog
?- presupuesto_restante('Real Madrid', ['Robert Lewandowski', 'Pedri'], Restante).
Restante = 75.
```

---

## 🔄 Comparación Conceptual: Prolog vs enfoque funcional (Racket/Scheme)

### Paradigma Declarativo

Ambos lenguajes son **declarativos**, pero con enfoques diferentes:

#### Prolog
- **Programación lógica**: Basada en relaciones y búsqueda de pruebas
- **Backtracking automático**: Explora todas las soluciones
- **Unificación**: Variables se instancian automáticamente
- **Búsqueda completa**: Encuentra todas las soluciones posibles

#### Racket/Scheme
- **Programación funcional**: Basada en funciones y transformaciones
- **Evaluación estricta**: Flujo de evaluación explícito
- **Tipado dinámico**: Flexibilidad para prototipado académico
- **Inmutabilidad**: Los datos no se modifican

### Ejemplo Conceptual: Filtrado de Jugadores

#### En Prolog:
```prolog
puede_firmar(Equipo, Jugador) :-
    puede_pagar(Equipo, Jugador),
    juega_posicion_necesaria(Jugador, Equipo).
```

**Características:**
- **Declarativo**: Describe QUÉ condiciones deben cumplirse
- **Bidireccional**: Puede encontrar jugadores para un equipo o equipos para un jugador
- **Backtracking**: Encuentra todas las soluciones automáticamente

#### En Racket (funcional):
```racket
(define (puede-firmar? eq j)
  (and (puede-pagar? eq j)
       (cubre-necesidad? eq j)
       (cumple-edad? eq j)))
```

**Características:**
- **Funcional**: Define una función que transforma entrada en salida
- **Unidireccional**: Calcula un valor booleano
- **Explícito**: Necesita `filter` o list comprehensions para encontrar todas las soluciones

### Ventajas de Prolog para este Dominio

1. **Búsqueda automática**: No necesita escribir loops o recursión explícita para encontrar soluciones
2. **Bidireccionalidad**: Los predicados funcionan en múltiples direcciones
3. **Backtracking integrado**: Explora el espacio de soluciones automáticamente
4. **Modelado natural**: Las relaciones se expresan de forma intuitiva

### Ventajas del enfoque funcional (Racket/Scheme) para este dominio

1. **Tipado fuerte**: Previene errores en tiempo de compilación
2. **Composabilidad**: Funciones pequeñas se combinan fácilmente
3. **Rendimiento**: Optimizaciones automáticas y evaluación perezosa
4. **Expresividad**: List comprehensions y funciones de orden superior

### Conclusión

**Prolog** es ideal para problemas de **búsqueda y restricciones** donde necesitamos explorar múltiples soluciones. El enfoque funcional en **Racket/Scheme** es fuerte para **transformaciones de datos**, composición y control explícito de estrategia. Este proyecto utiliza ambos enfoques de forma comparativa para cubrir los contenidos de la materia.

---

## 🎯 Decisiones de Diseño

### 1. Separación de Hechos y Reglas

**Decisión:** Separar `conocimiento.pl` (hechos) de `reglas.pl` (lógica).

**Razón:** Facilita el mantenimiento y permite actualizar la base de datos sin modificar la lógica.

### 2. Predicados Auxiliares

**Decisión:** Crear predicados auxiliares como `precio_jugador/2`, `edad_jugador/2`.

**Razón:** Mejora la legibilidad y permite reutilización de código.

### 3. Combinaciones Óptimas

**Decisión:** Usar `subconjunto/2` para generar combinaciones y verificar restricciones.

**Razón:** Aprovecha el backtracking de Prolog para explorar el espacio de soluciones sin algoritmos explícitos.

### 4. Rendimiento como Métrica

**Decisión:** Usar `goles + asistencias` como métrica de rendimiento.

**Razón:** Es una métrica simple y efectiva que permite comparar jugadores de diferentes posiciones.

### 5. Restricciones de Edad Opcionales

**Decisión:** Hacer las restricciones de edad opcionales usando `->` (implicación condicional).

**Razón:** No todos los equipos tienen restricciones de edad, y esto permite flexibilidad.

---

## 📝 Comentarios sobre el Código

### Estilo y Convensiones

- **Nombres descriptivos**: Los predicados tienen nombres claros que indican su propósito
- **Comentarios**: Cada sección y predicado importante está documentado
- **Modularidad**: El código está organizado en módulos lógicos
- **Consistencia**: Se sigue un estilo uniforme en todo el proyecto

### Predicados Recursivos

Los predicados recursivos siguen el patrón estándar:
1. **Caso base**: Define el resultado para la estructura vacía
2. **Caso recursivo**: Procesa el primer elemento y llama recursivamente

**Ejemplo:**
```prolog
costo_total([], 0).
costo_total([Jugador|Resto], CostoTotal) :-
    precio_jugador(Jugador, Precio),
    costo_total(Resto, CostoSubtotal),
    CostoTotal is Precio + CostoSubtotal.
```

---

## 🧪 Pruebas y Validación

### Consultas de Prueba

1. **Verificar restricciones básicas:**
   ```prolog
   ?- puede_firmar('Real Madrid', 'Kylian Mbappé').  % Debe fallar (presupuesto)
   ```

2. **Verificar filtrado:**
   ```prolog
   ?- jugadores_por_posicion('Barcelona', delantero, Lista).
   ```

3. **Verificar optimización:**
   ```prolog
   ?- combinacion_optima('Manchester City', Lista).
   ```

4. **Verificar restricciones complejas:**
   ```prolog
   ?- combinacion_valida(['Erling Haaland', 'Pedri'], 'Real Madrid').
   ```

### Suite automática (recomendada para entrega)

```bash
# Validación sintáctica base
swipl -q -f test_sintaxis.pl -t halt

# Tests lógicos en Prolog (plunit)
swipl -q -f tests/prolog_logic_tests.pl -g run_tests -t halt

# Tests del bridge Python-Prolog
python3 -m unittest tests/test_prolog_bridge.py -v

# Benchmark reproducible de consultas
python3 benchmarks/run_benchmarks.py
```

Resultados de benchmark:
- `benchmarks/latest_benchmark.csv`
- `benchmarks/latest_benchmark.md`

---

## ⚡ Funcionalidades Avanzadas

### Sistema de Química entre Jugadores

El sistema incluye un modelo de **química** que representa qué tan bien rinden juntos los jugadores:

- **Química explícita**: Combinaciones conocidas (ej: Pedri + Gavi = 9/10)
- **Química automática**: Misma nacionalidad = +3 puntos
- **Bonus de rendimiento**: La química mejora el rendimiento total

**Ejemplo:**
```prolog
?- quimica_entre('Pedri', 'Gavi', Puntuacion).
Puntuacion = 9.

?- rendimiento_con_quimica(['Pedri', 'Gavi'], Rendimiento).
Rendimiento = 20.9.  % 20 (base) + 0.9 (química)
```

Ver documentación completa en: `docs/QUIMICA_Y_LIGA.md`

### Restricciones de Liga y Competición

El sistema verifica que las combinaciones cumplan reglas de liga:

- **Límite de misma nacionalidad**: Máximo de jugadores de una nacionalidad
- **Cupo mínimo de cantera**: Mínimo de jugadores formados localmente
- **Límite de edad**: Balance generacional

**Ejemplo:**
```prolog
?- cumple_reglas_liga(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona').
false.  % Puede fallar por no cumplir cupo de cantera
```

Ver documentación completa en: `docs/QUIMICA_Y_LIGA.md`

## 🔮 Extensiones Futuras

Posibles mejoraciones al sistema:

1. **Restricciones de salario**: Agregar salarios y límites salariales
2. **Historial de lesiones**: Considerar jugadores con historial médico
3. **Compatibilidad de estilo**: Filtrar por estilo de juego
4. **Optimización multi-objetivo**: Balancear rendimiento, precio y edad
5. **Análisis temporal**: Considerar contratos y fechas de expiración

---

## 📚 Referencias

- **SWI-Prolog Documentation**: https://www.swi-prolog.org/pldoc/
- **Learn Prolog Now!**: http://www.learnprolognow.org/
- **Programming in Prolog** (Clocksin & Mellish)
- **Racket Documentation**: https://docs.racket-lang.org/
- **Revisión contra programa de la materia (UNNOBA)**: `docs/REVISION_PROGRAMA_UNNOBA.md`
- **Checklist de defensa final**: `docs/CHECKLIST_DEFENSA_FINAL.md`
- **Comparativa formal Prolog vs Racket**: `docs/COMPARATIVA_PROLOG_RACKET.md`

---

## 👤 Autor

Proyecto desarrollado para el curso de **Programación Lógica y Funcional**.

---

## 📄 Licencia

Este proyecto es de carácter académico y educativo.

---

## 🙏 Agradecimientos

Inspirado en el repositorio de referencia:
- [Sudoku Comparative Study](https://github.com/Ericthered123/sudoku-comparative-study)

---

**Última actualización:** 2026

