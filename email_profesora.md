# Email para Profesora - Propuesta de Proyecto

---

**Asunto:** Propuesta de Proyecto Final - Sistema Lógico de Compra de Jugadores de Fútbol en Prolog

---

Estimada Profesora [Nombre],

Espero que se encuentre bien. Me dirijo a usted para presentarle la propuesta de mi proyecto final para el curso de **Programación Lógica y Funcional**.

## Propuesta del Proyecto

He desarrollado un **Sistema Lógico de Compra de Jugadores de Fútbol en Prolog** que modela un mercado de transferencias utilizando el paradigma de programación lógica. El proyecto está inspirado en la estructura del repositorio de referencia del curso (Sudoku Comparative Study), pero aplicado a un dominio diferente y con funcionalidades adicionales.

## Objetivos y Alcance

El sistema permite:

1. **Modelado declarativo** del mercado de transferencias mediante hechos y reglas
2. **Evaluación de fichajes** considerando múltiples restricciones:
   - Presupuesto disponible
   - Necesidades de posición
   - Cupos de extranjeros
   - Restricciones de edad
   - **Restricciones de liga** (límites de nacionalidad, cupos de cantera)
3. **Sistema de química** entre jugadores que afecta el rendimiento
4. **Optimización de combinaciones** que maximiza el rendimiento total
5. **Consultas complejas** con filtrado por múltiples condiciones

## Conceptos de Programación Lógica Aplicados

El proyecto demuestra el uso de:

- ✅ **Hechos y reglas** para modelar el dominio
- ✅ **Backtracking** automático para explorar soluciones
- ✅ **Restricciones complejas** (presupuesto, cupos, reglas de liga)
- ✅ **Predicados recursivos** para procesar listas
- ✅ **Filtrado por múltiples condiciones**
- ✅ **Generación de combinaciones óptimas**
- ✅ **Unificación y búsqueda de pruebas**

## Estructura del Proyecto

El proyecto está organizado de forma clara y académica:

```
prolog/
├── src/
│   ├── conocimiento.pl      # Base de conocimiento (hechos)
│   ├── reglas.pl            # Reglas lógicas y predicados
│   └── sistema_compras.pl   # Archivo principal
├── examples/                # Ejemplos de consultas y ejecución
├── docs/                     # Documentación completa
└── README.md                 # Documentación académica
```

## Funcionalidades Principales

### Predicados Implementados:

1. **Consultas básicas:**
   - `puede_firmar/2` - Verifica si un equipo puede firmar a un jugador
   - `recomendar/2` - Recomienda jugadores ordenados por rendimiento
   - `mejor_fichaje/2` - Encuentra el mejor fichaje posible

2. **Consultas con listas:**
   - `jugadores_disponibles/2` - Lista jugadores disponibles
   - `jugadores_por_posicion/3` - Filtra por posición
   - `jugadores_por_edad/4` - Filtra por rango de edad

3. **Optimización:**
   - `combinacion_optima/2` - Genera combinaciones óptimas
   - `combinacion_valida/2` - Verifica validez de combinaciones

4. **Funcionalidades avanzadas:**
   - `quimica_entre/3` - Calcula química entre jugadores
   - `rendimiento_con_quimica/2` - Rendimiento mejorado
   - `cumple_reglas_liga/2` - Verifica restricciones de liga
   - `analizar_combinacion/3` - Análisis completo

## Aspectos Destacados

1. **Separación clara** entre base de conocimiento y reglas lógicas
2. **Documentación completa** con explicaciones de cada predicado
3. **Ejemplos de ejecución** con resultados esperados
4. **Comparación conceptual** con Haskell en el README
5. **Funcionalidades avanzadas** que demuestran dominio del paradigma

## Estado del Proyecto

El proyecto está **completamente funcional** y listo para ejecutarse en SWI-Prolog. Incluye:

- Base de conocimiento con 30+ jugadores y 6 equipos
- Más de 20 predicados implementados
- Sistema de restricciones complejas
- Sistema de química entre jugadores
- Documentación académica completa

## Solicitud

Me gustaría presentar este proyecto como trabajo final del curso. El código está disponible y puedo hacer una demostración en clase si lo considera apropiado.

¿Sería posible que revise el proyecto y me indique si cumple con los requisitos del curso? Estoy abierto a realizar ajustes o mejoras según sus indicaciones.

Quedo atento a su respuesta.

Saludos cordiales,

[Nombre del estudiante]
[Matrícula/Número de estudiante]
[Email de contacto]

---

**P.D.:** El proyecto incluye un README académico completo con explicaciones del enfoque lógico, decisiones de modelado, y una comparación conceptual con Haskell, similar al nivel del repositorio de referencia del curso.

