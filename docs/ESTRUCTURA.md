# Estructura del Proyecto

## Organización de Archivos

```
prolog/
│
├── src/                          # Código fuente
│   ├── conocimiento.pl          # Base de conocimiento (hechos)
│   ├── reglas.pl                # Reglas lógicas y predicados
│   └── sistema_compras.pl       # Archivo principal (carga todo)
│
├── examples/                     # Ejemplos y pruebas
│   ├── consultas.pl             # Ejemplos de consultas comentadas
│   └── ejecucion_ejemplo.txt    # Salidas esperadas de ejecución
│
├── docs/                         # Documentación adicional
│   └── ESTRUCTURA.md            # Este archivo
│
├── README.md                     # Documentación principal del proyecto
└── QUICKSTART.md                 # Guía rápida de inicio
```

## Descripción de Archivos

### `src/conocimiento.pl`
Contiene todos los **hechos** del sistema:
- Información de jugadores (nombre, posición, edad, precio, nacionalidad, estadísticas)
- Información de equipos (presupuestos, necesidades, cupos de extranjeros)
- Restricciones adicionales (edades mínimas/máximas)

**Tipo:** Base de datos declarativa

### `src/reglas.pl`
Contiene todas las **reglas** y **predicados** del sistema:
- Predicados auxiliares (obtener precio, edad, rendimiento)
- Predicados de restricciones (puede pagar, cumple edad, etc.)
- Predicados principales (puede_firmar, recomendar, mejor_fichaje)
- Predicados de optimización (combinacion_optima)
- Predicados de análisis (jugadores_disponibles, filtros)

**Tipo:** Lógica de negocio

### `src/sistema_compras.pl`
Archivo principal que:
- Carga la base de conocimiento
- Carga las reglas
- Muestra mensaje de bienvenida

**Uso:** Punto de entrada al sistema

### `examples/consultas.pl`
Ejemplos comentados de consultas que se pueden realizar al sistema.

### `examples/ejecucion_ejemplo.txt`
Salidas esperadas de diferentes consultas, útil para verificar el comportamiento del sistema.

## Flujo de Uso

1. **Cargar el sistema:**
   ```prolog
   ?- [src/sistema_compras].
   ```

2. **Realizar consultas:**
   ```prolog
   ?- puede_firmar('Real Madrid', 'Robert Lewandowski').
   ```

3. **Explorar soluciones:**
   - Presionar `;` para ver más soluciones (backtracking)
   - Presionar `.` para aceptar una solución

## Principios de Diseño

1. **Separación de concerns:** Hechos separados de reglas
2. **Modularidad:** Cada archivo tiene una responsabilidad clara
3. **Documentación:** Comentarios explicativos en cada sección
4. **Extensibilidad:** Fácil agregar nuevos jugadores o equipos

