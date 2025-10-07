<<<<<<< HEAD
import random

def distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[(i+1)%len(route)]] for i in range(len(route)))

def tsp_hill_climb(dist_matrix, iterations=1000):
    n = len(dist_matrix)
    current = list(range(n))
    random.shuffle(current)
    current_cost = distance(current, dist_matrix)

    for _ in range(iterations):
        a, b = random.sample(range(n), 2)
        neighbor = current[:]
        neighbor[a], neighbor[b] = neighbor[b], neighbor[a]
        neighbor_cost = distance(neighbor, dist_matrix)
        if neighbor_cost < current_cost:
            current, current_cost = neighbor, neighbor_cost
    return current, current_cost

def tsp_random_restart(dist_matrix, restarts=10, iterations=1000):
    best_route, best_cost = None, float("inf")
    for _ in range(restarts):
        route, cost = tsp_hill_climb(dist_matrix, iterations)
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost

if __name__ == "__main__":
    dist_matrix = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    solution, cost = tsp_random_restart(dist_matrix)
=======
import random

def distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[(i+1)%len(route)]] for i in range(len(route)))

def tsp_hill_climb(dist_matrix, iterations=1000):
    n = len(dist_matrix)
    current = list(range(n))
    random.shuffle(current)
    current_cost = distance(current, dist_matrix)

    for _ in range(iterations):
        a, b = random.sample(range(n), 2)
        neighbor = current[:]
        neighbor[a], neighbor[b] = neighbor[b], neighbor[a]
        neighbor_cost = distance(neighbor, dist_matrix)
        if neighbor_cost < current_cost:
            current, current_cost = neighbor, neighbor_cost
    return current, current_cost

def tsp_random_restart(dist_matrix, restarts=10, iterations=1000):
    best_route, best_cost = None, float("inf")
    for _ in range(restarts):
        route, cost = tsp_hill_climb(dist_matrix, iterations)
        if cost < best_cost:
            best_route, best_cost = route, cost
    return best_route, best_cost

if __name__ == "__main__":
    dist_matrix = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    solution, cost = tsp_random_restart(dist_matrix)
>>>>>>> 52317de (Week 6,7,8 added.)
    print("Best route:", solution, "Cost:", cost)