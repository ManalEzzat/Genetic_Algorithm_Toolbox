from typing import Union, List
from .problem import CVRPDataModel, decode_cvrp_chromosome

def check_cvrp_feasibility(chromosome: Union[List[int], object], data: CVRPDataModel) -> bool:
    """Verifying the feasibility of conditions, ensuring no client is overlooked or duplicated, and confirming that capacity limits are not exceeded."""
    genes = chromosome.genes if hasattr(chromosome, "genes") else chromosome
    num_customers = len(data.distance_matrix) - 1
    if len(genes) != num_customers or set(genes) != set(range(1, num_customers + 1)):
        return False
    return decode_cvrp_chromosome(genes, data).is_feasible

def evaluate_cvrp_violation(chromosome: Union[List[int], object], data: CVRPDataModel) -> float:
    """Calculating the total excess loads beyond vehicle capacities."""
    return float(decode_cvrp_chromosome(chromosome, data).total_overload)

def evaluate_cvrp_fitness(chromosome: Union[List[int], object], data: CVRPDataModel, penalty_multiplier: float = 1000.0,) -> float:
    """
    Fitness calculation function:
    - Calculates the total distance.
    - Adds a fixed penalty for each unit of excess load.
    - If the entity is a chromosome, the result is stored directly in `chromosome.fitness`.
    """
    genes = chromosome.genes if hasattr(chromosome, "genes") else chromosome
    sol = decode_cvrp_chromosome(genes, data)
    
    # Calculating the distance, with the addition of a penalty for exceeding the load limit (Static Penalty)
    total_cost = float(sol.total_distance + (sol.total_overload * penalty_multiplier))
    score = 1000.0 / (total_cost + 1e-6)
    if hasattr(chromosome, "fitness"):
        chromosome.fitness = score
    if hasattr(chromosome, "cost"):
        chromosome.cost = total_cost
    return score
