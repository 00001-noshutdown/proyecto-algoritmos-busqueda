"""Mapa (grafo) de la empresa de logística y utilidades comunes."""
import math
import time


class Nodo:
    def __init__(self, nombre, x, y):
        self.nombre = nombre
        self.x = x                  # posición (solo para la heurística y la interfaz)
        self.y = y
        self.h = 0                  # heurística: distancia estimada a la meta
        self.visitado = False
        self.anterior = None
        self.costo_acumulado = 0
        self.vecinos = []           # lista de (nodo, costo)

    def agrega_vecino(self, nodo, costo):
        self.vecinos.append((nodo, costo))

    def reiniciar(self):
        self.visitado = False
        self.anterior = None
        self.costo_acumulado = 0


# ---------------------------------------------------------------- MAPA
# Posiciones (x, y) de cada ubicación
POSICIONES = {
    "A": (0, 4), "B": (2, 7), "C": (2, 4), "D": (2, 1),
    "E": (5, 8), "F": (5, 5), "G": (5, 2), "H": (8, 7),
    "I": (8, 4), "J": (8, 1), "K": (10, 5), "L": (10, 2),
}

# (origen, destino, costo, bloqueada). Todas las vías son de doble sentido.
CONEXIONES = [
    ("A", "B", 4.0, False), ("A", "C", 2.5, False), ("A", "D", 5.0, False),
    ("B", "C", 3.5, False), ("B", "E", 3.5, False), ("C", "D", 3.0, False),
    ("C", "F", 4.0, False), ("D", "G", 3.5, False), ("E", "F", 3.0, False),
    ("E", "H", 6.0, False), ("F", "G", 3.5, False),
    ("F", "H", 8.0, False),   # carretera muy congestionada (costo alto)
    ("F", "I", 3.5, True),    # BLOQUEADA: no se puede usar
    ("G", "I", 6.0, False), ("G", "J", 3.5, False), ("H", "I", 3.5, False),
    ("H", "K", 5.0, False), ("I", "K", 2.5, False), ("I", "J", 4.0, False),
    ("I", "L", 3.0, False), ("J", "L", 2.5, False), ("K", "L", 3.5, False),
    ("J", "K", 5.0, False),
]

NODOS = {n: Nodo(n, x, y) for n, (x, y) in POSICIONES.items()}
for a, b, costo, bloqueada in CONEXIONES:
    if not bloqueada:           # una conexión bloqueada no se agrega al grafo
        NODOS[a].agrega_vecino(NODOS[b], costo)
        NODOS[b].agrega_vecino(NODOS[a], costo)

# ---------------------------------------------------------- HEURÍSTICAS
# Distancia en línea recta multiplicada por un factor
TIPOS_H = {
    "Euclidiana": 1.0,
    "Sobreestimada (x3)": 3.0,
    "Cero (sin heurística)": 0.0,
}


def calcular_heuristicas(meta, tipo="Euclidiana"):
    factor = TIPOS_H[tipo]
    for n in NODOS.values():
        n.h = round(factor * math.hypot(n.x - meta.x, n.y - meta.y), 2)


# ------------------------------------------------------------ UTILIDADES
def reiniciar_nodos():
    for n in NODOS.values():
        n.reiniciar()


def reconstruir(meta):
    camino = []
    nodo = meta
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = nodo.anterior
    return camino


def ejecutar(algoritmo, inicio, meta, tipo_h="Euclidiana", repeticiones=200):
    """Corre el algoritmo y devuelve un diccionario con los resultados.
    El tiempo es el promedio de varias repeticiones (una sola corrida es
    demasiado rápida para medirse con precisión)."""
    calcular_heuristicas(NODOS[meta], tipo_h)
    t0 = time.perf_counter()
    for _ in range(repeticiones):
        reiniciar_nodos()
        camino, costo, orden = algoritmo(NODOS[inicio], NODOS[meta])
    tiempo_ms = (time.perf_counter() - t0) / repeticiones * 1000
    return {
        "camino": [n.nombre for n in camino],
        "costo": round(costo, 2),
        "explorados": len(orden),
        "orden": [n.nombre for n in orden],
        "tiempo_ms": tiempo_ms,
    }


def mostrar(titulo, r):
    print("=== " + titulo + " ===")
    print("Orden de exploración:", " -> ".join(r["orden"]))
    if r["camino"]:
        print("Ruta encontrada:", " -> ".join(r["camino"]))
        print("Costo total:", r["costo"])
    else:
        print("No se encontró ruta")
    print("Nodos explorados:", r["explorados"])
    print("Tiempo de ejecución: %.4f ms" % r["tiempo_ms"])
