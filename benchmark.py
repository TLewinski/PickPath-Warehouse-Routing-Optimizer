# benchmark.py
# Experimental evaluation for routing algorithms
# Compare optimal (brute force) vs heuristic (nearest neighbor)
# Metrics collected:
#   - Total route distance (solution quality)
#   - Execution time (performance)
#   - Relative error vs optimal solution

import random
import time
from algorithms import brute_force_route, nearest_neighbor_route
from store import store


# Runs both routing algorithms on a single input instance.
def run_single_test(order):

    # Brute force (optimal solution)
    start = time.perf_counter()
    brute_route, brute_distance = brute_force_route(order)
    brute_time = time.perf_counter() - start

    # Nearest neighbor (heuristic)
    start = time.perf_counter()
    nn_route, nn_distance = nearest_neighbor_route(order)
    nn_time = time.perf_counter() - start

    # error vs optimal
    error_percent = ((nn_distance - brute_distance) / brute_distance) * 100

    return brute_distance, nn_distance, brute_time, nn_time, error_percent

#Generates multiple random orders and evaluates both algorithms
# to produce statistically meaningful averages
def benchmark(num_trials=30, order_size=6):
    items = list(store.keys())
    print(f"\nRunning {num_trials} trials (order size = {order_size})\n")

    total_error = 0
    total_brute_time = 0
    total_nn_time = 0

    for i in range(num_trials):
        # Randomly simulate a customer order
        order = random.sample(items, order_size)
        brute_d, nn_d, brute_t, nn_t, error = run_single_test(order)

        total_error += error
        total_brute_time += brute_t
        total_nn_time += nn_t

        print(f"Trial {i+1}: error={error:.2f}% | brute={brute_t:.4f}s | nn={nn_t:.5f}s")
    # Results
    print("\n===== SUMMARY =====")
    print("Avg error:", total_error / num_trials, "%")
    print("Avg brute time:", total_brute_time / num_trials, "s")
    print("Avg nn time:", total_nn_time / num_trials, "s")


#Stress test showing scaling behavior.
#Increases input size to demonstrate:
#   - factorial growth of brute force (O(n!))
#   - near-linear growth of greedy heuristic (O(n²))
def scaling_test():

    items = list(store.keys())
    print("\n===== SCALING TEST =====\n")

    for size in range(4, 11):

        order = random.sample(items, size)
        # Measure brute force scaling behavior
        start = time.perf_counter()
        brute_force_route(order)
        brute_time = time.perf_counter() - start
        # Measure heuristic scaling behavior
        start = time.perf_counter()
        nearest_neighbor_route(order)
        nn_time = time.perf_counter() - start

        print(f"n={size} | brute={brute_time:.4f}s | nn={nn_time:.6f}s")