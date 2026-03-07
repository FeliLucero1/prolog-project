% Script de prueba de sintaxis
% Este archivo verifica que la sintaxis de los archivos sea correcta

% Intentar cargar los archivos
:- consult('src/conocimiento.pl').
:- consult('src/reglas.pl').

% Pruebas básicas de que los predicados existen
test_predicados :-
    writeln('Probando predicados básicos...'),
    
    % Verificar que existen jugadores
    (jugador(_, _, _, _, _, _, _) -> 
        writeln('✓ Hechos de jugadores cargados correctamente')
    ; 
        writeln('✗ Error: No se encontraron jugadores')
    ),
    
    % Verificar que existen equipos
    (presupuesto(_, _) -> 
        writeln('✓ Hechos de equipos cargados correctamente')
    ; 
        writeln('✗ Error: No se encontraron equipos')
    ),
    
    % Verificar predicados principales
    (predicate_property(puede_firmar(_, _), defined) -> 
        writeln('✓ Predicado puede_firmar/2 definido')
    ; 
        writeln('✗ Error: Predicado puede_firmar/2 no encontrado')
    ),
    
    (predicate_property(recomendar(_, _), defined) -> 
        writeln('✓ Predicado recomendar/2 definido')
    ; 
        writeln('✗ Error: Predicado recomendar/2 no encontrado')
    ),
    
    (predicate_property(combinacion_optima(_, _), defined) -> 
        writeln('✓ Predicado combinacion_optima/2 definido')
    ; 
        writeln('✗ Error: Predicado combinacion_optima/2 no encontrado')
    ),
    
    writeln(''),
    writeln('Pruebas de sintaxis completadas.').

% Ejecutar pruebas al cargar
:- initialization(test_predicados).

