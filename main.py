import random

from ga.chromosome import IntegerChromosome
from ga.genetic_algorithm import GeneticAlgorithm
from cvrp.problem import CVRPDataModel, decode_cvrp_chromosome, print_ortools_solution
from cvrp.fitness import evaluate_cvrp_fitness, check_cvrp_feasibility


data = CVRPDataModel()
customers = list(range(1, len(data.distance_matrix)))


def create_chromosome():
    genes = customers.copy()
    random.shuffle(genes)
    return IntegerChromosome(genes, 1, len(customers))


def repair(chromosome):
    genes = []
    for g in chromosome.genes:
        if g not in genes:
            genes.append(g)
    for c in customers:
        if c not in genes:
            genes.append(c)
    chromosome.genes = genes
    return chromosome


def fitness(chromosome):
    return evaluate_cvrp_fitness(chromosome, data)


def feasible(chromosome):
    return check_cvrp_feasibility(chromosome, data)


ga = GeneticAlgorithm(
    create_chromosome,
    fitness,
    feasible,
    repair,
    population_size=150,
    generations=600,
    mutation_rate=0.3,
)

best = ga.run()
solution = decode_cvrp_chromosome(best, data)
print()
print_ortools_solution(solution, data)
