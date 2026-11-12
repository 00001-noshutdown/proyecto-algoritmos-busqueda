from mapa import reconstruir, ejecutar, mostrar


def busqueda_bfs(inicio, meta):
    """Búsqueda en anchura: explora por niveles con una cola (FIFO)."""
    cola = [inicio]
    inicio.visitado = True
    orden = []

    while len(cola) > 0:
        actual = cola.pop(0)              # el que lleva más tiempo esperando
        orden.append(actual)

        if actual == meta:
            return reconstruir(actual), actual.costo_acumulado, orden

        for vecino, costo in actual.vecinos:
            if not vecino.visitado:
                vecino.visitado = True
                vecino.anterior = actual
                vecino.costo_acumulado = actual.costo_acumulado + costo
                cola.append(vecino)

    return [], 0, orden


if __name__ == "__main__":
    mostrar("BFS", ejecutar(busqueda_bfs, "A", "K"))
