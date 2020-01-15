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


def get_path_length(paths, metric):
    res_length = 0
    for path in paths:
        for i in range(1, len(path)):
            res_length += metric(path[i - 1], path[i])
    return res_length


def astar(matrix, start, end, metric):
    visited = set(start)
    candidates = []
    heapq.heapify(candidates)
    heapq.heappush(candidates, (metric(start, end), (0, [[start]])))
    while len(candidates) > 0:
        f_prev, (g_prev, curr_path) = heapq.heappop(candidates)
        curr_point = curr_path[-1][-1]
        if curr_point in visited:
            continue
        if curr_point == end:
            return curr_path, get_path_length(curr_path, metric)
        visited.add(curr_point)

        neighbours = [p for p in get_neighbours(curr_point, matrix) if p not in visited]
        for neighbour in neighbours:
            (y, x) = neighbour
            neighbour_val = matrix[y][x]
            g = g_prev + metric(curr_point, neighbour)
            new_path = [row[:] for row in curr_path]
            new_path[-1].append(neighbour)
            # Portal case:
            if isinstance(neighbour_val, list):
                [i, j] = neighbour_val
                f = g + metric([i, j], end)
                new_path.append([(i, j)])
                heapq.heappush(candidates, (f, (g, new_path)))
            # Point case:
            else:
                f = (g + metric(neighbour, end)) * neighbour_val
                heapq.heappush(candidates, (f, (g, new_path)))
    return None, None


def best_first(matrix, start, end, metric):
    visited = set(start)
    candidates = []
    heapq.heapify(candidates)
    heapq.heappush(candidates, (metric(start, end), [[start]]))
    while len(candidates) > 0:
        f_prev, curr_path = heapq.heappop(candidates)
        curr_point = curr_path[-1][-1]
        if curr_point in visited:
            continue
        if curr_point == end:
            return curr_path, get_path_length(curr_path, metric)
        visited.add(curr_point)

        neighbours = [p for p in get_neighbours(curr_point, matrix) if p not in visited]
        for neighbour in neighbours:
            (y, x) = neighbour
            neighbour_val = matrix[y][x]
            new_path = [row[:] for row in curr_path]
            new_path[-1].append(neighbour)
            # Portal case:
            if isinstance(neighbour_val, list):
                [i, j] = neighbour_val
                f = metric((i, j), end)
                new_path.append([(i, j)])
                heapq.heappush(candidates, (f, new_path))
            # Point case:
            else:
                f = metric(neighbour, end) * neighbour_val
                heapq.heappush(candidates, (f, new_path))
    return None, None


def Dijkstra(matrix, start, end, metric=manhattan_dist):
    distances = {start: 0}
    visited = set()
    prev = {}
    candidates = []
    heapq.heapify(candidates)
    heapq.heappush(candidates, (0, start))

    while end not in distances:
        (curr_node_dist, curr_node) = heapq.heappop(candidates)
        if curr_node in visited:
            continue
        neighbours = get_neighbours(curr_node, matrix)
        visited.add(curr_node)
        for neighbour in neighbours:
            (y, x) = neighbour
            neighbour_val = matrix[y][x]
            alt_dist = metric(curr_node, neighbour) + curr_node_dist
            # Portal case:
            if isinstance(neighbour_val, list):
                neighbour_tuple = tuple(neighbour_val)
                if ((neighbour_tuple not in distances) or neighbour_tuple in distances and alt_dist < distances[
                    neighbour_tuple]) \
                        or ((neighbour not in distances) or neighbour in distances and alt_dist < distances[neighbour]):
                    distances[neighbour_tuple] = alt_dist
                    distances[neighbour] = alt_dist
                    prev[neighbour_tuple] = (curr_node, neighbour, alt_dist)
                    prev[neighbour] = (curr_node, neighbour_tuple, alt_dist)
                # heapq.heappush(candidates, (alt_dist, neighbour))
                heapq.heappush(candidates, (distances[neighbour_tuple], neighbour_tuple))
            # Point case:
            else:
                alt_dist *= neighbour_val
                if (neighbour not in distances) or neighbour in distances and alt_dist < distances[neighbour]:
                    distances[neighbour] = alt_dist
                    prev[neighbour] = (curr_node, None, alt_dist)
                heapq.heappush(candidates, (distances[neighbour], neighbour))
    paths = []
    curr_path = [end]
    curr_node = end
    path_dist = distances[end]
    prev_portal = False
    while curr_node != start:
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
    for path in paths:
        path.reverse()
    return paths, path_dist
