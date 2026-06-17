# PickPath — Warehouse Routing Optimizer

A routing simulation that models warehouse order fulfillment and finds efficient pick paths across a store grid. Built to compare an exact algorithm (guaranteed-optimal but slow) against a heuristic (fast and near-optimal), and to measure the tradeoff between them empirically.

Inspired by four years working online order fulfillment, where every wasted step across the floor adds up.

## The Problem

Given a list of items and their locations in a store, what is the shortest route to collect all of them and return to the start? This is the Traveling Salesman Problem (TSP) — easy to state, famously hard to solve perfectly at scale.

Movement is modeled with Manhattan distance (`|x₁−x₂| + |y₁−y₂|`) rather than straight-line distance, because warehouse travel happens along aisles, not diagonally through shelving.

## Approach

Two algorithms, built to be compared:

| Algorithm | Strategy | Guarantee | Complexity |
|-----------|----------|-----------|------------|
| *Brute force* | Evaluates every possible ordering of the route | Always finds the optimal route | O(n!) |
| *Nearest neighbor* | Greedily walks to the closest unvisited item | Fast, usually near-optimal, not guaranteed | O(n²) |

The brute-force solver gives a perfect baseline to measure the heuristic against. The whole point of the project is showing *why* a heuristic is needed: brute force becomes unusable as orders grow.

## Results

Benchmarked over 30 randomized orders (order size 6):

- *Nearest neighbor averaged ~9.6% above the optimal route distance* — near-optimal quality
- *...while running roughly 60× faster* than brute force

### Scaling test — why the heuristic matters

Running both algorithms on growing order sizes shows the factorial wall in action:

| Order size (n) | Brute force | Nearest neighbor |
|----------------|-------------|------------------|
| 4  | 0.0000s | 0.000005s |
| 5  | 0.0001s | 0.000006s |
| 6  | 0.0005s | 0.000006s |
| 7  | 0.0043s | 0.000012s |
| 8  | 0.0370s | 0.000016s |
| 9  | 0.3665s | 0.000019s |
| 10 | 4.0159s | 0.000020s |

Brute force grows roughly 10× per added item — from half a millisecond at n=6 to **4 seconds at n=10** — while nearest neighbor stays essentially flat. Extrapolated out, brute force would take days at n=15. That gap is the reason heuristics exist.

## Project Structure

```
pick-path/
├── store.py        # Store layout: items mapped to (x, y) grid coordinates
├── algorithms.py   # Distance math, brute-force solver, nearest-neighbor heuristic
├── benchmark.py    # Randomized accuracy benchmark + scaling test
└── README.md
```

## Running It

Requires Python 3. No external dependencies.

```bash
python benchmark.py
```

This runs the accuracy benchmark (heuristic vs. optimal across random orders) and the scaling test (runtime growth as order size increases).

## What I Learned

- Why heuristics exist: building the exact solver first, then watching it slow to a crawl as orders grew, made the need for an approximate algorithm concrete rather than theoretical.
- Nearest neighbor's weakness: a greedy "closest next" choice early can force a long detour later, which is why its routes land a few percent above optimal. The error is near zero on simple orders and larger on orders where greedy gets trapped.
- Measuring instead of assuming: the benchmark turns "this should be faster" into a real number, and the scaling test turns "O(n!) is slow" into an observable curve.

## Possible Next Steps

- A **2-opt improvement pass** to refine nearest-neighbor routes by untangling crossed segments
- A **grid visualization** of the computed path
- Configurable store layouts loaded from a file
