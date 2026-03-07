% ============================================================================
% REGLAS LÓGICAS - SISTEMA DE COMPRA DE JUGADORES DE FÚTBOL
% ============================================================================
% Este archivo contiene todas las reglas y predicados del sistema.
% Implementa la lógica de negocio usando el paradigma declarativo de Prolog.
% ============================================================================

% ----------------------------------------------------------------------------
% PREDICADOS AUXILIARES
% ----------------------------------------------------------------------------

% Verifica si un jugador es extranjero para un equipo dado
% Un jugador es extranjero si su nacionalidad difiere de la del equipo
es_extranjero(Jugador, Equipo) :-
    jugador(Jugador, _, _, _, NacionalidadJugador, _, _),
    nacionalidad_equipo(Equipo, NacionalidadEquipo),
    NacionalidadJugador \= NacionalidadEquipo.

% Verifica si un jugador es nacional para un equipo dado
es_nacional(Jugador, Equipo) :-
    jugador(Jugador, _, _, _, NacionalidadJugador, _, _),
    nacionalidad_equipo(Equipo, NacionalidadEquipo),
    NacionalidadJugador = NacionalidadEquipo.

% Obtiene el precio de un jugador
precio_jugador(Jugador, Precio) :-
    jugador(Jugador, _, _, Precio, _, _, _).

% Obtiene la posición de un jugador
posicion_jugador(Jugador, Posicion) :-
    jugador(Jugador, Posicion, _, _, _, _, _).

% Obtiene la edad de un jugador
edad_jugador(Jugador, Edad) :-
    jugador(Jugador, _, Edad, _, _, _, _).

% Calcula el rendimiento de un jugador (goles + asistencias)
rendimiento(Jugador, Rendimiento) :-
    jugador(Jugador, _, _, _, _, Goles, Asistencias),
    Rendimiento is Goles + Asistencias.

% Obtiene el presupuesto de un equipo
presupuesto_equipo(Equipo, Presupuesto) :-
    presupuesto(Equipo, Presupuesto).

% Obtiene el cupo de extranjeros de un equipo
cupo_extranjeros_equipo(Equipo, Cupo) :-
    cupo_extranjeros(Equipo, Cupo).

% Verifica si un equipo necesita una posición específica
equipo_necesita(Equipo, Posicion) :-
    necesita(Equipo, Posicion).

% ----------------------------------------------------------------------------
% PREDICADOS PRINCIPALES: RESTRICCIONES Y FILTROS
% ----------------------------------------------------------------------------

% Verifica si un jugador cumple con la restricción de edad mínima del equipo
cumple_edad_minima(Jugador, Equipo) :-
    edad_jugador(Jugador, Edad),
    (edad_minima(Equipo, EdadMin) -> Edad >= EdadMin; true).

% Verifica si un jugador cumple con la restricción de edad máxima del equipo
cumple_edad_maxima(Jugador, Equipo) :-
    edad_jugador(Jugador, Edad),
    (edad_maxima(Equipo, EdadMax) -> Edad =< EdadMax; true).

% Verifica si un jugador cumple con todas las restricciones de edad
cumple_restricciones_edad(Jugador, Equipo) :-
    cumple_edad_minima(Jugador, Equipo),
    cumple_edad_maxima(Jugador, Equipo).

% Verifica si un equipo puede pagar el precio de un jugador
puede_pagar(Equipo, Jugador) :-
    presupuesto_equipo(Equipo, Presupuesto),
    precio_jugador(Jugador, Precio),
    Presupuesto >= Precio.

% Verifica si un jugador juega en una posición que el equipo necesita
juega_posicion_necesaria(Jugador, Equipo) :-
    posicion_jugador(Jugador, Posicion),
    equipo_necesita(Equipo, Posicion).

% ----------------------------------------------------------------------------
% PREDICADO PRINCIPAL: puede_firmar/2
% ----------------------------------------------------------------------------
% Determina si un equipo puede firmar a un jugador, considerando:
% - Presupuesto disponible
% - Posición necesitada
% - Restricciones de edad (si existen)
% NOTA: No verifica cupo de extranjeros aquí, se hace en combinaciones

puede_firmar(Equipo, Jugador) :-
    puede_pagar(Equipo, Jugador),
    juega_posicion_necesaria(Jugador, Equipo),
    cumple_restricciones_edad(Jugador, Equipo).

% ----------------------------------------------------------------------------
% PREDICADO: recomendar/2
% ----------------------------------------------------------------------------
% Recomienda jugadores para un equipo basándose en:
% - Que pueda firmarlos (presupuesto, posición, edad)
% - Ordenados por rendimiento (goles + asistencias) descendente
%
% Usa setof para obtener jugadores ordenados por rendimiento de forma eficiente

recomendar(Equipo, Jugador) :-
    % Obtenemos todos los jugadores con su rendimiento, ordenados
    setof(Rendimiento-Jugador,
          (puede_firmar(Equipo, Jugador),
           rendimiento(Jugador, Rendimiento)),
          ListaOrdenada),
    % Invertimos para orden descendente (mayor rendimiento primero)
    reverse(ListaOrdenada, ListaDesc),
    % Hacemos backtracking sobre la lista ordenada
    member(_-Jugador, ListaDesc).

% ----------------------------------------------------------------------------
% PREDICADO: mejor_fichaje/2
% ----------------------------------------------------------------------------
% Encuentra el mejor fichaje posible para un equipo:
% - El jugador con mayor rendimiento que puede ser firmado

mejor_fichaje(Equipo, Jugador) :-
    puede_firmar(Equipo, Jugador),
    rendimiento(Jugador, Rendimiento),
    % Verificamos que no haya otro jugador con mejor rendimiento
    \+ (puede_firmar(Equipo, OtroJugador),
        rendimiento(OtroJugador, OtroRendimiento),
        OtroRendimiento > Rendimiento).

% ----------------------------------------------------------------------------
% PREDICADOS PARA MANEJO DE LISTAS DE JUGADORES
% ----------------------------------------------------------------------------

% Cuenta cuántos extranjeros hay en una lista de jugadores para un equipo
contar_extranjeros([], _, 0).
contar_extranjeros([Jugador|Resto], Equipo, Total) :-
    contar_extranjeros(Resto, Equipo, Subtotal),
    (es_extranjero(Jugador, Equipo) -> Total is Subtotal + 1; Total = Subtotal).

% Verifica si una lista de jugadores respeta el cupo de extranjeros
respeta_cupo_extranjeros(ListaJugadores, Equipo) :-
    contar_extranjeros(ListaJugadores, Equipo, CantidadExtranjeros),
    cupo_extranjeros_equipo(Equipo, CupoMaximo),
    CantidadExtranjeros =< CupoMaximo.

% Calcula el costo total de una lista de jugadores
costo_total([], 0).
costo_total([Jugador|Resto], CostoTotal) :-
    precio_jugador(Jugador, Precio),
    costo_total(Resto, CostoSubtotal),
    CostoTotal is Precio + CostoSubtotal.

% Verifica si una lista de jugadores cabe en el presupuesto
cabe_en_presupuesto(ListaJugadores, Equipo) :-
    costo_total(ListaJugadores, CostoTotal),
    presupuesto_equipo(Equipo, Presupuesto),
    CostoTotal =< Presupuesto.

% Verifica si todos los jugadores de una lista pueden ser firmados
todos_pueden_firmar([], _).
todos_pueden_firmar([Jugador|Resto], Equipo) :-
    puede_firmar(Equipo, Jugador),
    todos_pueden_firmar(Resto, Equipo).

% ----------------------------------------------------------------------------
% PREDICADO: combinacion_valida/2
% ----------------------------------------------------------------------------
% Verifica si una combinación de jugadores es válida para un equipo:
% - Todos pueden ser firmados
% - Respetan el presupuesto
% - Respetan el cupo de extranjeros

combinacion_valida(ListaJugadores, Equipo) :-
    todos_pueden_firmar(ListaJugadores, Equipo),
    cabe_en_presupuesto(ListaJugadores, Equipo),
    respeta_cupo_extranjeros(ListaJugadores, Equipo).

% ----------------------------------------------------------------------------
% PREDICADO: combinacion_optima/2
% ----------------------------------------------------------------------------
% Genera combinaciones óptimas de fichajes para un equipo.
% Una combinación es óptima si:
% - Es válida (presupuesto, cupos, restricciones)
% - Maximiza el rendimiento total del equipo
% 
% Usa backtracking para encontrar todas las combinaciones posibles
% y selecciona las que tienen mayor rendimiento total.

combinacion_optima(Equipo, ListaJugadores) :-
    !,
    combinacion_optima_filtrada_rapida(Equipo, [], 12, 4, ListaJugadores).

% Predicado auxiliar: genera subconjuntos de una lista
subconjunto([], []).
subconjunto([X|Xs], [X|Ys]) :- subconjunto(Xs, Ys).
subconjunto(Xs, [_|Ys]) :- subconjunto(Xs, Ys).

% Calcula el rendimiento total de una lista de jugadores
rendimiento_total([], 0).
rendimiento_total([Jugador|Resto], RendimientoTotal) :-
    rendimiento(Jugador, Rendimiento),
    rendimiento_total(Resto, RendimientoSubtotal),
    RendimientoTotal is Rendimiento + RendimientoSubtotal.

% ----------------------------------------------------------------------------
% PREDICADOS ADICIONALES: CONSULTAS ÚTILES
% ----------------------------------------------------------------------------

% Lista todos los jugadores disponibles para un equipo
jugadores_disponibles(Equipo, ListaJugadores) :-
    findall(Jugador, puede_firmar(Equipo, Jugador), ListaJugadores).

% Lista jugadores por posición para un equipo
jugadores_por_posicion(Equipo, Posicion, ListaJugadores) :-
    findall(Jugador, 
            (puede_firmar(Equipo, Jugador),
             posicion_jugador(Jugador, Posicion)), 
            ListaJugadores).

% Encuentra el jugador más caro que un equipo puede comprar
jugador_mas_caro(Equipo, Jugador) :-
    puede_firmar(Equipo, Jugador),
    precio_jugador(Jugador, Precio),
    \+ (puede_firmar(Equipo, OtroJugador),
        precio_jugador(OtroJugador, OtroPrecio),
        OtroPrecio > Precio).

% Encuentra el jugador más barato que un equipo puede comprar
jugador_mas_barato(Equipo, Jugador) :-
    puede_firmar(Equipo, Jugador),
    precio_jugador(Jugador, Precio),
    \+ (puede_firmar(Equipo, OtroJugador),
        precio_jugador(OtroJugador, OtroPrecio),
        OtroPrecio < Precio).

% Filtra jugadores por rango de edad
jugadores_por_edad(Equipo, EdadMin, EdadMax, ListaJugadores) :-
    findall(Jugador,
            (puede_firmar(Equipo, Jugador),
             edad_jugador(Jugador, Edad),
             Edad >= EdadMin,
             Edad =< EdadMax),
            ListaJugadores).

% Calcula cuánto presupuesto le queda a un equipo después de comprar jugadores
presupuesto_restante(Equipo, ListaJugadores, Restante) :-
    presupuesto_equipo(Equipo, Presupuesto),
    costo_total(ListaJugadores, Costo),
    Restante is Presupuesto - Costo.

% ----------------------------------------------------------------------------
% PREDICADOS: RESTRICCIONES DE LIGA Y COMPETICIÓN
% ----------------------------------------------------------------------------

% Cuenta cuántos jugadores de una nacionalidad específica hay en una lista
contar_por_nacionalidad([], _, 0).
contar_por_nacionalidad([Jugador|Resto], Nacionalidad, Total) :-
    contar_por_nacionalidad(Resto, Nacionalidad, Subtotal),
    (jugador(Jugador, _, _, _, Nacionalidad, _, _) -> 
        Total is Subtotal + 1 
    ; 
        Total = Subtotal
    ).

% Verifica si una lista respeta el límite de jugadores de la misma nacionalidad
respeta_limite_nacionalidad(ListaJugadores, Equipo) :-
    (limite_misma_nacionalidad(Equipo, Limite) ->
        % Para cada nacionalidad, verificar que no exceda el límite
        findall(Nacionalidad, 
                (member(Jugador, ListaJugadores),
                 jugador(Jugador, _, _, _, Nacionalidad, _, _)),
                Nacionalidades),
        list_to_set(Nacionalidades, NacionalidadesUnicas),
        forall(member(Nacionalidad, NacionalidadesUnicas),
               (contar_por_nacionalidad(ListaJugadores, Nacionalidad, Cantidad),
                Cantidad =< Limite))
    ;
        true  % Si no hay límite definido, se permite
    ).

% Cuenta cuántos jugadores formados en cantera hay (nacionales del país del equipo)
contar_cantera([], _, 0).
contar_cantera([Jugador|Resto], Equipo, Total) :-
    contar_cantera(Resto, Equipo, Subtotal),
    (es_nacional(Jugador, Equipo) -> 
        Total is Subtotal + 1 
    ; 
        Total = Subtotal
    ).

% Verifica si una lista cumple con el cupo mínimo de cantera
cumple_cupo_cantera(ListaJugadores, Equipo) :-
    (cupo_minimo_cantera(Equipo, Minimo) ->
        contar_cantera(ListaJugadores, Equipo, Cantidad),
        Cantidad >= Minimo
    ;
        true  % Si no hay requisito, se cumple
    ).

% Cuenta jugadores mayores de cierta edad
contar_mayores_edad([], _, 0).
contar_mayores_edad([Jugador|Resto], EdadLimite, Total) :-
    contar_mayores_edad(Resto, EdadLimite, Subtotal),
    (edad_jugador(Jugador, Edad),
     Edad > EdadLimite -> 
        Total is Subtotal + 1 
    ; 
        Total = Subtotal
    ).

% Verifica si una lista respeta el límite de jugadores mayores
respeta_limite_edad(ListaJugadores, Equipo) :-
    (limite_jugadores_mayores(Equipo, EdadLimite, Maximo) ->
        contar_mayores_edad(ListaJugadores, EdadLimite, Cantidad),
        Cantidad =< Maximo
    ;
        true  % Si no hay límite, se permite
    ).

% Verifica si una combinación cumple todas las restricciones de liga
cumple_reglas_liga(ListaJugadores, Equipo) :-
    respeta_limite_nacionalidad(ListaJugadores, Equipo),
    cumple_cupo_cantera(ListaJugadores, Equipo),
    respeta_limite_edad(ListaJugadores, Equipo).

% ----------------------------------------------------------------------------
% PREDICADOS: QUÍMICA Y COMPATIBILIDAD ENTRE JUGADORES
% ----------------------------------------------------------------------------

% Calcula la química entre dos jugadores
% Primero busca química explícita, luego calcula automática
quimica_entre(Jugador1, Jugador2, Puntuacion) :-
    quimica(Jugador1, Jugador2, Puntuacion), !.
quimica_entre(Jugador1, Jugador2, Puntuacion) :-
    % Química automática por misma nacionalidad
    jugador(Jugador1, _, _, _, Nacionalidad1, _, _),
    jugador(Jugador2, _, _, _, Nacionalidad2, _, _),
    Nacionalidad1 = Nacionalidad2,
    Jugador1 \= Jugador2,
    Puntuacion = 3, !.
quimica_entre(Jugador1, Jugador2, 0).

% Calcula la química total de una lista de jugadores
% Suma la química entre todos los pares
quimica_total([], 0).
quimica_total([_], 0).
quimica_total([Jugador1, Jugador2|Resto], QuimicaTotal) :-
    quimica_entre(Jugador1, Jugador2, QuimicaPar),
    quimica_total([Jugador2|Resto], QuimicaResto),
    % También calcular química del primero con el resto
    quimica_primero_resto(Jugador1, Resto, QuimicaPrimero),
    QuimicaTotal is QuimicaPar + QuimicaResto + QuimicaPrimero.

% Calcula química de un jugador con el resto de la lista
quimica_primero_resto(_, [], 0).
quimica_primero_resto(Jugador1, [Jugador2|Resto], Total) :-
    quimica_entre(Jugador1, Jugador2, Quimica),
    quimica_primero_resto(Jugador1, Resto, Subtotal),
    Total is Quimica + Subtotal.

% Calcula el rendimiento mejorado considerando química
% La química añade un bonus al rendimiento total
rendimiento_con_quimica(ListaJugadores, RendimientoMejorado) :-
    rendimiento_total(ListaJugadores, RendimientoBase),
    quimica_total(ListaJugadores, QuimicaTotal),
    % La química añade un 10% del valor de química al rendimiento
    Bonus is QuimicaTotal * 0.1,
    RendimientoMejorado is RendimientoBase + Bonus.

% Encuentra combinaciones con buena química (química total > umbral)
buena_quimica(ListaJugadores, Umbral) :-
    quimica_total(ListaJugadores, QuimicaTotal),
    QuimicaTotal >= Umbral.

% ----------------------------------------------------------------------------
% PREDICADO ACTUALIZADO: combinacion_valida/2
% ----------------------------------------------------------------------------
% Ahora incluye verificación de reglas de liga

combinacion_valida(ListaJugadores, Equipo) :-
    todos_pueden_firmar(ListaJugadores, Equipo),
    cabe_en_presupuesto(ListaJugadores, Equipo),
    respeta_cupo_extranjeros(ListaJugadores, Equipo),
    cumple_reglas_liga(ListaJugadores, Equipo).

% ----------------------------------------------------------------------------
% PREDICADO ACTUALIZADO: combinacion_optima/2
% ----------------------------------------------------------------------------
% Ahora considera rendimiento con química

combinacion_optima(Equipo, ListaJugadores) :-
    combinacion_optima_filtrada_rapida(Equipo, [], 12, 4, ListaJugadores).

% ----------------------------------------------------------------------------
% PREDICADOS ADICIONALES: CONSULTAS CON QUÍMICA Y RESTRICCIONES
% ----------------------------------------------------------------------------

% Encuentra combinaciones con excelente química
combinacion_con_quimica(Equipo, ListaJugadores, Umbral) :-
    findall(Jugador, puede_firmar(Equipo, Jugador), JugadoresDisponibles),
    subconjunto(ListaJugadores, JugadoresDisponibles),
    ListaJugadores \= [],
    combinacion_valida(ListaJugadores, Equipo),
    buena_quimica(ListaJugadores, Umbral).

% Analiza una combinación mostrando química y restricciones
analizar_combinacion(ListaJugadores, Equipo, Analisis) :-
    costo_total(ListaJugadores, Costo),
    rendimiento_total(ListaJugadores, RendimientoBase),
    rendimiento_con_quimica(ListaJugadores, RendimientoMejorado),
    quimica_total(ListaJugadores, QuimicaTotal),
    contar_extranjeros(ListaJugadores, Equipo, Extranjeros),
    contar_cantera(ListaJugadores, Equipo, Cantera),
    combinacion_valida(ListaJugadores, Equipo),
    Analisis = [
        costo = Costo,
        rendimiento_base = RendimientoBase,
        rendimiento_mejorado = RendimientoMejorado,
        quimica_total = QuimicaTotal,
        extranjeros = Extranjeros,
        cantera = Cantera,
        valida = true
    ].

% ----------------------------------------------------------------------------
% PREDICADOS FILTRADOS: SOPORTE PARA FRONTEND VISUAL
% ----------------------------------------------------------------------------
% Permiten excluir una lista de jugadores (por ejemplo, de clubes rivales)
% al calcular mejor fichaje y combinacion optima.

disponible_filtrado(Equipo, Excluidos, Jugador) :-
    puede_firmar(Equipo, Jugador),
    \+ member(Jugador, Excluidos).

mejor_fichaje_filtrado(Equipo, Excluidos, Jugador) :-
    disponible_filtrado(Equipo, Excluidos, Jugador),
    rendimiento(Jugador, Rendimiento),
    \+ (disponible_filtrado(Equipo, Excluidos, OtroJugador),
        rendimiento(OtroJugador, OtroRendimiento),
        OtroRendimiento > Rendimiento).

combinacion_optima_filtrada(Equipo, Excluidos, ListaJugadores) :-
    combinacion_optima_filtrada_rapida(Equipo, Excluidos, 12, 4, ListaJugadores).

extraer_jugadores([], []).
extraer_jugadores([_-Jugador|Resto], [Jugador|RestoJugadores]) :-
    extraer_jugadores(Resto, RestoJugadores).

tomar_n(_, 0, []) :- !.
tomar_n([], _, []) :- !.
tomar_n([X|Xs], N, [X|Ys]) :-
    N1 is N - 1,
    tomar_n(Xs, N1, Ys).

subconjunto_acotado(Lista, Universo, MaxTam) :-
    subconjunto(Lista, Universo),
    Lista \= [],
    length(Lista, Tam),
    Tam =< MaxTam.

% Version optimizada para frontend:
% 1) toma solo los mejores candidatos por rendimiento
% 2) limita tamano de combinacion
% Esto evita explosiones combinatorias con bases de conocimiento grandes.
combinacion_optima_filtrada_rapida(Equipo, Excluidos, MaxCandidatos, MaxTam, ListaJugadores) :-
    setof(Rendimiento-Jugador,
          (disponible_filtrado(Equipo, Excluidos, Jugador),
           rendimiento(Jugador, Rendimiento)),
          ParesAsc),
    reverse(ParesAsc, ParesDesc),
    extraer_jugadores(ParesDesc, CandidatosOrdenados),
    tomar_n(CandidatosOrdenados, MaxCandidatos, CandidatosTop),
    subconjunto_acotado(ListaJugadores, CandidatosTop, MaxTam),
    combinacion_valida(ListaJugadores, Equipo),
    rendimiento_con_quimica(ListaJugadores, RendimientoTotal),
    \+ (subconjunto_acotado(OtraLista, CandidatosTop, MaxTam),
        combinacion_valida(OtraLista, Equipo),
        rendimiento_con_quimica(OtraLista, OtroRendimiento),
        OtroRendimiento > RendimientoTotal).

