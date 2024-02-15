import numpy as np


def get_id_factory(width):
    return lambda x, y: x + y * width

def get_position_factory(width, height):
    return lambda index: (index % width, index // height)

def grid_to_graph(grid, get_id):
    rows, cols = len(grid), len(grid[0])
    size = rows * cols
    graph = np.zeros((size, size), dtype=bool)

    for i in range(rows):
        for j in range(cols):
            k0 = get_id(j, i)
            ki = get_id(j, i + 1)
            kj = get_id(j + 1, i)

            if grid[i][j] != 0:
                continue

            if i + 1 < rows and grid[i + 1][j] == 0:
                graph[k0][ki] = True
                graph[ki][k0] = True

            if j + 1 < cols and grid[i][j + 1] == 0:
                graph[k0][kj] = True
                graph[kj][k0] = True

    return graph

def clear_graph_corners(graph, ignore):
    degrees = np.sum(graph, axis=1)

    for index, degree in enumerate(degrees):
        if degree != 1 or index in ignore:
            continue

        current = int(index)

        while degrees[current] == 1:
            if current in ignore:
                break

            neighbor = np.where(graph[current])[0][0]
            graph[current][neighbor] = False
            graph[neighbor][current] = False
            degrees[current] -= 1
            degrees[neighbor] -= 1
            current = neighbor

def flood_graph(graph, origin, target):
    flood = np.zeros_like(graph[0], dtype=bool)
    candidates = [origin]
    found = False

    while len(candidates) > 0:
        current = candidates.pop(0)
        flood[current] = True
        neighbors = np.where(graph[current])[0]

        if not found:
            candidates.extend(neighbors)

        if current == target:
            found = True

    return np.where(flood)[0]

get_id = get_id_factory(5)
get_pos = get_position_factory(5, 5)
origin = (1, 4)
origin_id = get_id(*origin)
target = (4, 0)
target_id = get_id(*target)
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0]
]

for i, row in enumerate(grid):
    for j, col in enumerate(row):
        if i == origin[1] and j == origin[0]:
            print("@", end=" ")
        elif i == target[1] and j == target[0]:
            print("#", end=" ")
        else:
            print("X" if col else ".", end=" ")
    print("")

print("")

graph = grid_to_graph(grid, get_id)
candidates = flood_graph(graph, origin_id, target_id)

clear_graph_corners(graph, (origin_id, target_id))

for index, row in enumerate(graph):
    print(index, "-", end="\t")
    for col in row:
        print("X" if col else ".", end=" ")
    print()

print(candidates)

for i, row in enumerate(grid):
    for j, col in enumerate(row):
        if i == origin[1] and j == origin[0]:
            print("@", end=" ")
        elif i == target[1] and j == target[0]:
            print("#", end=" ")
        else:
            print("X" if col else ".", end=" ")
    print("")
