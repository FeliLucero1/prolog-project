:- begin_tests(logica_fichajes).

:- consult('src/conocimiento.pl').
:- consult('src/reglas.pl').

test(combinacion_valida_aplica_reglas_liga, [true]) :-
    \+ combinacion_valida(['Kylian Mbappé'], 'Real Madrid').

test(mejor_fichaje_real_madrid_existe, [nondet]) :-
    mejor_fichaje('Real Madrid', _).

test(quimica_explicita, [true(Q =:= 9)]) :-
    quimica_entre('Pedri', 'Gavi', Q).

test(rendimiento_con_quimica_mayor_igual_base, [true(RMejorado >= RBase)]) :-
    RBase is 8 + 12 + 5 + 7,
    once(rendimiento_con_quimica(['Pedri', 'Gavi'], RMejorado)).

:- end_tests(logica_fichajes).
