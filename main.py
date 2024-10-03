import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

from grafo import grafo
from _amplitud_search import amplitud
from _profundidad_search import profundida
from _coste_search import coste
from _iterativa_search import iterativa

class GraphTraversalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busqueda en nodos")
        self.root.configure(bg='palegreen')
        self.root.state('zoomed')

        self.graph = self.create_graph()
        self.pos = nx.spring_layout(self.graph, k=1.2)
        self.canvas = None

        # Configuración del estilo para botones y etiquetas (texto en negro y fondo negro)
        style = ttk.Style()
        style.configure("TButton", background='palegreen2', foreground='black', font=('SegoeUI', 12), padding=6)
        style.configure("TLabel", foreground='black', background='limegreen', font=('SegoeUI', 16,))
        style.configure("TFrame", background='palegreen2')  # Fondo del frame en negro
        style.configure("TCombo", font=('SegoeUI', 14))

        self.create_widgets()
        self.draw_graph()

    def create_graph(self):
        g = nx.Graph()
        graph_data = grafo()
        for node, neighbors in graph_data.items():
            for neighbor, weight in neighbors.items():
                g.add_edge(node, neighbor, weight=weight)
        return g

    def create_widgets(self):
        nodos = list(grafo().keys())

        frame = ttk.Frame(self.root, style="TFrame")
        frame.pack(pady=20)

        # Etiquetas y Combobox (fondo del frame es negro)
        ttk.Label(frame, text="Selecciona Punto Inicial:").grid(row=0, column=0, padx=10, pady=10)
        self.start_combobox = ttk.Combobox(frame, values=nodos, state='readonly')
        self.start_combobox.grid(row=1, column=0, padx=10, pady=10)
        self.start_combobox.set('')

        ttk.Label(frame, text="Selecciona Punto Final:").grid(row=0, column=1, padx=10, pady=10)
        self.end_combobox = ttk.Combobox(frame, values=nodos, state='readonly')
        self.end_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.end_combobox.set('')

        # Frame para los botones de limpiar y salir, también en negro
        ttk.Button(frame, text="Restablecer", command=self.clear_entries).grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(frame, text="Salir", command=self.root.quit).grid(row=1, column=3, padx=10, pady=10)

        # Botones con estilo (fondo negro y texto negro)
        ttk.Button(frame, text="BFS (Amplitud)", command=lambda: self.show_result("BFS")).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(frame, text="DFS (Profundidad)", command=lambda: self.show_result("DFS")).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(frame, text="UCS (Coste Uniforme)", command=lambda: self.show_result("UCS")).grid(row=2, column=2, padx=10, pady=10)
        ttk.Button(frame, text="IDDFS (Prof. Iterativa)", command=lambda: self.show_result("IDDFS")).grid(row=2, column=3, padx=10, pady=10)

    def draw_graph(self, path_edges=None, path_nodes=None):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots(figsize=(9, 7))
        nx.draw(self.graph, self.pos, with_labels=True, node_color='#3498db', node_size=800, font_size=9, font_color='black', font_weight='bold', edge_color='#9b59b6', width=2, ax=ax)  # Palabras en negro
        if path_nodes:
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path_nodes, node_color="#e74c3c", node_size=900)

        if path_edges:
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges, width=5, edge_color='#2ecc71')

        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'), font_color='black', ax=ax)  # Color de las etiquetas en negro

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_result(self, search_type):
        start = self.start_combobox.get().strip()
        goal = self.end_combobox.get().strip()

        if search_type == "BFS":
            result = amplitud(self.graph, start, goal)
        elif search_type == "DFS":
            result = profundida(self.graph, start, goal)
        elif search_type == "UCS":
            result = coste(self.graph, start, goal)
        elif search_type == "IDDFS":
            result = iterativa(self.graph, start, goal, max_depth=3)

        if result:
            path_edges = [(result[i], result[i + 1]) for i in range(len(result) - 1)]
            path_nodes = result
            self.draw_graph(path_edges, path_nodes)

            if search_type == "UCS":
                self.show_distance(sum(self.graph[u][v]['weight'] for u, v in path_edges))
        else:
            self.draw_graph()

    def clear_entries(self):
        self.start_combobox.set('')
        self.end_combobox.set('')
        self.draw_graph()

    def show_distance(self, total_weight):
        messagebox.showinfo("Resultado UCS", f"Distancia: {self.start_combobox.get()} - {self.end_combobox.get()}: {total_weight} m")

def main():
    root = tk.Tk()
    app = GraphTraversalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
