def dfs_limitado(grafo, inicio, objetivo, limite, visitados=None):
    if visitados is None:
        visitados = set()

    visitados.add(inicio)

    if inicio == objetivo:
        return [inicio]

    if limite <= 0:
        return None

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            camino = dfs_limitado(grafo, vecino, objetivo, limite - 1, visitados)
            if camino:
                return [inicio] + camino

    return None

def iterativa(grafo, inicio, objetivo, max_depth):
    for profundidad in range(max_depth + 1):
        visitados = set()
        resultado = dfs_limitado(grafo, inicio, objetivo, profundidad, visitados)
        if resultado:
            return resultado
    return None
