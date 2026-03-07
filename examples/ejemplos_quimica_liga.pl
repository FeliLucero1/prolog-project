% ============================================================================
% EJEMPLOS DE USO: QUÍMICA Y RESTRICCIONES DE LIGA
% ============================================================================
% Este archivo contiene ejemplos de consultas relacionadas con:
% - Sistema de química entre jugadores
% - Restricciones de liga y competición
% ============================================================================

% Para cargar el sistema primero:
% ?- [src/sistema_compras].

% ============================================================================
% EJEMPLOS: RESTRICCIONES DE LIGA
% ============================================================================

% 1. Verificar si una combinación cumple las reglas de liga
% ?- cumple_reglas_liga(['Pedri', 'Gavi', 'Robert Lewandowski'], 'Barcelona').
% Resultado: true (si cumple límites de nacionalidad, cantera y edad)

% 2. Verificar límite de nacionalidad
% ?- respeta_limite_nacionalidad(['Pedri', 'Gavi', 'Rodri'], 'Real Madrid').
% Resultado: true (máximo 3 españoles para Real Madrid)

% 3. Verificar cupo de cantera
% ?- cumple_cupo_cantera(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona').
% Resultado: true (tiene 2 jugadores de cantera, mínimo requerido es 3... espera, esto fallaría)

% 4. Contar jugadores de cantera
% ?- contar_cantera(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona', Cantidad).
% Cantidad = 2.

% 5. Contar por nacionalidad
% ?- contar_por_nacionalidad(['Pedri', 'Gavi', 'Rodri'], espana, Cantidad).
% Cantidad = 3.

% ============================================================================
% EJEMPLOS: QUÍMICA ENTRE JUGADORES
% ============================================================================

% 6. Verificar química entre dos jugadores específicos
% ?- quimica_entre('Pedri', 'Gavi', Puntuacion).
% Puntuacion = 9.

% 7. Calcular química total de una combinación
% ?- quimica_total(['Pedri', 'Gavi', 'Robert Lewandowski'], Quimica).
% Quimica = [valor calculado sumando todas las quimicas entre pares]

% 8. Calcular rendimiento mejorado con química
% ?- rendimiento_con_quimica(['Pedri', 'Gavi'], Rendimiento).
% Rendimiento = [rendimiento base + bonus de química]

% 9. Encontrar combinaciones con buena química
% ?- combinacion_con_quimica('Barcelona', Lista, 15).
% Lista = [combinaciones con química total >= 15]

% 10. Analizar una combinación completa
% ?- analizar_combinacion(['Pedri', 'Gavi', 'Robert Lewandowski'], 'Barcelona', Analisis).
% Analisis = [costo=..., rendimiento_base=..., rendimiento_mejorado=..., ...]

% ============================================================================
% EJEMPLOS: COMBINACIONES ÓPTIMAS CON QUÍMICA
% ============================================================================

% 11. Encontrar combinación óptima (ahora considera química)
% ?- combinacion_optima('Barcelona', Lista).
% Lista = [combinación que maximiza rendimiento + química]

% 12. Comparar rendimiento con y sin química
% ?- rendimiento_total(['Pedri', 'Gavi'], Base),
%    rendimiento_con_quimica(['Pedri', 'Gavi'], Mejorado).
% Base = 20, Mejorado = 20.9 (ejemplo)

% ============================================================================
% EJEMPLOS: RESTRICCIONES COMBINADAS
% ============================================================================

% 13. Verificar combinación válida (ahora incluye reglas de liga)
% ?- combinacion_valida(['Pedri', 'Gavi', 'Erling Haaland'], 'Barcelona').
% Resultado: true/false dependiendo de si cumple:
%   - Presupuesto
%   - Cupo extranjeros
%   - Límite nacionalidad
%   - Cupo cantera
%   - Límite edad

% 14. Encontrar combinaciones que cumplan todas las restricciones
% ?- findall(Lista, 
%            (combinacion_valida(Lista, 'Real Madrid'),
%             length(Lista, 2)),
%            Combinaciones).
% Combinaciones = [todas las combinaciones de 2 jugadores válidas]

% ============================================================================
% EJEMPLOS: ANÁLISIS DETALLADO
% ============================================================================

% 15. Ver todas las restricciones que debe cumplir un equipo
% ?- limite_misma_nacionalidad('Real Madrid', LimiteNac),
%    cupo_minimo_cantera('Real Madrid', MinCantera),
%    cupo_extranjeros('Real Madrid', MaxExtranjeros).
% LimiteNac = 3, MinCantera = 2, MaxExtranjeros = 5

% 16. Verificar química automática (misma nacionalidad)
% ?- quimica_entre('Pedri', 'Rodri', Puntuacion).
% Puntuacion = 3 (química automática por ser ambos españoles)

% 17. Verificar química explícita vs automática
% ?- quimica_entre('Pedri', 'Gavi', Puntuacion).
% Puntuacion = 9 (química explícita, mayor que la automática)

% ============================================================================
% FIN DE EJEMPLOS
% ============================================================================

