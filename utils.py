# Calculate the total distance in the graph

def calculate_total_distance(graph, path):
    total_distance = 0
    for x in range(len(path) - 1):
        a = path[x]
        b = path[x + 1]

        total_distance += graph[a][b]['distance']
    return total_distance
