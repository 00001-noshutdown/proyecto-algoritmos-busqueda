from mapa import ejecutar, TIPOS_H
from bfs import busqueda_bfs
from dfs import busqueda_dfs
from greedy import busqueda_voraz
from astar import busqueda_a_estrella

ALGORITMOS = [("BFS", busqueda_bfs), ("DFS", busqueda_dfs),
              ("Greedy", busqueda_voraz), ("A*", busqueda_a_estrella)]

INICIO, META = "A", "K"

print("TABLA COMPARATIVA (inicio %s, destino %s)" % (INICIO, META))
print("%-8s %-28s %-7s %-10s %s" % ("Algoritmo", "Ruta", "Costo", "Explorados", "Tiempo (ms)"))
for nombre, f in ALGORITMOS:
    r = ejecutar(f, INICIO, META)
    print("%-9s %-28s %-7s %-10s %.4f" % (nombre, "-".join(r["camino"]), r["costo"],
                                         r["explorados"], r["tiempo_ms"]))
    print("          orden:", "-".join(r["orden"]))

print("\nEFECTO DE CAMBIAR LA HEURÍSTICA")
for tipo in TIPOS_H:
    for nombre, f in ALGORITMOS[2:]:
        r = ejecutar(f, INICIO, META, tipo)
        print("%-24s %-7s ruta %-26s costo %-5s explorados %s" %
              (tipo, nombre, "-".join(r["camino"]), r["costo"], r["explorados"]))
