% ============================================================================
% SISTEMA DE COMPRA DE JUGADORES DE FÚTBOL - ARCHIVO PRINCIPAL
% ============================================================================
% Este es el archivo principal que carga toda la base de conocimiento
% y las reglas del sistema.
%
% Uso:
%   ?- consult('src/sistema_compras.pl').
%   o en SWI-Prolog:
%   ?- [src/sistema_compras].
% ============================================================================

% Cargar la base de conocimiento (hechos)
:- consult('src/conocimiento.pl').

% Cargar las reglas lógicas
:- consult('src/reglas.pl').

% Mensaje de bienvenida al cargar
:- initialization(mensaje_bienvenida).

mensaje_bienvenida :-
    writeln('========================================'),
    writeln('SISTEMA DE COMPRA DE JUGADORES DE FÚTBOL'),
    writeln('========================================'),
    writeln(''),
    writeln('Sistema cargado correctamente.'),
    writeln(''),
    writeln('Consultas disponibles:'),
    writeln('  ?- puede_firmar(Equipo, Jugador).'),
    writeln('  ?- recomendar(Equipo, Jugador).'),
    writeln('  ?- mejor_fichaje(Equipo, Jugador).'),
    writeln('  ?- combinacion_optima(Equipo, ListaJugadores).'),
    writeln('  ?- jugadores_disponibles(Equipo, Lista).'),
    writeln('  ?- jugadores_por_posicion(Equipo, Posicion, Lista).'),
    writeln(''),
    writeln('========================================').

