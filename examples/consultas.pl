% ============================================================================
% EJEMPLOS DE CONSULTAS - SISTEMA DE COMPRA DE JUGADORES
% ============================================================================
% Este archivo contiene ejemplos de consultas que se pueden realizar
% al sistema. Copia y pega estas consultas en la consola de SWI-Prolog
% después de cargar el sistema.
% ============================================================================

% Para cargar el sistema primero:
% ?- [src/sistema_compras].

% ============================================================================
% CONSULTAS BÁSICAS
% ============================================================================

% 1. Verificar si un equipo puede firmar a un jugador específico
% ?- puede_firmar('Real Madrid', 'Kylian Mbappé').
% Resultado esperado: false (excede presupuesto)

% ?- puede_firmar('Real Madrid', 'Robert Lewandowski').
% Resultado esperado: true

% 2. Obtener recomendaciones para un equipo
% ?- recomendar('Barcelona', Jugador).
% Resultado: Lista de jugadores recomendados ordenados por rendimiento

% 3. Encontrar el mejor fichaje para un equipo
% ?- mejor_fichaje('Liverpool', Jugador).
% Resultado: El jugador con mayor rendimiento que puede ser firmado

% ============================================================================
% CONSULTAS CON LISTAS
% ============================================================================

% 4. Ver todos los jugadores disponibles para un equipo
% ?- jugadores_disponibles('Manchester City', Lista).
% Resultado: Lista con todos los jugadores que puede comprar

% 5. Filtrar jugadores por posición
% ?- jugadores_por_posicion('Real Madrid', delantero, Lista).
% Resultado: Lista de delanteros disponibles

% 6. Filtrar jugadores por rango de edad
% ?- jugadores_por_edad('Barcelona', 20, 30, Lista).
% Resultado: Jugadores entre 20 y 30 años

% ============================================================================
% CONSULTAS DE OPTIMIZACIÓN
% ============================================================================

% 7. Encontrar combinación óptima de fichajes
% ?- combinacion_optima('Real Madrid', ListaJugadores).
% Resultado: Mejor combinación de jugadores que maximiza rendimiento

% 8. Verificar si una combinación específica es válida
% ?- combinacion_valida(['Robert Lewandowski', 'Pedri'], 'Real Madrid').
% Resultado: true o false según restricciones

% ============================================================================
% CONSULTAS DE ANÁLISIS
% ============================================================================

% 9. Encontrar el jugador más caro disponible
% ?- jugador_mas_caro('Barcelona', Jugador).

% 10. Encontrar el jugador más barato disponible
% ?- jugador_mas_barato('PSG', Jugador).

% 11. Calcular presupuesto restante después de compras
% ?- presupuesto_restante('Real Madrid', ['Robert Lewandowski', 'Pedri'], Restante).

% ============================================================================
% CONSULTAS DE EXPLORACIÓN
% ============================================================================

% 12. Ver todos los jugadores de una nacionalidad
% ?- jugador(Jugador, _, _, _, argentina, _, _).

% 13. Ver todos los jugadores de una posición
% ?- jugador(Jugador, delantero, _, _, _, _, _).

% 14. Ver jugadores con alto rendimiento
% ?- jugador(Jugador, _, _, _, _, Goles, Asistencias),
%    Rendimiento is Goles + Asistencias,
%    Rendimiento > 30.

% ============================================================================
% CONSULTAS COMPLEJAS
% ============================================================================

% 15. Encontrar jugadores jóvenes con buen rendimiento
% ?- jugador(Jugador, _, Edad, _, _, Goles, Asistencias),
%    Edad < 25,
%    Rendimiento is Goles + Asistencias,
%    Rendimiento > 15.

% 16. Encontrar combinaciones de 2 jugadores para un equipo
% ?- puede_firmar('Real Madrid', J1),
%    puede_firmar('Real Madrid', J2),
%    J1 \= J2,
%    combinacion_valida([J1, J2], 'Real Madrid').

% 17. Verificar restricciones de extranjeros
% ?- es_extranjero('Kylian Mbappé', 'Real Madrid').
% Resultado: true (francés para equipo español)

% ?- es_nacional('Pedri', 'Barcelona').
% Resultado: true (español para equipo español)

