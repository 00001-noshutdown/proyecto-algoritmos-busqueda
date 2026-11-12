from mapa import reconstruir, ejecutar, mostrar


def buscar_menor(lista):
    menor = lista[0]
    for nodo in lista:
        if nodo.h < menor.h:
            menor = nodo
    return menor


def busqueda_voraz(inicio, meta):
    """Greedy Best-First: elige siempre el nodo con menor h (ignora el costo)."""
    pendientes = [inicio]
    orden = []

    while len(pendientes) > 0:
        actual = buscar_menor(pendientes)
        pendientes.remove(actual)
        actual.visitado = True
        orden.append(actual)

        if actual == meta:
            return reconstruir(actual), actual.costo_acumulado, orden

        for vecino, costo in actual.vecinos:
            if vecino.visitado == False and vecino not in pendientes:
                vecino.anterior = actual
                vecino.costo_acumulado = actual.costo_acumulado + costo
                pendientes.append(vecino)

    return [], 0, orden


if __name__ == "__main__":
    mostrar("GREEDY", ejecutar(busqueda_voraz, "A", "K"))
