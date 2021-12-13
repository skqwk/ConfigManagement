addedNodes = set()

sorted = []

def topSort(graph):
    
    # Пока не все вершины рассмотрены
    while (len(sorted) != len(graph)):
        for node in graph:
            # Если данная вершина еще не рассматривалась
            if node not in addedNodes:
                # Помечаем ее
                addedNodes.add(node)
                # Рекурсивно проверяем детей данной вершины
                checkChildren(graph[node], node, graph)
    return sorted

def checkChildren(tree, head, graph):
    addedNodes.add(head)
    if head in sorted:
        return
    # Рекурсивно вызываем у детей 
    for node in tree:
        try:
            checkChildren(graph[node], node, graph)
        except:
            pass
    sorted.append(head)




  