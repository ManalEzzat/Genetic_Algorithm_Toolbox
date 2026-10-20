def generational_replacement(old_population, offspring_population):

    if not old_population or not offspring_population:
        raise ValueError("Populations cannot be empty.")

    if len(offspring_population) != len(old_population):
        raise ValueError("Offspring population size must match the old population size.")

    return [child.copy() for child in offspring_population]


def steady_state_replacement(population, parents, offspring):
    if not population:
        raise ValueError("Population cannot be empty.")

    if len(parents) != len(offspring):
        raise ValueError("Number of parents must match the number of offspring.")

    new_population = [ind.copy() for ind in population]

    for parent, child in zip(parents, offspring):
        for i, current_individual in enumerate(new_population):
            if current_individual == parent:
                new_population[i] = child.copy()
                break

    return new_population
