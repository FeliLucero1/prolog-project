# Resumen de Ejemplos de Ejecución

## 📋 Consultas Básicas

### 1. Verificar Fichaje
```prolog
?- puede_firmar('Real Madrid', 'Robert Lewandowski').
true.

?- puede_firmar('Real Madrid', 'Kylian Mbappé').
false.
```

### 2. Recomendaciones
```prolog
?- recomendar('Barcelona', Jugador).
Jugador = 'Erling Haaland' ;
Jugador = 'Kylian Mbappé' ;
Jugador = 'Bukayo Saka' ;
...
```

### 3. Mejor Fichaje
```prolog
?- mejor_fichaje('Liverpool', Jugador).
Jugador = 'Bukayo Saka'.
```

## 📊 Consultas con Listas

### 4. Jugadores Disponibles
```prolog
?- jugadores_disponibles('Manchester City', Lista).
Lista = ['Erling Haaland', 'Kevin De Bruyne', ...].
```

### 5. Filtrar por Posición
```prolog
?- jugadores_por_posicion('Real Madrid', delantero, Lista).
Lista = ['Robert Lewandowski', 'Karim Benzema', 'Cristiano Ronaldo'].
```

### 6. Filtrar por Edad
```prolog
?- jugadores_por_edad('Barcelona', 20, 30, Lista).
Lista = ['Erling Haaland', 'Pedri', ...].
```

## 🔍 Consultas de Análisis

### 7. Restricciones de Extranjeros
```prolog
?- es_extranjero('Kylian Mbappé', 'Real Madrid').
true.

?- contar_extranjeros(['Erling Haaland', 'Pedri', 'Ronald Araújo'], 'Real Madrid', Cantidad).
Cantidad = 2.
```

### 8. Análisis de Presupuesto
```prolog
?- presupuesto_restante('Real Madrid', ['Robert Lewandowski', 'Pedri'], Restante).
Restante = 75.

?- costo_total(['Robert Lewandowski', 'Pedri'], Costo).
Costo = 125.
```

### 9. Jugadores Extremos
```prolog
?- jugador_mas_caro('Barcelona', Jugador).
Jugador = 'Erling Haaland'.

?- jugador_mas_barato('PSG', Jugador).
Jugador = 'Sergio Ramos'.
```

## 🎯 Consultas Avanzadas

### 10. Combinaciones Válidas
```prolog
?- combinacion_valida(['Robert Lewandowski', 'Pedri'], 'Real Madrid').
true.

?- combinacion_valida(['Erling Haaland', 'Pedri'], 'Real Madrid').
false.
```

### 11. Combinación Óptima
```prolog
?- combinacion_optima('Real Madrid', Lista).
Lista = [jugadores que maximizan rendimiento respetando restricciones].
```

### 12. Consultas Complejas
```prolog
% Jugadores jóvenes con buen rendimiento
?- jugador(Jugador, _, Edad, _, _, Goles, Asistencias),
   Edad < 25,
   Rendimiento is Goles + Asistencias,
   Rendimiento > 15.
```

## 💡 Tips de Uso

- **Backtracking**: Presiona `;` para ver más soluciones
- **Aceptar solución**: Presiona `.` o Enter
- **Salir**: Escribe `halt.`
- **Ayuda**: Escribe `help.` para ver comandos disponibles

## 🚀 Cómo Ejecutar

1. Instalar SWI-Prolog:
   ```bash
   sudo apt install swi-prolog
   ```

2. Iniciar Prolog:
   ```bash
   swipl
   ```

3. Cargar el sistema:
   ```prolog
   ?- [src/sistema_compras].
   ```

4. Ejecutar consultas:
   ```prolog
   ?- puede_firmar('Real Madrid', 'Robert Lewandowski').
   ```

