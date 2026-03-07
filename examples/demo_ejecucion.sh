#!/bin/bash
# Script de demostración de ejecución del sistema
# Este script muestra ejemplos de cómo ejecutar consultas en SWI-Prolog

echo "=================================================================================="
echo "DEMOSTRACIÓN DE EJECUCIÓN - SISTEMA DE COMPRA DE JUGADORES"
echo "=================================================================================="
echo ""
echo "Para ejecutar estos ejemplos, necesitas SWI-Prolog instalado:"
echo "  sudo apt install swi-prolog"
echo ""
echo "Luego ejecuta:"
echo "  swipl"
echo "  ?- [src/sistema_compras]."
echo ""
echo "=================================================================================="
echo "EJEMPLOS DE CONSULTAS Y RESULTADOS ESPERADOS:"
echo "=================================================================================="
echo ""

cat << 'EOF'
EJEMPLO 1: Verificar si un equipo puede firmar a un jugador
--------------------------------------------------------------------------------
?- puede_firmar('Real Madrid', 'Robert Lewandowski').
true.

?- puede_firmar('Real Madrid', 'Kylian Mbappé').
false.

Explicación: Lewandowski (25M) cabe en el presupuesto de Real Madrid (200M),
mientras que Mbappé (180M) podría excederlo dependiendo de otras compras.

--------------------------------------------------------------------------------

EJEMPLO 2: Obtener recomendaciones (presiona ; para ver más)
--------------------------------------------------------------------------------
?- recomendar('Barcelona', Jugador).
Jugador = 'Erling Haaland' ;
Jugador = 'Kylian Mbappé' ;
Jugador = 'Bukayo Saka' ;
Jugador = 'Robert Lewandowski' ;
Jugador = 'Karim Benzema' ;
Jugador = 'Cristiano Ronaldo' ;
false.

Explicación: Jugadores ordenados por rendimiento (goles + asistencias)
que Barcelona puede comprar.

--------------------------------------------------------------------------------

EJEMPLO 3: Encontrar el mejor fichaje
--------------------------------------------------------------------------------
?- mejor_fichaje('Liverpool', Jugador).
Jugador = 'Bukayo Saka'.

Explicación: Saka tiene el mayor rendimiento (18+15=33) entre los jugadores
que Liverpool puede comprar con su presupuesto de 120M.

--------------------------------------------------------------------------------

EJEMPLO 4: Listar todos los jugadores disponibles
--------------------------------------------------------------------------------
?- jugadores_disponibles('Manchester City', Lista).
Lista = ['Erling Haaland', 'Kevin De Bruyne', 'Bruno Fernandes', 'Pedri', 
         'Jude Bellingham', 'Federico Valverde', 'Rodri', 'Rúben Dias', 
         'Marquinhos', 'Alessandro Bastoni', 'Ronald Araújo', 'Theo Hernández', 
         'Alisson', 'Thibaut Courtois', 'Marc-André ter Stegen', 'Jan Oblak', 
         'Gianluigi Donnarumma', 'Gavi', 'Eduardo Camavinga', 'Jamal Musiala', 
         'Bukayo Saka'].

--------------------------------------------------------------------------------

EJEMPLO 5: Filtrar jugadores por posición
--------------------------------------------------------------------------------
?- jugadores_por_posicion('Real Madrid', delantero, Lista).
Lista = ['Robert Lewandowski', 'Karim Benzema', 'Cristiano Ronaldo'].

?- jugadores_por_posicion('Real Madrid', mediocampista, Lista).
Lista = ['Kevin De Bruyne', 'Bruno Fernandes', 'Pedri', 'Jude Bellingham', 
         'Federico Valverde', 'Rodri', 'Toni Kroos', 'Gavi', 'Eduardo Camavinga', 
         'Jamal Musiala'].

--------------------------------------------------------------------------------

EJEMPLO 6: Filtrar por rango de edad
--------------------------------------------------------------------------------
?- jugadores_por_edad('Barcelona', 20, 30, Lista).
Lista = ['Erling Haaland', 'Pedri', 'Jude Bellingham', 'Federico Valverde', 
         'Rodri', 'Alessandro Bastoni', 'Ronald Araújo', 'Theo Hernández', 
         'Gianluigi Donnarumma', 'Gavi', 'Eduardo Camavinga', 'Jamal Musiala', 
         'Bukayo Saka'].

--------------------------------------------------------------------------------

EJEMPLO 7: Verificar restricciones de extranjeros
--------------------------------------------------------------------------------
?- es_extranjero('Kylian Mbappé', 'Real Madrid').
true.

?- es_nacional('Pedri', 'Barcelona').
true.

?- contar_extranjeros(['Erling Haaland', 'Pedri', 'Ronald Araújo'], 'Real Madrid', Cantidad).
Cantidad = 2.

Explicación: Haaland (noruega) y Araújo (uruguay) son extranjeros para Real Madrid.

--------------------------------------------------------------------------------

EJEMPLO 8: Análisis de presupuesto
--------------------------------------------------------------------------------
?- presupuesto_restante('Real Madrid', ['Robert Lewandowski'], Restante).
Restante = 175.

?- presupuesto_restante('Real Madrid', ['Robert Lewandowski', 'Pedri'], Restante).
Restante = 75.

?- costo_total(['Robert Lewandowski', 'Pedri'], Costo).
Costo = 125.

--------------------------------------------------------------------------------

EJEMPLO 9: Jugador más caro y más barato
--------------------------------------------------------------------------------
?- jugador_mas_caro('Barcelona', Jugador).
Jugador = 'Erling Haaland'.

?- jugador_mas_barato('PSG', Jugador).
Jugador = 'Sergio Ramos'.

--------------------------------------------------------------------------------

EJEMPLO 10: Consultas complejas con múltiples condiciones
--------------------------------------------------------------------------------
% Jugadores jóvenes con buen rendimiento
?- jugador(Jugador, _, Edad, _, _, Goles, Asistencias),
   Edad < 25,
   Rendimiento is Goles + Asistencias,
   Rendimiento > 15.
Jugador = 'Kylian Mbappé',
Edad = 25,
Goles = 35,
Asistencias = 10,
Rendimiento = 45 ;
Jugador = 'Erling Haaland',
Edad = 24,
Goles = 40,
Asistencias = 8,
Rendimiento = 48 ;
Jugador = 'Bukayo Saka',
Edad = 22,
Goles = 18,
Asistencias = 15,
Rendimiento = 33 ;
...

--------------------------------------------------------------------------------

EJEMPLO 11: Verificar combinaciones válidas
--------------------------------------------------------------------------------
?- combinacion_valida(['Robert Lewandowski', 'Pedri'], 'Real Madrid').
true.

?- combinacion_valida(['Erling Haaland', 'Pedri'], 'Real Madrid').
false.

Explicación: La segunda combinación excede el presupuesto (150+100=250 > 200).

--------------------------------------------------------------------------------

EJEMPLO 12: Buscar combinaciones de 2 jugadores
--------------------------------------------------------------------------------
?- puede_firmar('Real Madrid', J1),
   puede_firmar('Real Madrid', J2),
   J1 \= J2,
   combinacion_valida([J1, J2], 'Real Madrid').
J1 = 'Robert Lewandowski',
J2 = 'Pedri' ;
J1 = 'Robert Lewandowski',
J2 = 'Jude Bellingham' ;
J1 = 'Robert Lewandowski',
J2 = 'Federico Valverde' ;
...

EOF

echo ""
echo "=================================================================================="
echo "FIN DE LA DEMOSTRACIÓN"
echo "=================================================================================="

