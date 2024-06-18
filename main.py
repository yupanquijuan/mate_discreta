import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class AplicacionGrafos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Unión de Destinos con Dijkstra")
        
        self.frame_entrada = ttk.Frame(self.ventana, padding="10")
        self.frame_entrada.pack()

        self.label_nodos = ttk.Label(self.frame_entrada, text="Nodos (lugares):")
        self.label_nodos.grid(row=0, column=0, sticky=tk.W)

        self.entry_nodos = ttk.Entry(self.frame_entrada, width=30)
        self.entry_nodos.grid(row=0, column=1)

        self.label_aristas = ttk.Label(self.frame_entrada, text="Aristas (conexiones y distancia):")
        self.label_aristas.grid(row=1, column=0, sticky=tk.W)

        self.entry_aristas = ttk.Entry(self.frame_entrada, width=30)
        self.entry_aristas.grid(row=1, column=1)

        self.label_origen = ttk.Label(self.frame_entrada, text="Origen:")
        self.label_origen.grid(row=2, column=0, sticky=tk.W)

        self.entry_origen = ttk.Entry(self.frame_entrada, width=20)
        self.entry_origen.grid(row=2, column=1)

        self.label_destino = ttk.Label(self.frame_entrada, text="Destino:")
        self.label_destino.grid(row=3, column=0, sticky=tk.W)

        self.entry_destino = ttk.Entry(self.frame_entrada, width=20)
        self.entry_destino.grid(row=3, column=1)

        self.boton_calcular = ttk.Button(self.frame_entrada, text="Calcular Ruta", command=self.calcular_y_mostrar_ruta)
        self.boton_calcular.grid(row=4, columnspan=2, pady=10)

        self.frame_resultados = ttk.Frame(self.ventana, padding="10")
        self.frame_resultados.pack()

        self.label_resultado = ttk.Label(self.frame_resultados, text="")
        self.label_resultado.pack()

        self.figura_grafo = None  # Variable para guardar la figura del grafo

    def calcular_y_mostrar_ruta(self):
        grafo = Grafo()  # Crear instancia de la clase Grafo

        nodos = self.entry_nodos.get().split(',')
        for nodo in nodos:
            grafo.agregar_nodo(nodo.strip())

        aristas = self.entry_aristas.get().split(';')
        for arista in aristas:
            datos_arista = arista.split(',')
            if len(datos_arista) < 3:
                continue  # Ignorar aristas mal formadas
            desde = datos_arista[0].strip()
            hacia = datos_arista[1].strip()
            peso_distancia = float(datos_arista[2].strip())

            grafo.agregar_arista(desde, hacia, peso_distancia)

        origen = self.entry_origen.get().strip()
        destino = self.entry_destino.get().strip()

        if origen not in grafo.nodos or destino not in grafo.nodos:
            messagebox.showerror("Error", "Origen o destino no válido.")
            return

        distancias, ruta_previa = grafo.dijkstra(origen)
        ruta_corta = grafo.reconstruir_ruta(origen, destino, ruta_previa)

        self.label_resultado.config(text=f"Ruta más corta de {origen} a {destino} por distancia: {ruta_corta}")

        # Mostrar el grafo
        self.mostrar_grafo()

    def mostrar_grafo(self):
        G = nx.DiGraph()

        # Agregar nodos
        nodos = self.entry_nodos.get().split(',')
        for nodo in nodos:
            G.add_node(nodo.strip())

        # Agregar aristas con etiquetas de distancia
        aristas = self.entry_aristas.get().split(';')
        for arista in aristas:
            datos_arista = arista.split(',')
            if len(datos_arista) < 3:
                continue
            desde = datos_arista[0].strip()
            hacia = datos_arista[1].strip()
            peso_distancia = float(datos_arista[2].strip())

            G.add_edge(desde, hacia, weight=peso_distancia)

        # Dibujar el grafo
        pos = nx.spring_layout(G)
        etiquetas_aristas = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_aristas)

        plt.title("Grafo de Nodos y Aristas")
        plt.axis('off')

        # Mostrar la figura en una ventana nueva
        if self.figura_grafo is None:
            self.figura_grafo = plt.figure()
        else:
            self.figura_grafo.clear()

        plt.gca().invert_yaxis()
        plt.show()

class Grafo:
    def __init__(self):
        self.nodos = set()
        self.aristas = {}
        self.distancias = {}

    def agregar_nodo(self, nodo):
        self.nodos.add(nodo)
        if nodo not in self.aristas:
            self.aristas[nodo] = {}
            self.distancias[nodo] = {}

    def agregar_arista(self, desde, hacia, peso_distancia):
        if desde not in self.nodos or hacia not in self.nodos:
            return  # Ignorar aristas con nodos no existentes
        self.aristas[desde][hacia] = peso_distancia
        self.distancias[desde][hacia] = peso_distancia

    def dijkstra(self, origen):
        distancias = {nodo: float('infinity') for nodo in self.nodos}
        distancias[origen] = 0
        cola = [(0, origen)]
        ruta_previa = {}

        while cola:
            (distancia_actual, nodo_actual) = heapq.heappop(cola)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.aristas[nodo_actual].items():
                distancia = distancia_actual + peso
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    heapq.heappush(cola, (distancia, vecino))
                    ruta_previa[vecino] = nodo_actual

        return distancias, ruta_previa

    def reconstruir_ruta(self, origen, destino, ruta_previa):
        ruta = []
        nodo_actual = destino
        while nodo_actual != origen:
            ruta.insert(0, nodo_actual)
            nodo_actual = ruta_previa[nodo_actual]
        ruta.insert(0, origen)
        return ruta

if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = AplicacionGrafos(ventana)
    ventana.mainloop()
