import math
import heapq

"""
    Here we will write our awesome algorithms
"""


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_neighbours(point, matrix):
    res = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            y = point[0] + i
            x = point[1] + j
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix) and [y, x] != point and matrix[y][x] != -1:
                res.append((y, x))
    return res


def Astar(matrix, start, end, metric=manhattan_dist):
    curr_point = start
    visited = {start: True}
    paths = []
    curr_path = []
    portal_point = None
    while curr_point != end:
        if portal_point: # if chosen point is portal
            curr_path.append(portal_point)
            paths.append(curr_path)
            curr_path = []
        curr_path.append(curr_point)
        neighbours = get_neighbours(curr_point, matrix)
        possible_neighbours = [p for p in neighbours if p not in visited or not visited[p]]
        candidates = []
        heapq.heapify(candidates)  # Candidates stored in min-heap
        for neighbour in possible_neighbours:
            (y, x) = neighbour
            neighbour_val = matrix[y][x]
            # Portal case:
            if isinstance(neighbour_val, list):
                [i, j] = neighbour_val
                g = metric(start, curr_point)
                f = g + metric(matrix[i][j], end)
                heapq.heappush(candidates, (f, tuple(neighbour_val), neighbour))
            # Point case:
            else:
                g = metric(start, curr_point)
                f = (g + metric(neighbour, end)) * neighbour_val
                heapq.heappush(candidates, (f, neighbour, None))
            visited[neighbour] = True
        (length, curr_point, portal_point) = heapq.heappop(candidates)
    curr_path.append(curr_point)
    paths.append(curr_path)
    return paths

def Dijkstra():
    pass