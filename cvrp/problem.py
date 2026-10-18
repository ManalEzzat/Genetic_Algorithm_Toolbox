import random
from dataclasses import dataclass, field
from typing import List, Union
from ga.chromosome import Chromosome

class PermutationChromosome:
    """A permutation chromosome compatible with the structure of Chromosome."""
    def __init__(self, genes, min_value=1, max_value=16):
        self.genes = list(genes)
        self.min_value = min_value
        self.max_value = max_value
        self.fitness = None
        if not self.validate():
            raise ValueError("Invalid permutation chromosome.")
    def get_genes(self):
        return self.genes.copy()
    def copy(self):
        new_chromosome = self.__class__.__new__(self.__class__)
        new_chromosome.genes = self.genes.copy()
        new_chromosome.min_value = self.min_value
        new_chromosome.max_value = self.max_value
        new_chromosome.fitness = self.fitness
        return new_chromosome
    @classmethod
    def generate_random(cls, min_value=1, max_value=16):
        genes = list(range(min_value, max_value + 1))
        random.shuffle(genes)
        return cls(genes, min_value, max_value)
    def validate(self):
        expected_set = set(range(self.min_value, self.max_value + 1))
        return (
            len(self.genes) == len(expected_set)
            and set(self.genes) == expected_set
            and all(isinstance(g, int) for g in self.genes)
        )
    def __len__(self):
        return len(self.genes)
    def __repr__(self):
        return f"PermutationChromosome({self.genes}, fitness={self.fitness})"

@dataclass
class CVRPDataModel:
    """Google OR-Tools CVRP Benchmark Data Model."""
    distance_matrix: List[List[int]] = field(
        default_factory=lambda: [
            [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
            [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
            [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
            [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
            [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
            [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
            [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
            [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
            [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
            [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
            [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
            [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
            [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
            [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
            [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
            [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
            [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
        ]
    )
    demands: List[int] = field(default_factory=lambda: [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8])
    vehicle_capacities: List[int] = field(default_factory=lambda: [15, 15, 15, 15])
    num_vehicles: int = 4
    depot: int = 0

@dataclass
class DecodedRoute:
    nodes: List[int] = field(default_factory=list)
    distance: int = 0
    load: int = 0
    capacity: int = 15

@dataclass
class DecodedCVRPSolution:
    routes: List[DecodedRoute] = field(default_factory=list)
    total_distance: int = 0
    total_load: int = 0
    total_overload: int = 0
    is_feasible: bool = True

def decode_cvrp_chromosome(
    chromosome: Union[List[int], object], data: CVRPDataModel
) -> DecodedCVRPSolution:
    """
    Decodes the sequence into paths for 4 vehicles.
    Supports receiving a list of standard numbers or a chromosome object that contains a 'genes' property.
    """
    genes = chromosome.genes if hasattr(chromosome, "genes") else chromosome
    routes = [
        DecodedRoute(capacity=data.vehicle_capacities[v])
        for v in range(data.num_vehicles)
    ]
    curr_v = 0
    for customer in genes:
        demand = data.demands[customer]
        if (
            curr_v < data.num_vehicles - 1
            and routes[curr_v].load + demand > data.vehicle_capacities[curr_v]
        ):
            curr_v += 1
        routes[curr_v].nodes.append(customer)
        routes[curr_v].load += demand
    total_distance = 0
    total_load = 0
    total_overload = 0
    is_feasible = True
    dist_mat = data.distance_matrix
    depot = data.depot
    for r in routes:
        if r.nodes:
            d = dist_mat[depot][r.nodes[0]]
            for i in range(len(r.nodes) - 1):
                d += dist_mat[r.nodes[i]][r.nodes[i + 1]]
            d += dist_mat[r.nodes[-1]][depot]
            r.distance = d
        else:
            r.distance = 0
        total_distance += r.distance
        total_load += r.load
        if r.load > r.capacity:
            is_feasible = False
            total_overload += r.load - r.capacity
    return DecodedCVRPSolution(
        routes=routes,
        total_distance=total_distance,
        total_load=total_load,
        total_overload=total_overload,
        is_feasible=is_feasible,
    )


def print_ortools_solution(sol: DecodedCVRPSolution, data: CVRPDataModel) -> None:
    """Print the result using the same style as the Google OR-Tools library."""
    print(f"Objective: {sol.total_distance}")
    total_distance = 0
    total_load = 0
    for v_id, route in enumerate(sol.routes):
        plan_output = f"Route for vehicle {v_id}:\n "
        cum_load = 0
        plan_output += f"{data.depot} Load({cum_load}) -> "
        for node in route.nodes:
            cum_load += data.demands[node]
            plan_output += f"{node} Load({cum_load}) -> "
        plan_output += f"{data.depot} Load({cum_load})\n"
        plan_output += f"Distance of the route: {route.distance}m\n"
        plan_output += f"Load of the route: {route.load}\n"
        print(plan_output)
        total_distance += route.distance
        total_load += route.load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")
