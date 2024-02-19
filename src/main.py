import argparse
from enum import Enum

import numpy as np


class Actions(Enum):
    GO_UP = 0
    GO_DOWN = 1
    GO_LEFT = 2
    GO_RIGHT = 3
    PICK_PASSENGER = 4
    DROP_PASSENGER = 5


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

def flood_graph(graph, origin, target):
    flood = np.zeros_like(graph[0], dtype=bool)
    candidates = [origin]
    found = False

    while len(candidates) > 0:
        current = candidates.pop(0)

        if flood[current]:
            continue

        flood[current] = True
        neighbors = np.where(graph[current])[0]

        if not found:
            candidates.extend(neighbors)

        if current == target:
            found = True

    return np.where(flood)[0]

def get_graph_resume(graph, ids):
    return [
        [
            col
            for j, col in enumerate(row)
            if j in ids
        ]
        for i, row in enumerate(graph)
        if i in ids
    ]

def pathfind(graph, origin, target):
    path = [origin]
    ignore = [origin]
    current = origin
    size = len(graph)

    while current != target:
        row = graph[current]

        before = None
        for i in range(current - 1, -1, -1):
            if row[i]:
                if i in path or i in ignore:
                    continue
            
                before = i
                break

        after = None
        for i in range(current + 1, size):
            if row[i]:
                if i in path or i in ignore:
                    continue
            
                after = i
                break

        if (current > target or after is None) and before is not None:
            path.append(before)
        elif after is not None:
            path.append(after)
        else:
            ignore.append(path.pop())

        current = path[-1]

    return path

def get_directions(path):
    directions = []

    for d0, df in zip(path[:-1], path[1:]):
        if d0 == df + 1:
            directions.append(Actions.GO_LEFT)
        elif d0 == df - 1:
            directions.append(Actions.GO_RIGHT)
        elif d0 > df:
            directions.append(Actions.GO_UP)
        else:
            directions.append(Actions.GO_DOWN)

    return directions

def read_grid_file(filename):
    origin = None
    passager = None
    target = None
    grid = []

    for row in open(filename):
        args = row.strip("\n").split(" ")

        if args[0] == "o":
            origin = (int(args[1]), int(args[2]))
        elif args[0] == "p":
            passager = (int(args[1]), int(args[2]))
        elif args[0] == "t":
            target = (int(args[1]), int(args[2]))
        elif args[0] in (".", "#"):
            grid.append([i == "#" for i in args])

    return origin, passager, target, grid

def get_script(origin, passager, target, grid):
    width = len(grid[0])
    height = len(grid)
    get_id = get_id_factory(width)
    get_pos = get_position_factory(width, height)
    origin_id = get_id(*origin)
    passager_id = get_id(*passager)
    target_id = get_id(*target)

    graph_base = grid_to_graph(grid, get_id)
    ids = flood_graph(graph_base, origin_id, passager_id)
    origin_id2 = np.where(ids == origin_id)[0][0]
    passager_id2 = np.where(ids == passager_id)[0][0]
    graph = get_graph_resume(graph_base, ids)
    path = pathfind(graph, origin_id2, passager_id2)
    path = [ids[i] for i in path]
    directions1 = get_directions(path)


    ids = flood_graph(graph_base, passager_id, target_id)
    passager_id2 = np.where(ids == passager_id)[0][0]
    target_id2 = np.where(ids == target_id)[0][0]
    graph = get_graph_resume(graph_base, ids)
    path = pathfind(graph, passager_id2, target_id2)
    path = [ids[i] for i in path]
    directions2 = get_directions(path)

    return (
        *directions1,
        Actions.PICK_PASSENGER,
        *directions2,
        Actions.DROP_PASSENGER,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some file.')
    parser.add_argument('filename', help='The path to the grid file.')
    
    args = parser.parse_args()

    print("Taxi script:")

    for step in get_script(*read_grid_file(args.filename)):
        print("-", " ".join(step.name.capitalize().split("_")))
