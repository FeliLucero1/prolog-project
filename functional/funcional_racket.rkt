#lang racket

;; Implementación funcional comparativa del sistema de fichajes.
;; Objetivo: resolver el mismo problema central que Prolog,
;; pero con estilo funcional explícito (listas inmutables + HOF + recursión).
;;
;; Ejecutar demo:
;;   racket functional/funcional_racket.rkt
;;
;; Ejecutar tests:
;;   raco test functional/funcional_racket.rkt

(require racket/list
         racket/format
         racket/string
         rackunit)

(struct jugador (nombre posicion edad precio nacionalidad goles asistencias club) #:transparent)
(struct equipo (nombre presupuesto cupo-extranjeros nacionalidad necesidades edad-min edad-max) #:transparent)

(define jugadores
  (list
   (jugador "Kylian Mbappe" 'delantero 25 180 'francia 35 10 "Real Madrid")
   (jugador "Erling Haaland" 'delantero 24 150 'noruega 40 8 "Manchester City")
   (jugador "Robert Lewandowski" 'delantero 35 25 'polonia 30 6 "Barcelona")
   (jugador "Karim Benzema" 'delantero 36 20 'francia 22 9 "Al-Ittihad")
   (jugador "Pedri" 'mediocampista 21 100 'espana 8 12 "Barcelona")
   (jugador "Gavi" 'mediocampista 20 90 'espana 5 7 "Barcelona")
   (jugador "Jude Bellingham" 'mediocampista 21 120 'inglaterra 10 8 "Real Madrid")
   (jugador "Rodri" 'mediocampista 28 85 'espana 4 6 "Manchester City")
   (jugador "Kevin De Bruyne" 'mediocampista 33 80 'belgica 12 20 "Manchester City")
   (jugador "Virgil van Dijk" 'defensa 33 40 'holanda 2 1 "Liverpool")
   (jugador "Ronald Araujo" 'defensa 25 70 'uruguay 1 1 "Barcelona")
   (jugador "Theo Hernandez" 'defensa 26 50 'francia 4 6 "AC Milan")
   (jugador "Alisson" 'portero 32 50 'brasil 0 0 "Liverpool")
   (jugador "Thibaut Courtois" 'portero 32 45 'belgica 0 0 "Real Madrid")
   (jugador "Mike Maignan" 'portero 29 55 'francia 0 0 "AC Milan")))

(define equipos
  (list
   (equipo "Real Madrid" 200 5 'espana '(delantero mediocampista) 20 #f)
   (equipo "Barcelona" 150 4 'espana '(delantero defensa) 18 #f)
   (equipo "Manchester City" 300 6 'inglaterra '(mediocampista defensa) #f #f)
   (equipo "Bayern Munich" 180 4 'alemania '(portero defensa) #f 32)
   (equipo "PSG" 250 7 'francia '(mediocampista defensa) #f #f)
   (equipo "Liverpool" 120 5 'inglaterra '(delantero mediocampista) #f 30)))

;; -------- utilidades puras --------

(define (buscar-equipo nombre)
  (findf (lambda (e) (string-ci=? (equipo-nombre e) nombre)) equipos))

(define (rendimiento j)
  (+ (jugador-goles j) (jugador-asistencias j)))

(define (es-extranjero? eq j)
  (not (eq? (equipo-nacionalidad eq) (jugador-nacionalidad j))))

(define (cumple-edad? eq j)
  (define edad (jugador-edad j))
  (define min-ok (if (equipo-edad-min eq) (>= edad (equipo-edad-min eq)) #t))
  (define max-ok (if (equipo-edad-max eq) (<= edad (equipo-edad-max eq)) #t))
  (and min-ok max-ok))

(define (cubre-necesidad? eq j)
  (member (jugador-posicion j) (equipo-necesidades eq)))

(define (puede-pagar? eq j)
  (<= (jugador-precio j) (equipo-presupuesto eq)))

(define (puede-firmar? eq j)
  (and (puede-pagar? eq j)
       (cubre-necesidad? eq j)
       (cumple-edad? eq j)))

(define (costo-total lista)
  (foldl (lambda (j acc) (+ acc (jugador-precio j))) 0 lista))

(define (contar-extranjeros eq lista)
  (foldl (lambda (j acc) (+ acc (if (es-extranjero? eq j) 1 0))) 0 lista))

(define (cumple-cupo-extranjeros? eq lista)
  (<= (contar-extranjeros eq lista) (equipo-cupo-extranjeros eq)))

(define (comb-valida? eq lista)
  (and (not (empty? lista))
       (andmap (lambda (j) (puede-firmar? eq j)) lista)
       (<= (costo-total lista) (equipo-presupuesto eq))
       (cumple-cupo-extranjeros? eq lista)))

(define (nombres lista)
  (map jugador-nombre lista))

;; -------- combinaciones (recursión explícita) --------

(define (subconjuntos xs)
  (if (empty? xs)
      (list '())
      (let* ([resto (subconjuntos (rest xs))]
             [con-primer (map (lambda (s) (cons (first xs) s)) resto)])
        (append resto con-primer))))

(define (filtrar-tamano-max subconj tam-max)
  (filter (lambda (s) (and (not (empty? s)) (<= (length s) tam-max))) subconj))

;; -------- consultas equivalentes a Prolog --------

(define (recomendaciones equipo-nombre)
  (define eq (buscar-equipo equipo-nombre))
  (if (not eq)
      '()
      (sort (filter (lambda (j) (puede-firmar? eq j)) jugadores)
            >
            #:key rendimiento)))

(define (recomendaciones-por-posicion equipo-nombre pos)
  (filter (lambda (j) (eq? (jugador-posicion j) pos))
          (recomendaciones equipo-nombre)))

(define (mejor-fichaje equipo-nombre)
  (define recs (recomendaciones equipo-nombre))
  (if (empty? recs) #f (first recs)))

(define (recomendaciones-por-autor-club equipo-nombre clubes-vistos)
  (define recs (recomendaciones equipo-nombre))
  (filter (lambda (j) (member (jugador-club j) clubes-vistos)) recs))

(define (mejor-combinacion equipo-nombre [tam-max 3])
  (define eq (buscar-equipo equipo-nombre))
  (if (not eq)
      '()
      (let* ([candidatos (recomendaciones equipo-nombre)]
             [subs (filtrar-tamano-max (subconjuntos candidatos) tam-max)]
             [validas (filter (lambda (s) (comb-valida? eq s)) subs)])
        (if (empty? validas)
            '()
            (argmax (lambda (s) (apply + (map rendimiento s))) validas)))))

;; -------- presentación de resultados --------

(define (mostrar-jugador j)
  (displayln
   (format "~a | ~a | Edad ~a | ~a M€ | Rend ~a"
           (jugador-nombre j)
           (symbol->string (jugador-posicion j))
           (jugador-edad j)
           (jugador-precio j)
           (rendimiento j))))

(define (mostrar-lista titulo lista)
  (displayln (string-append "\n" titulo))
  (if (empty? lista)
      (displayln "  (sin resultados)")
      (for-each (lambda (j) (displayln (string-append "  - " (jugador-nombre j)))) lista)))

(define (demo)
  (displayln "== Demo comparativa funcional (Racket) ==")
  (define equipo-demo "Real Madrid")
  (displayln (format "\nEquipo: ~a" equipo-demo))

  (define recs (recomendaciones equipo-demo))
  (displayln (format "Recomendaciones totales: ~a" (length recs)))
  (for-each mostrar-jugador (take recs (min 5 (length recs))))

  (define mejor (mejor-fichaje equipo-demo))
  (when mejor
    (displayln "\nMejor fichaje funcional:")
    (mostrar-jugador mejor))

  (define combo (mejor-combinacion equipo-demo 3))
  (displayln "\nMejor combinación funcional (tam <= 3):")
  (if (empty? combo)
      (displayln "  (sin combinación válida)")
      (begin
        (displayln (format "  Jugadores: ~a" (string-join (nombres combo) ", ")))
        (displayln (format "  Costo total: ~a M€" (costo-total combo)))
        (displayln
         (format "  Rendimiento total: ~a"
                 (apply + (map rendimiento combo))))))

  (define por-autor (recomendaciones-por-autor-club equipo-demo '("Barcelona" "Manchester City")))
  (mostrar-lista "Recomendadas por clubes ya observados (autor-club):" por-autor))

;; Menú interactivo para defensa (similar a los ejemplos de la cátedra).
(define (menu-loop)
  (displayln "\n=== Menú funcional de recomendaciones ===")
  (displayln "1) Ver recomendaciones por equipo")
  (displayln "2) Ver mejor fichaje")
  (displayln "3) Ver mejor combinación")
  (displayln "4) Ejecutar demo")
  (displayln "0) Salir")
  (display "Opción: ")
  (flush-output)
  (define op (read))
  (define (pedir-linea-etiqueta etiqueta)
    (display etiqueta)
    (flush-output)
    (let loop ()
      (define txt (string-trim (read-line)))
      (if (string=? txt "") (loop) txt)))
  (cond
    [(equal? op 0) (displayln "Fin.")]
    [(equal? op 1)
     (define e (pedir-linea-etiqueta "Equipo: "))
     (define rs (recomendaciones e))
     (displayln (format "Recomendaciones para ~a: ~a" e (length rs)))
     (for-each mostrar-jugador (take rs (min 10 (length rs))))
     (menu-loop)]
    [(equal? op 2)
     (define e (pedir-linea-etiqueta "Equipo: "))
     (define m (mejor-fichaje e))
     (if m (mostrar-jugador m) (displayln "No encontrado."))
     (menu-loop)]
    [(equal? op 3)
     (define e (pedir-linea-etiqueta "Equipo: "))
     (define c (mejor-combinacion e 3))
     (if (empty? c)
         (displayln "Sin combinación válida.")
         (displayln (format "~a" (nombres c))))
     (menu-loop)]
    [(equal? op 4)
     (demo)
     (menu-loop)]
    [else
     (displayln "Opción inválida.")
     (menu-loop)]))

;; -------- tests de consistencia --------

(module+ test
  (check-true (not (empty? (recomendaciones "Real Madrid"))))
  (check-true (jugador? (mejor-fichaje "Barcelona")))
  (check-true (list? (mejor-combinacion "Manchester City" 3)))
  (check-equal? (costo-total '()) 0)
  (let ([eq (buscar-equipo "Liverpool")]
        [j (jugador "Tmp" 'delantero 20 10 'francia 1 1 "X")])
    (check-true (es-extranjero? eq j))))

(module+ main
  (demo))
