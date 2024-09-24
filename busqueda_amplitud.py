from collections import deque

def amplitud(grafo, inicio, objetivo):
    visitados = set()
    cola = deque([[inicio]])

    if inicio == objetivo:
        return [inicio]

    while cola:
        camino = cola.popleft()
        nodo = camino[-1]

        if nodo not in visitados:
            vecinos = list(grafo[nodo])

            for vecino in vecinos:
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)

                if vecino == objetivo:
                    return nuevo_camino

            visitados.add(nodo)

    return None
