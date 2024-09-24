def profundida(grafo, inicio, objetivo, visitados=None):
    if visitados is None:
        visitados = set()

    visitados.add(inicio)

    if inicio == objetivo:
        return [inicio]

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            camino = profundida(grafo, vecino, objetivo, visitados)
            if camino:
                return [inicio] + camino

    return None
