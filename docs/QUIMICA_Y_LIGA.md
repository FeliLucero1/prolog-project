# Sistema de Química y Restricciones de Liga

## 📋 Descripción

Este documento explica las nuevas funcionalidades agregadas al sistema:
1. **Restricciones de Liga y Competición**: Reglas que deben cumplir las combinaciones de jugadores
2. **Sistema de Química**: Compatibilidad entre jugadores que mejora el rendimiento

---

## 🏛️ Restricciones de Liga y Competición

### Tipos de Restricciones

#### 1. Límite de Misma Nacionalidad
Evita la concentración excesiva de jugadores de una misma nacionalidad.

**Ejemplo:**
```prolog
limite_misma_nacionalidad('Real Madrid', 3).
```
Significa que Real Madrid no puede tener más de 3 jugadores de la misma nacionalidad.

**Predicado:**
```prolog
respeta_limite_nacionalidad(ListaJugadores, Equipo).
```

#### 2. Cupo Mínimo de Cantera
Promueve el desarrollo de talento local exigiendo un mínimo de jugadores nacionales.

**Ejemplo:**
```prolog
cupo_minimo_cantera('Barcelona', 3).
```
Barcelona debe tener al menos 3 jugadores formados en cantera (españoles).

**Predicado:**
```prolog
cumple_cupo_cantera(ListaJugadores, Equipo).
```

#### 3. Límite de Jugadores Mayores
Balance generacional limitando jugadores mayores de cierta edad.

**Ejemplo:**
```prolog
limite_jugadores_mayores('Real Madrid', 35, 2).
```
Real Madrid no puede tener más de 2 jugadores mayores de 35 años.

**Predicado:**
```prolog
respeta_limite_edad(ListaJugadores, Equipo).
```

### Predicado Principal

```prolog
cumple_reglas_liga(ListaJugadores, Equipo).
```

Verifica que una combinación cumple **todas** las restricciones de liga:
- ✅ Límite de misma nacionalidad
- ✅ Cupo mínimo de cantera
- ✅ Límite de jugadores mayores

---

## ⚡ Sistema de Química

### Concepto

La **química** representa qué tan bien rinden juntos dos jugadores. Se mide en una escala de 1 a 10, donde 10 es máxima química.

### Tipos de Química

#### 1. Química Explícita
Definida manualmente para combinaciones conocidas.

**Ejemplos:**
```prolog
quimica('Pedri', 'Gavi', 9).  % Excelente química
quimica('Kevin De Bruyne', 'Erling Haaland', 9).
```

#### 2. Química Automática
Se calcula automáticamente cuando dos jugadores comparten:
- **Misma nacionalidad**: +3 puntos de química
- **Posiciones complementarias**: Se define explícitamente

### Predicados de Química

#### Calcular Química entre Dos Jugadores
```prolog
quimica_entre(Jugador1, Jugador2, Puntuacion).
```

Busca primero química explícita, luego calcula automática.

**Ejemplo:**
```prolog
?- quimica_entre('Pedri', 'Gavi', Puntuacion).
Puntuacion = 9.  % Química explícita

?- quimica_entre('Pedri', 'Rodri', Puntuacion).
Puntuacion = 3.  % Química automática (misma nacionalidad)
```

#### Calcular Química Total
```prolog
quimica_total(ListaJugadores, QuimicaTotal).
```

Suma la química entre todos los pares de jugadores en la lista.

**Ejemplo:**
```prolog
?- quimica_total(['Pedri', 'Gavi'], Quimica).
Quimica = 9.  % Química entre Pedri y Gavi
```

#### Rendimiento Mejorado
```prolog
rendimiento_con_quimica(ListaJugadores, RendimientoMejorado).
```

Calcula el rendimiento base y añade un bonus basado en la química total.

**Fórmula:**
```
Rendimiento Mejorado = Rendimiento Base + (Química Total × 0.1)
```

**Ejemplo:**
```prolog
?- rendimiento_total(['Pedri', 'Gavi'], Base),
   rendimiento_con_quimica(['Pedri', 'Gavi'], Mejorado).
Base = 20,      % 8+12 = 20
Mejorado = 20.9.  % 20 + (9 × 0.1) = 20.9
```

---

## 🔄 Integración con el Sistema

### Combinación Válida Actualizada

El predicado `combinacion_valida/2` ahora incluye verificación de reglas de liga:

```prolog
combinacion_valida(ListaJugadores, Equipo) :-
    todos_pueden_firmar(ListaJugadores, Equipo),
    cabe_en_presupuesto(ListaJugadores, Equipo),
    respeta_cupo_extranjeros(ListaJugadores, Equipo),
    cumple_reglas_liga(ListaJugadores, Equipo).  % ← NUEVO
```

### Combinación Óptima Actualizada

El predicado `combinacion_optima/2` ahora considera química:

```prolog
combinacion_optima(Equipo, ListaJugadores) :-
    ...
    rendimiento_con_quimica(ListaJugadores, RendimientoTotal),  % ← NUEVO
    ...
```

---

## 📊 Nuevos Predicados Disponibles

### Análisis de Combinaciones

```prolog
analizar_combinacion(ListaJugadores, Equipo, Analisis).
```

Retorna un análisis completo incluyendo:
- Costo total
- Rendimiento base
- Rendimiento mejorado (con química)
- Química total
- Cantidad de extranjeros
- Cantidad de cantera
- Si es válida

**Ejemplo:**
```prolog
?- analizar_combinacion(['Pedri', 'Gavi'], 'Barcelona', Analisis).
Analisis = [
    costo = 190,
    rendimiento_base = 20,
    rendimiento_mejorado = 20.9,
    quimica_total = 9,
    extranjeros = 0,
    cantera = 2,
    valida = true
].
```

### Combinaciones con Buena Química

```prolog
combinacion_con_quimica(Equipo, ListaJugadores, Umbral).
```

Encuentra combinaciones válidas con química total >= umbral.

**Ejemplo:**
```prolog
?- combinacion_con_quimica('Barcelona', Lista, 15).
Lista = [combinaciones con química >= 15].
```

---

## 🎯 Ejemplos de Uso

### Ejemplo 1: Verificar Restricciones
```prolog
?- cumple_reglas_liga(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona').
false.  % Puede fallar por cupo de cantera (necesita 3, tiene 2)
```

### Ejemplo 2: Calcular Química
```prolog
?- quimica_total(['Pedri', 'Gavi', 'Robert Lewandowski'], Quimica).
Quimica = [suma de todas las quimicas entre pares].
```

### Ejemplo 3: Rendimiento con Química
```prolog
?- rendimiento_con_quimica(['Kevin De Bruyne', 'Erling Haaland'], Rendimiento).
Rendimiento = 60.9.  % 60 (base) + 0.9 (química)
```

### Ejemplo 4: Combinación Óptima
```prolog
?- combinacion_optima('Barcelona', Lista).
Lista = [combinación que maximiza rendimiento + química].
```

---

## 🔍 Detalles de Implementación

### Cálculo de Química Total

La química total se calcula sumando la química entre todos los pares de jugadores:

```
Química Total = Σ quimica(Jugador_i, Jugador_j) para todo i < j
```

### Bonus de Rendimiento

El bonus se calcula como:
```
Bonus = Química Total × 0.1
```

Esto significa que cada punto de química añade 0.1 al rendimiento total.

### Verificación de Restricciones

Las restricciones se verifican en este orden:
1. Límite de nacionalidad
2. Cupo mínimo de cantera
3. Límite de edad

Si alguna falla, la combinación no es válida.

---

## 📝 Notas Importantes

1. **Química Bidireccional**: Si `quimica(A, B, 9)`, también se asume `quimica(B, A, 9)`.

2. **Química Automática**: Solo se aplica si no hay química explícita definida.

3. **Restricciones Opcionales**: Si un equipo no tiene una restricción definida, se considera cumplida.

4. **Rendimiento Mejorado**: Solo se usa en `combinacion_optima`, no afecta otros predicados.

---

## 🚀 Extensibilidad

El sistema es fácilmente extensible:

- **Agregar más restricciones**: Añadir hechos y predicados de verificación
- **Agregar más química**: Añadir hechos `quimica/3`
- **Modificar fórmulas**: Cambiar el cálculo de bonus en `rendimiento_con_quimica`

---

**Última actualización:** 2024

