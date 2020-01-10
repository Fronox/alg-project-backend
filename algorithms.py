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
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix) and (y, x) != point and matrix[y][x] != -1:
                res.append((y, x))
    return res


def Astar(matrix, start, end, metric=manhattan_dist):
    curr_point = start
    visited = {start: True}
    paths = []
    curr_path = []
    res_length = 0
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
        (_, new_point, portal_point) = heapq.heappop(candidates)
        res_length += metric(curr_point, new_point)
        curr_point = new_point
    curr_path.append(curr_point)
    paths.append(curr_path)
    return (paths, res_length)

def Dijkstra(matrix, start, end, metric=manhattan_dist):
    distances = {start: 0}
    visited = {}
    prev = {}

    while len(visited) < len(distances):
        unvisited_points = list(filter(lambda x: x[0] not in visited, distances.items()))
        (curr_node, curr_node_dist) = min(unvisited_points, key=lambda x: x[1])
        neighbours = get_neighbours(curr_node, matrix)
        print(neighbours)
        for neighbour in neighbours:
            (y, x) = neighbour
            neighbour_val = matrix[y][x]
            alt_dist = metric(curr_node, neighbour) + curr_node_dist
            # Portal case:
            if isinstance(neighbour_val, list):
                neighbour_tuple = tuple(neighbour_val)
                if ((neighbour_tuple not in distances) or neighbour_tuple in distances and alt_dist < distances[neighbour_tuple]) \
                        or ((neighbour not in distances) or neighbour in distances and alt_dist < distances[neighbour]):
                    distances[neighbour_tuple] = alt_dist
                    distances[neighbour] = alt_dist
                    prev[neighbour_tuple] = (curr_node, neighbour, alt_dist)
                    prev[neighbour] = (curr_node, neighbour_tuple, alt_dist)
            # Point case:
            else:
                if (neighbour not in distances) or neighbour in distances and alt_dist < distances[neighbour]:
                    distances[neighbour] = alt_dist
                    prev[neighbour] = (curr_node, None, alt_dist)
        visited[curr_node] = True

    paths = []
    curr_path = [end]
    curr_node = end
    path_dist = distances[end]
    prev_portal = False
    while curr_node != start:
        print(curr_node)
        (prev_node, portal_node, dist) = prev[curr_node]
        if portal_node and not prev_portal:
            paths.append(curr_path)
            curr_path = [portal_node]
            prev_node = portal_node
            prev_portal = True
        else:
            curr_path = [prev_node] + curr_path
            if prev_portal:
                prev_portal = False
        curr_node = prev_node
    paths.append(curr_path)
    paths.reverse()
    return paths, path_dist