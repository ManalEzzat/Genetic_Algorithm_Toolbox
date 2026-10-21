import random

def multi_point_crossover(parent1, parent2, num_points=2, pc=1.0):
    """
    multi-point crossover for binary, integer, or float chromosomes.
    Swaps segments of genes between two parents at multiple random cut points.
    """
    if random.random() > pc:
        return parent1.copy(), parent2.copy()
    
    size = len(parent1.genes)
    if num_points >= size:
        num_points = size - 1
        
    # Generate random unique cut points and sort them
    points = sorted(random.sample(range(1, size), num_points))
    points = [0] + points + [size]
    
    c1_genes = []
    c2_genes = []
    swap = False
    
    for i in range(len(points) - 1):
        start, end = points[i], points[i+1]
        if swap:
            c1_genes.extend(parent2.genes[start:end])
            c2_genes.extend(parent1.genes[start:end])
        else:
            c1_genes.extend(parent1.genes[start:end])
            c2_genes.extend(parent2.genes[start:end])
        swap = not swap
        
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    child1.genes = c1_genes
    child2.genes = c2_genes
    
    # reset fitness and cost because the genes have changed
    child1.fitness, child1.cost = None, None
    child2.fitness, child2.cost = None, None
    
    return child1, child2

def order_crossover(parent1, parent2, pc=1.0):
    """
    order crossover for permutation chromosomes.
    preserves the relative sequence of genes to prevent invalid routes.
    """
    if random.random() > pc:
        return parent1.copy(), parent2.copy()
    
    size = len(parent1.genes)
    start, end = sorted(random.sample(range(size), 2))
    
    def apply_ox1(p1, p2):
        child_genes = [None] * size
        
        # copy the randomly selected subset from the first parent
        child_genes[start:end+1] = p1.genes[start:end+1]
        
        # filter out the copied genes from the second parent
        p2_filtered = [g for g in p2.genes if g not in child_genes[start:end+1]]
        
        # insert the remaining genes starting from the index after 'end', wrapping around
        insert_pos = (end + 1) % size
        for g in p2_filtered:
            child_genes[insert_pos] = g
            insert_pos = (insert_pos + 1) % size
            
        child = p1.copy()
        child.genes = child_genes
        child.fitness, child.cost = None, None
        return child

    child1 = apply_ox1(parent1, parent2)
    child2 = apply_ox1(parent2, parent1)
    
    return child1, child2