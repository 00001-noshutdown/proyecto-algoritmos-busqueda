import sys
from mapa import reconstruir, ejecutar, mostrar

sys.setrecursionlimit(5000)


def busqueda_dfs(inicio, meta):
    """Búsqueda en profundidad con retroceso (recursiva)."""
    orden = []

    def visitar(actual):
        actual.visitado = True
        orden.append(actual)

        if actual == meta:
            return True

        for vecino, costo in actual.vecinos:
            if not vecino.visitado:
                vecino.anterior = actual
                vecino.costo_acumulado = actual.costo_acumulado + costo
                if visitar(vecino):       # baja lo más profundo posible
                    return True
        return False                      # callejón sin salida: RETROCEDE

    if visitar(inicio):
        return reconstruir(meta), meta.costo_acumulado, orden
    return [], 0, orden


if __name__ == "__main__":
    mostrar("DFS", ejecutar(busqueda_dfs, "A", "K"))
