def bellmanford(G, s, l):
    distance = dict()
    previous = dict()
    graph = []

    for key in G.keys():
        for val in G[key]:
            graph.append((key, val[0], val[1]))

    #Set distances for all vertices to infinity and previous vertices to None
    for vertex in G.keys():
        distance[vertex] = float('infinity')
        previous[vertex] = None

    #Set the distance of the start vertex to 0
    distance[s] = 0

    #Relax edges vertex-1 times
    for i in range(len(G)-1):
        for key, val, w in graph:
            d = w + distance[key]
            if d < distance[val]:
                distance[val] = d
                previous[val] = key

    #Check for negative weight cycles
    for key, val, w in graph:
        if distance[key] + w < distance[val]:
            return("Error")

    #Get the shortest path from s to l
    path = []
    current = l
    while current != None:
        path.append(current)
        current = previous[current]
    path.reverse()

    return 'result:', distance[l], path
#G = {v1:(v2, w)}
'''
graph = {
        'A': [('C', 4), ('F',7)],
        'B': [('E',9), ('H',3)],
        'C': [('A',4), ('F',2), ('D', 3), ('G', 9)],
        'D': [('C',3), ('G',7), ('E', 3)],
        'E': [('D',3), ('G',2), ('H', 7), ('B', 9)],
        'F': [('A',7), ('C', 2), ('G',8)],
        'G': [('F',8), ('H',3), ('C', 9), ('D', 7), ('E', 2)],
        'H': [('G',3), ('E',7), ('B', 3)]
        }

print(bellmanford(graph, 'A', 'B'))
'''