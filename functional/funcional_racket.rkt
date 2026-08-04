#lang racket

;; Material complementario del proyecto para evidenciar contenidos
;; del paradigma funcional (Unidad IV y V del programa).
;;
;; Ejecutar:
;;   racket functional/funcional_racket.rkt

(struct jugador (nombre posicion edad precio nacionalidad goles asistencias) #:transparent)

(define jugadores-demo
  (list
   (jugador "Kylian Mbappe" 'delantero 25 180 'francia 35 10)
   (jugador "Rodri" 'mediocampista 28 85 'espana 4 6)
   (jugador "Pedri" 'mediocampista 21 100 'espana 8 12)
   (jugador "Bukayo Saka" 'delantero 22 120 'inglaterra 18 15)
   (jugador "Robert Lewandowski" 'delantero 35 25 'polonia 30 6)))

(define (rendimiento j)
  (+ (jugador-goles j) (jugador-asistencias j)))

(define (puede-pagar? presupuesto j)
  (<= (jugador-precio j) presupuesto))

(define (por-posicion pos jugadores)
  (filter (lambda (j) (eq? (jugador-posicion j) pos)) jugadores))

(define (recomendar presupuesto posicion jugadores)
  (define candidatos
    (filter (lambda (j)
              (and (puede-pagar? presupuesto j)
                   (eq? (jugador-posicion j) posicion)))
            jugadores))
  (sort candidatos > #:key rendimiento))

(define (costo-total lista)
  (foldl (lambda (j acc) (+ acc (jugador-precio j))) 0 lista))

(define (nombres lista)
  (map jugador-nombre lista))

(define (demo)
  (displayln "== Demo funcional (Racket) ==")
  (define sugeridos (recomendar 130 'delantero jugadores-demo))
  (displayln (format "Sugeridos: ~a" (nombres sugeridos)))
  (displayln (format "Costo total: ~a" (costo-total sugeridos)))
  (displayln (format "Solo mediocampistas: ~a"
                     (nombres (por-posicion 'mediocampista jugadores-demo)))))

(module+ main
  (demo))
