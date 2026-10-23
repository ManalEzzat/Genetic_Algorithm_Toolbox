# GA Toolbox + CVRP

A Genetic Algorithm toolbox written in Python from scratch (no GA libraries), and a program that uses it to solve the Capacitated Vehicle Routing Problem (CVRP).

## Project Structure

```
GA_CVRP_Project/
│
├── ga/
│   ├── chromosome.py          # binary, integer and float chromosomes
│   ├── selection.py           # roulette wheel and tournament selection
│   ├── crossover.py           # multi-point and order crossover
│   ├── mutation.py            # swap, inversion and bit flip mutation
│   ├── replacement.py         # generational and steady-state replacement
│   └── genetic_algorithm.py   # the GA class that connects everything
│
├── cvrp/
│   ├── problem.py             # CVRP data, decoding a chromosome into routes, printing
│   └── fitness.py             # fitness function and feasibility check
│
├── main.py                    # runs the GA on the CVRP example
└── README.md
```

## How to Run

Python 3 is needed, no extra libraries.

```
python3 main.py
```

## Part 1 – GA Toolbox

| Component | Options |
|---|---|
| Chromosomes | `BinaryChromosome`, `IntegerChromosome`, `FloatChromosome` |
| Selection | `"tournament"`, `"roulette"` |
| Crossover | `"multi_point"`, `"order"` |
| Mutation | `"swap"`, `"inversion"`, `"bit_flip"` |
| Replacement | `"generational"` (with elitism), `"steady_state"` |

### Using the toolbox for any problem

The GA does not know anything about the problem. The user gives it:

- `create_chromosome()` – returns a new random chromosome
- `fitness_func(chromosome)` – returns the fitness (higher is better)
- `feasibility_func(chromosome)` – returns True if the solution is feasible (optional)
- `repair_func(chromosome)` – fixes an infeasible chromosome (optional)

Example (OneMax problem):

```python
from ga.chromosome import BinaryChromosome
from ga.genetic_algorithm import GeneticAlgorithm

ga = GeneticAlgorithm(
    lambda: BinaryChromosome.generate_random(30),
    lambda c: sum(c.genes),
    crossover="multi_point",
    mutation="bit_flip",
    mutation_rate=0.03,
)
best = ga.run()
print(best.genes, best.fitness)
```

### Hyperparameters

All of them have default values and can be changed when creating the GA:

| Parameter | Default |
|---|---|
| `population_size` | 100 |
| `generations` | 500 |
| `selection` | `"tournament"` |
| `tournament_size` | 3 |
| `crossover` | `"order"` |
| `crossover_rate` | 0.9 |
| `mutation` | `"inversion"` |
| `mutation_rate` | 0.2 |
| `replacement` | `"generational"` |
| `elitism` | 2 |

### Infeasible solutions

We use two methods together:

1. **Repair** – if a repair function is given, infeasible children are fixed before they are evaluated.
2. **Penalty** – the fitness function adds a penalty to infeasible solutions so they get a low fitness.

The GA always returns the best **feasible** solution it found.

## Part 2 – CVRP

We use the example from the Google OR-Tools CVRP page: 16 customers, 1 depot, 4 vehicles, each with capacity 15.

- **Chromosome:** a permutation of the customers (1 to 16) stored in an `IntegerChromosome`.
- **Decoding:** customers are given to vehicle 0 in order until the next one does not fit, then we move to the next vehicle.
- **Fitness:** `1000 / (total distance + 1000 * overload)`, so shorter routes and no overload give higher fitness.
- **Repair:** removes repeated customers and adds the missing ones (needed with multi-point crossover).
- **Feasibility:** every customer is visited exactly once and no vehicle is over capacity.

## Results

The GA finds a solution with total distance **6208m**, the same as the OR-Tools result:

```
Objective: 6208
Route for vehicle 0:
 0 Load(0) -> 7 Load(8) -> 4 Load(12) -> 3 Load(14) -> 1 Load(15) -> 0 Load(15)
Distance of the route: 1552m
Load of the route: 15

Route for vehicle 1:
 0 Load(0) -> 12 Load(2) -> 11 Load(3) -> 15 Load(11) -> 13 Load(15) -> 0 Load(15)
Distance of the route: 1552m
Load of the route: 15

Route for vehicle 2:
 0 Load(0) -> 8 Load(8) -> 6 Load(12) -> 2 Load(13) -> 5 Load(15) -> 0 Load(15)
Distance of the route: 1552m
Load of the route: 15

Route for vehicle 3:
 0 Load(0) -> 9 Load(1) -> 10 Load(3) -> 16 Load(11) -> 14 Load(15) -> 0 Load(15)
Distance of the route: 1552m
Load of the route: 15

Total distance of all routes: 6208m
Total load of all routes: 60
```

The routes can be in a different order each run because the GA is random, but the total distance is 6208m.
