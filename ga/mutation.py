import random

def swap_mutation(chromosome, pm=0.1):
    """
    Randomly selects two genes in the chromosome and swaps their positions.
    """
    child = chromosome.copy()
    
    if random.random() <= pm:
        size = len(child.genes)
        idx1, idx2 = random.sample(range(size), 2)
        
        child.genes[idx1], child.genes[idx2] = child.genes[idx2], child.genes[idx1]
        
        # reset fitness
        child.fitness, child.cost = None, None
        
    return child

def inversion_mutation(chromosome, pm=0.1):
    """
    Selects a random contiguous subset of the chromosome and reverses its order.
    """
    child = chromosome.copy()
    
    if random.random() <= pm:
        size = len(child.genes)
        start, end = sorted(random.sample(range(size), 2))
        
        # Reverse the sublist in place
        child.genes[start:end+1] = reversed(child.genes[start:end+1])
        
        child.fitness, child.cost = None, None
        
    return child

def bit_flip_mutation(chromosome, pm=0.1):
    """
    Iterates through every gene and flips it with probability Pm.
    """
    child = chromosome.copy()
    mutated = False
    
    for i in range(len(child.genes)):
        if random.random() <= pm:
            # Flips 0 to 1, and 1 to 0
            child.genes[i] = 1 - child.genes[i]
            mutated = True

    # reset fitness only if a mutation applied to the chromosome, otherwise don't reset
    if mutated:
        child.fitness, child.cost = None, None
        
    return child