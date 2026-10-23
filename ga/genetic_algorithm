import random

from .selection import roulette_wheel_selection, tournament_selection
from .crossover import multi_point_crossover, order_crossover
from .mutation import swap_mutation, inversion_mutation, bit_flip_mutation
from .replacement import generational_replacement, steady_state_replacement


class GeneticAlgorithm:

    def __init__(self, create_chromosome, fitness_func, feasibility_func=None, repair_func=None,
                 population_size=100, generations=500,
                 selection="tournament", tournament_size=3,
                 crossover="order", crossover_rate=0.9,
                 mutation="inversion", mutation_rate=0.2,
                 replacement="generational", elitism=2):
        self.create_chromosome = create_chromosome
        self.fitness_func = fitness_func
        self.feasibility_func = feasibility_func
        self.repair_func = repair_func

        self.population_size = population_size
        self.generations = generations
        self.selection = selection
        self.tournament_size = tournament_size
        self.crossover = crossover
        self.crossover_rate = crossover_rate
        self.mutation = mutation
        self.mutation_rate = mutation_rate
        self.replacement = replacement
        self.elitism = elitism

        self.population = []
        self.pool = []

    def is_feasible(self, c):
        if self.feasibility_func is None:
            return True
        return self.feasibility_func(c)

    def fix_and_evaluate(self, c):

        if self.repair_func is not None and not self.is_feasible(c):
            c = self.repair_func(c)
            c.fitness = None
        if c.fitness is None:
            c.fitness = self.fitness_func(c)
        return c

    def select_parents(self):
        if self.selection == "roulette":
            return roulette_wheel_selection(self.population, 2)

        if len(self.pool) < 2:
            self.pool = tournament_selection(self.population, self.tournament_size)
            random.shuffle(self.pool)
        return [self.pool.pop(), self.pool.pop()]

    def make_children(self):
        p1, p2 = self.select_parents()

        if self.crossover == "multi_point":
            c1, c2 = multi_point_crossover(p1, p2, 2, self.crossover_rate)
        else:
            c1, c2 = order_crossover(p1, p2, self.crossover_rate)

        if self.mutation == "swap":
            c1 = swap_mutation(c1, self.mutation_rate)
            c2 = swap_mutation(c2, self.mutation_rate)
        elif self.mutation == "bit_flip":
            c1 = bit_flip_mutation(c1, self.mutation_rate)
            c2 = bit_flip_mutation(c2, self.mutation_rate)
        else:
            c1 = inversion_mutation(c1, self.mutation_rate)
            c2 = inversion_mutation(c2, self.mutation_rate)

        return [self.fix_and_evaluate(c1), self.fix_and_evaluate(c2)]

    def next_generation(self):
        self.pool = []

        if self.replacement == "steady_state":
            for _ in range(self.population_size // 2):
                children = self.make_children()
                worst = sorted(self.population, key=lambda c: c.fitness)[:2]
                self.population = steady_state_replacement(self.population, worst, children)
            return

        children = []
        while len(children) < self.population_size:
            children += self.make_children()
        children = children[:self.population_size]

        new_population = generational_replacement(self.population, children)

        old_sorted = sorted(self.population, key=lambda c: c.fitness, reverse=True)
        new_population.sort(key=lambda c: c.fitness)
        for i in range(self.elitism):
            new_population[i] = old_sorted[i].copy()

        self.population = new_population

    def run(self):
        self.population = []
        for _ in range(self.population_size):
            self.population.append(self.fix_and_evaluate(self.create_chromosome()))

        best = None
        for gen in range(1, self.generations + 1):
            self.next_generation()

            for c in self.population:
                if self.is_feasible(c) and (best is None or c.fitness > best.fitness):
                    best = c.copy()

            if gen % 100 == 0 and best is not None:
                print(f"Generation {gen}: best fitness = {best.fitness:.6f}")

        if best is None:
            best = max(self.population, key=lambda c: c.fitness).copy()
        return best
