# algorithms.py
# Core optimization logic for warehouse routing.

from itertools import permutations
from store import store

# Calculates the distance between two points
def calculate_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# Compute total travel distance for a full route,
def calculate_route_distance(route):
    current_position = (0, 0)
    total_distance = 0

    for item in route:

        item_location = store[item]
        total_distance += calculate_distance(current_position, item_location)
        current_position = item_location

    # Return to the origin
    total_distance += calculate_distance(current_position, (0, 0))
    return total_distance

# Evaluate all possible permutations of the order
# Guarantees optimal solution but has factorial time complexity O(n!)
def brute_force_route(order):
    shortest_distance = float("inf")
    best_route = None

    for route in permutations(order):
        distance = calculate_route_distance(route)
        if distance < shortest_distance:
            shortest_distance = distance
            best_route = route

    return best_route, shortest_distance


# Heuristic algorithm for finding a near-optimal route
# Faster than brute force (O(n²)) but not always optimal
def nearest_neighbor_route(order):
    remaining = order.copy()
    route = []
    current_position = (0, 0)

    while remaining:
        closest_item = None
        shortest_distance = float("inf")
        for item in remaining:
            distance = calculate_distance(current_position, store[item])
            if distance < shortest_distance:
                shortest_distance = distance
                closest_item = item

        route.append(closest_item)
        current_position = store[closest_item]
        remaining.remove(closest_item)

    total_distance = calculate_route_distance(route)
    return route, total_distance