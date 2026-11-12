from mapa import reconstruir, ejecutar, mostrar


def buscar_menor_f(lista):
    menor = lista[0]
    for nodo in lista:
        if nodo.costo_acumulado + nodo.h < menor.costo_acumulado + menor.h:
            menor = nodo
    return menor


def busqueda_a_estrella(inicio, meta):
    """A*: elige el nodo con menor f = g (costo acumulado) + h (heurística)."""
    pendientes = [inicio]
    orden = []

    while len(pendientes) > 0:
        actual = buscar_menor_f(pendientes)
        pendientes.remove(actual)
        actual.visitado = True
        orden.append(actual)

        if actual == meta:
            return reconstruir(actual), actual.costo_acumulado, orden

        for vecino, costo in actual.vecinos:
            nuevo_costo = actual.costo_acumulado + costo
            # Entra si es nuevo, o si encontramos un camino MÁS BARATO hasta él
            if (vecino not in pendientes and not vecino.visitado) or \
               (vecino.costo_acumulado > nuevo_costo and (vecino in pendientes or vecino.visitado)):
                vecino.anterior = actual
                vecino.costo_acumulado = nuevo_costo
                vecino.visitado = False
                if vecino not in pendientes:
                    pendientes.append(vecino)

    return [], 0, orden


if __name__ == "__main__":
    mostrar("A*", ejecutar(busqueda_a_estrella, "A", "K"))
