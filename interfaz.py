import tkinter as tk
from tkinter import ttk, messagebox

from mapa import NODOS, CONEXIONES, POSICIONES, TIPOS_H, ejecutar
from bfs import busqueda_bfs
from dfs import busqueda_dfs
from greedy import busqueda_voraz
from astar import busqueda_a_estrella

ALGORITMOS = {
    "BFS": busqueda_bfs,
    "DFS": busqueda_dfs,
    "Greedy Best-First": busqueda_voraz,
    "A*": busqueda_a_estrella,
}

EXPLICACIONES = {
    "BFS": "Explora por niveles (cola FIFO). Garantiza el menor número de "
           "conexiones, pero ignora los costos, por eso puede no ser la ruta más barata.",
    "DFS": "Se mete lo más profundo posible por un camino y retrocede si llega a "
           "un callejón sin salida. Encuentra una ruta, pero normalmente larga y cara.",
    "Greedy Best-First": "Siempre expande el nodo con menor h (más cerca de la meta "
                         "en línea recta). Es rápido, pero ignora el costo acumulado.",
    "A*": "Expande el nodo con menor f = g + h (costo recorrido + estimación). Con una "
          "heurística admisible garantiza la ruta de menor costo.",
}

COLOR_RUTA, COLOR_EXPLORADO = "#7bd88f", "#ffd699"


def px(nombre):
    x, y = POSICIONES[nombre]
    return 60 + x * 60, 470 - y * 43


class App:
    def __init__(self, root):
        root.title("Búsqueda de rutas - Logística")
        panel = ttk.Frame(root, padding=8)
        panel.grid(row=0, column=0, sticky="n")

        nombres = sorted(NODOS)
        self.alg = tk.StringVar(value="A*")
        self.ini = tk.StringVar(value="A")
        self.fin = tk.StringVar(value="K")
        self.heu = tk.StringVar(value="Euclidiana")

        for i, (txt, var, vals) in enumerate([
                ("Algoritmo", self.alg, list(ALGORITMOS)),
                ("Nodo inicial", self.ini, nombres),
                ("Nodo destino", self.fin, nombres),
                ("Heurística", self.heu, list(TIPOS_H))]):
            ttk.Label(panel, text=txt).grid(row=2 * i, column=0, sticky="w")
            ttk.Combobox(panel, textvariable=var, values=vals, state="readonly",
                         width=22).grid(row=2 * i + 1, column=0, pady=(0, 6))

        ttk.Button(panel, text="Ejecutar búsqueda", command=self.buscar).grid(row=8, column=0, pady=4)
        ttk.Button(panel, text="Comparar los 4 algoritmos", command=self.comparar).grid(row=9, column=0)

        self.salida = tk.Text(panel, width=38, height=18, wrap="word")
        self.salida.grid(row=10, column=0, pady=8)

        self.canvas = tk.Canvas(root, width=720, height=510, bg="white")
        self.canvas.grid(row=0, column=1, padx=8, pady=8)
        self.dibujar()

    def dibujar(self, ruta=(), explorados=()):
        c = self.canvas
        c.delete("all")
        pares_ruta = {frozenset(p) for p in zip(ruta, ruta[1:])}
        for a, b, costo, bloqueada in CONEXIONES:
            (x1, y1), (x2, y2) = px(a), px(b)
            if bloqueada:
                c.create_line(x1, y1, x2, y2, fill="red", dash=(6, 4), width=2)
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="X", fill="red", font=("Arial", 14, "bold"))
            elif frozenset((a, b)) in pares_ruta:
                c.create_line(x1, y1, x2, y2, fill="#1a9c3a", width=6)
            else:
                c.create_line(x1, y1, x2, y2, fill="#999", width=2)
            if not bloqueada:
                c.create_text((x1 + x2) / 2 + 8, (y1 + y2) / 2 - 8, text=str(costo),
                              fill="#333", font=("Arial", 9))
        for n in NODOS:
            x, y = px(n)
            relleno = COLOR_RUTA if n in ruta else COLOR_EXPLORADO if n in explorados else "white"
            borde, grosor = "black", 2
            if n == self.ini.get():
                borde, grosor = "blue", 4
            if n == self.fin.get():
                borde, grosor = "red", 4
            c.create_oval(x - 19, y - 19, x + 19, y + 19, fill=relleno, outline=borde, width=grosor)
            c.create_text(x, y, text=n, font=("Arial", 12, "bold"))
        c.create_text(10, 495, anchor="w", font=("Arial", 9),
                      text="Borde azul: inicio | borde rojo: destino | verde: ruta | naranja: explorado | rojo punteado: bloqueada")

    def buscar(self):
        if self.ini.get() == self.fin.get():
            messagebox.showwarning("Aviso", "El inicio y el destino deben ser distintos.")
            return
        nombre = self.alg.get()
        r = ejecutar(ALGORITMOS[nombre], self.ini.get(), self.fin.get(), self.heu.get())
        self.dibujar(r["camino"], r["orden"])
        t = self.salida
        t.delete("1.0", "end")
        t.insert("end", "Algoritmo: %s\n" % nombre)
        if r["camino"]:
            t.insert("end", "Ruta: %s\n" % " -> ".join(r["camino"]))
            t.insert("end", "Costo total: %s\n" % r["costo"])
        else:
            t.insert("end", "No existe ruta entre esos nodos.\n")
        t.insert("end", "Nodos explorados: %d\n" % r["explorados"])
        t.insert("end", "Orden: %s\n" % " ".join(r["orden"]))
        t.insert("end", "Tiempo: %.4f ms\n\n" % r["tiempo_ms"])
        t.insert("end", EXPLICACIONES[nombre])

    def comparar(self):
        if self.ini.get() == self.fin.get():
            messagebox.showwarning("Aviso", "El inicio y el destino deben ser distintos.")
            return
        t = self.salida
        t.delete("1.0", "end")
        t.insert("end", "%s -> %s (heurística: %s)\n\n" % (self.ini.get(), self.fin.get(), self.heu.get()))
        for nombre, f in ALGORITMOS.items():
            r = ejecutar(f, self.ini.get(), self.fin.get(), self.heu.get())
            t.insert("end", "%s\n  ruta: %s\n  costo: %s | explorados: %d | %.4f ms\n\n" %
                     (nombre, "-".join(r["camino"]) or "sin ruta", r["costo"], r["explorados"], r["tiempo_ms"]))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
