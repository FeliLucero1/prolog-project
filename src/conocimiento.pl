% ============================================================================
% BASE DE CONOCIMIENTO - SISTEMA DE COMPRA DE JUGADORES DE FÚTBOL
% ============================================================================
% Este archivo contiene todos los hechos del sistema:
% - Información de jugadores disponibles en el mercado
% - Información de equipos (presupuestos, necesidades, cupos)
% ============================================================================

% ----------------------------------------------------------------------------
% HECHOS: JUGADORES
% ----------------------------------------------------------------------------
% jugador(Nombre, Posicion, Edad, Precio, Nacionalidad, Goles, Asistencias)
% 
% Posiciones posibles: portero, defensa, mediocampista, delantero
% Precio en millones de euros
% Goles y asistencias son estadísticas de la temporada anterior

jugador('Lionel Messi', delantero, 36, 50, argentina, 25, 18).
jugador('Cristiano Ronaldo', delantero, 39, 30, portugal, 28, 12).
jugador('Kylian Mbappé', delantero, 25, 180, francia, 35, 10).
jugador('Erling Haaland', delantero, 24, 150, noruega, 40, 8).
jugador('Robert Lewandowski', delantero, 35, 25, polonia, 30, 6).
jugador('Karim Benzema', delantero, 36, 20, francia, 22, 9).

jugador('Kevin De Bruyne', mediocampista, 33, 80, belgica, 12, 20).
jugador('Luka Modrić', mediocampista, 38, 15, croacia, 5, 10).
jugador('Bruno Fernandes', mediocampista, 29, 70, portugal, 15, 18).
jugador('Pedri', mediocampista, 21, 100, espana, 8, 12).
jugador('Jude Bellingham', mediocampista, 21, 120, inglaterra, 10, 8).
jugador('Federico Valverde', mediocampista, 26, 90, uruguay, 7, 9).
jugador('Rodri', mediocampista, 28, 85, espana, 4, 6).
jugador('Toni Kroos', mediocampista, 34, 20, alemania, 3, 8).

jugador('Virgil van Dijk', defensa, 33, 40, holanda, 2, 1).
jugador('Rúben Dias', defensa, 27, 75, portugal, 1, 2).
jugador('Marquinhos', defensa, 30, 60, brasil, 3, 1).
jugador('Alessandro Bastoni', defensa, 25, 55, italia, 2, 3).
jugador('Ronald Araújo', defensa, 25, 70, uruguay, 1, 1).
jugador('David Alaba', defensa, 32, 35, austria, 2, 4).
jugador('Theo Hernández', defensa, 26, 50, francia, 4, 6).

jugador('Alisson', portero, 32, 50, brasil, 0, 0).
jugador('Thibaut Courtois', portero, 32, 45, belgica, 0, 0).
jugador('Marc-André ter Stegen', portero, 32, 40, alemania, 0, 0).
jugador('Jan Oblak', portero, 31, 35, eslovenia, 0, 0).
jugador('Gianluigi Donnarumma', portero, 25, 60, italia, 0, 0).

% Jugadores jóvenes con potencial
jugador('Gavi', mediocampista, 20, 90, espana, 5, 7).
jugador('Eduardo Camavinga', mediocampista, 21, 80, francia, 2, 4).
jugador('Jamal Musiala', mediocampista, 21, 100, alemania, 12, 8).
jugador('Bukayo Saka', delantero, 22, 120, inglaterra, 18, 15).

% Jugadores económicos
jugador('Sergio Ramos', defensa, 38, 5, espana, 1, 0).
jugador('Iker Casillas', portero, 43, 2, espana, 0, 0).
jugador('Neymar', delantero, 32, 45, brasil, 20, 14).
jugador('Frenkie de Jong', mediocampista, 27, 80, holanda, 4, 7).

% Nuevos jugadores para ampliar el mercado
jugador('Vinicius Junior', delantero, 24, 170, brasil, 24, 12).
jugador('Mohamed Salah', delantero, 32, 75, egipto, 27, 11).
jugador('Lautaro Martinez', delantero, 27, 95, argentina, 30, 6).
jugador('Harry Kane', delantero, 31, 100, inglaterra, 33, 8).
jugador('Antoine Griezmann', delantero, 33, 45, francia, 18, 12).

jugador('Martin Odegaard', mediocampista, 26, 90, noruega, 10, 15).
jugador('Declan Rice', mediocampista, 26, 95, inglaterra, 6, 7).
jugador('Bernardo Silva', mediocampista, 30, 85, portugal, 9, 11).
jugador('Florian Wirtz', mediocampista, 21, 110, alemania, 13, 14).
jugador('Enzo Fernandez', mediocampista, 24, 95, argentina, 5, 8).
jugador('Cole Palmer', mediocampista, 22, 95, inglaterra, 22, 13).
jugador('Lamine Yamal', delantero, 17, 130, espana, 12, 16).

jugador('William Saliba', defensa, 23, 85, francia, 2, 2).
jugador('Lisandro Martinez', defensa, 26, 65, argentina, 1, 2).
jugador('Antonio Rudiger', defensa, 31, 50, alemania, 2, 1).
jugador('Pau Cubarsi', defensa, 18, 70, espana, 0, 2).
jugador('Joao Cancelo', defensa, 30, 55, portugal, 4, 7).

jugador('Emiliano Martinez', portero, 32, 45, argentina, 0, 0).
jugador('Mike Maignan', portero, 29, 55, francia, 0, 0).
jugador('Ederson', portero, 31, 40, brasil, 0, 0).

% ----------------------------------------------------------------------------
% HECHOS: EQUIPOS Y SUS CARACTERÍSTICAS
% ----------------------------------------------------------------------------

% Necesidades de posiciones por equipo
necesita('Real Madrid', delantero).
necesita('Real Madrid', mediocampista).
necesita('Barcelona', delantero).
necesita('Barcelona', defensa).
necesita('Manchester City', mediocampista).
necesita('Manchester City', defensa).
necesita('Bayern Munich', portero).
necesita('Bayern Munich', defensa).
necesita('PSG', mediocampista).
necesita('PSG', defensa).
necesita('Liverpool', delantero).
necesita('Liverpool', mediocampista).

% Presupuestos de los equipos (en millones de euros)
presupuesto('Real Madrid', 200).
presupuesto('Barcelona', 150).
presupuesto('Manchester City', 300).
presupuesto('Bayern Munich', 180).
presupuesto('PSG', 250).
presupuesto('Liverpool', 120).

% Cupos de extranjeros (máximo permitido)
cupo_extranjeros('Real Madrid', 5).
cupo_extranjeros('Barcelona', 4).
cupo_extranjeros('Manchester City', 6).
cupo_extranjeros('Bayern Munich', 4).
cupo_extranjeros('PSG', 7).
cupo_extranjeros('Liverpool', 5).

% Nacionalidad de los equipos (para determinar si un jugador es extranjero)
nacionalidad_equipo('Real Madrid', espana).
nacionalidad_equipo('Barcelona', espana).
nacionalidad_equipo('Manchester City', inglaterra).
nacionalidad_equipo('Bayern Munich', alemania).
nacionalidad_equipo('PSG', francia).
nacionalidad_equipo('Liverpool', inglaterra).

% ----------------------------------------------------------------------------
% HECHOS AUXILIARES: RESTRICCIONES ADICIONALES
% ----------------------------------------------------------------------------

% Edad mínima requerida por algunos equipos
edad_minima('Real Madrid', 20).
edad_minima('Barcelona', 18).

% Edad máxima preferida por algunos equipos
edad_maxima('Bayern Munich', 32).
edad_maxima('Liverpool', 30).

% ----------------------------------------------------------------------------
% HECHOS: RESTRICCIONES DE LIGA Y COMPETICIÓN
% ----------------------------------------------------------------------------

% Límite máximo de jugadores de la misma nacionalidad por equipo
% (Para evitar concentración excesiva de una nacionalidad)
limite_misma_nacionalidad('Real Madrid', 3).
limite_misma_nacionalidad('Barcelona', 3).
limite_misma_nacionalidad('Manchester City', 4).
limite_misma_nacionalidad('Bayern Munich', 3).
limite_misma_nacionalidad('PSG', 4).
limite_misma_nacionalidad('Liverpool', 3).

% Cupo mínimo de jugadores formados en cantera (jugadores nacionales del país del equipo)
% Esto promueve el desarrollo de talento local
cupo_minimo_cantera('Real Madrid', 2).
cupo_minimo_cantera('Barcelona', 3).
cupo_minimo_cantera('Manchester City', 2).
cupo_minimo_cantera('Bayern Munich', 2).
cupo_minimo_cantera('PSG', 2).
cupo_minimo_cantera('Liverpool', 2).

% Límite máximo de jugadores mayores de cierta edad (para balance generacional)
limite_jugadores_mayores('Real Madrid', 35, 2).
limite_jugadores_mayores('Barcelona', 35, 2).
limite_jugadores_mayores('Liverpool', 32, 3).

% ----------------------------------------------------------------------------
% HECHOS: QUÍMICA Y COMPATIBILIDAD ENTRE JUGADORES
% ----------------------------------------------------------------------------
% quimica(Jugador1, Jugador2, Puntuacion)
% Puntuacion de 1 a 10, donde 10 es máxima química
% Representa qué tan bien rinden juntos estos jugadores

% Combinaciones conocidas con excelente química
quimica('Lionel Messi', 'Neymar', 10).
quimica('Neymar', 'Lionel Messi', 10).
quimica('Kevin De Bruyne', 'Erling Haaland', 9).
quimica('Erling Haaland', 'Kevin De Bruyne', 9).
quimica('Pedri', 'Gavi', 9).
quimica('Gavi', 'Pedri', 9).
quimica('Bruno Fernandes', 'Cristiano Ronaldo', 8).
quimica('Cristiano Ronaldo', 'Bruno Fernandes', 8).
quimica('Federico Valverde', 'Rodri', 8).
quimica('Rodri', 'Federico Valverde', 8).

% Química por misma nacionalidad (bonificación automática)
% Se calcula dinámicamente, pero aquí definimos casos especiales
quimica('Virgil van Dijk', 'Frenkie de Jong', 7).
quimica('Frenkie de Jong', 'Virgil van Dijk', 7).

% Química por complementariedad de posiciones
quimica('Robert Lewandowski', 'Kevin De Bruyne', 8).
quimica('Kevin De Bruyne', 'Robert Lewandowski', 8).
quimica('Kylian Mbappé', 'Bruno Fernandes', 7).
quimica('Bruno Fernandes', 'Kylian Mbappé', 7).
quimica('Erling Haaland', 'Jude Bellingham', 8).
quimica('Jude Bellingham', 'Erling Haaland', 8).

% Química entre defensores y mediocampistas
quimica('Virgil van Dijk', 'Rodri', 7).
quimica('Rodri', 'Virgil van Dijk', 7).
quimica('Rúben Dias', 'Bruno Fernandes', 7).
quimica('Bruno Fernandes', 'Rúben Dias', 7).

