import random

def roulette_wheel_selection(population, num_parents=2):
    if not population:
        raise ValueError("Population cannot be empty.")
    if num_parents <= 0:
        raise ValueError("num_parents must be greater than 0.")

    if any(ind.fitness is None for ind in population):
        raise ValueError("All individuals must have an assigned fitness value.")

    total_fitness = sum(ind.fitness for ind in population)

    if total_fitness == 0:
        return [random.choice(population).copy() for _ in range(num_parents)]

    selected = []
    for _ in range(num_parents):
        pick = random.uniform(0, total_fitness)
        current = 0.0

        for individual in population:
            current += individual.fitness
            if current >= pick:
                selected.append(individual.copy())
                break

    return selected


def tournament_selection(population, n=2):

    if not population:
        raise ValueError("Population cannot be empty.")
    if n <= 0 or n > len(population):
        raise ValueError("Invalid tournament size n.")

    if any(ind.fitness is None for ind in population):
        raise ValueError("All individuals must have an assigned fitness value.")


    remaining = population.copy()
    selected = []

    while remaining:
        k = min(n, len(remaining))
        tournament_group = random.sample(remaining, k)

        winner = max(tournament_group, key=lambda ind: ind.fitness)

        for _ in range(n):
            selected.append(winner.copy())

        for participant in tournament_group:
            remaining.remove(participant)

    return selected
