import random
import math


class Chromosome:
    """Base class for all chromosome representations."""

    def __init__(self, genes):
        self.genes = list(genes)
        self.fitness = None

    def get_genes(self):
        return self.genes.copy()

    def copy(self):
        """Return an independent copy of the chromosome."""
        new_chromosome = self.__class__.__new__(self.__class__)
        new_chromosome.genes = self.genes.copy()
        new_chromosome.fitness = self.fitness
        return new_chromosome

    def validate(self):
        """Implemented by each chromosome type."""
        raise NotImplementedError(
            "Each chromosome type must implement validate()."
        )

    def __len__(self):
        return len(self.genes)

    def __eq__(self, other):
        return (
            isinstance(other, Chromosome)
            and type(self) is type(other)
            and self.genes == other.genes
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.genes})"


class BinaryChromosome(Chromosome):
    """Chromosome whose genes are 0 or 1."""

    def __init__(self, genes):
        super().__init__(genes)
        if not self.validate():
            raise ValueError("Binary genes must be 0 or 1.")

    @classmethod
    def generate_random(cls, length):
        if length < 0:
            raise ValueError("Length cannot be negative.")

        genes = [random.randint(0, 1) for _ in range(length)]
        return cls(genes)

    def validate(self):
        return all(
            type(gene) is int and gene in (0, 1)
            for gene in self.genes
        )


class IntegerChromosome(Chromosome):
    """Chromosome whose genes are integers within given bounds."""

    def __init__(self, genes, min_value=None, max_value=None):
        super().__init__(genes)
        self.min_value = min_value
        self.max_value = max_value

        if not self.validate():
            raise ValueError("Invalid integer chromosome.")

    @classmethod
    def generate_random(cls, length, min_value, max_value):
        if length < 0:
            raise ValueError("Length cannot be negative.")
        if min_value > max_value:
            raise ValueError("min_value cannot exceed max_value.")

        genes = [
            random.randint(min_value, max_value)
            for _ in range(length)
        ]
        return cls(genes, min_value, max_value)

    def validate(self):
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                return False

        for gene in self.genes:
            if type(gene) is not int:
                return False

            if self.min_value is not None and gene < self.min_value:
                return False

            if self.max_value is not None and gene > self.max_value:
                return False

        return True

    def copy(self):
        new_chromosome = super().copy()
        new_chromosome.min_value = self.min_value
        new_chromosome.max_value = self.max_value
        return new_chromosome


class FloatChromosome(Chromosome):
    """Chromosome whose genes are finite floating-point numbers."""

    def __init__(self, genes, min_value=None, max_value=None):
        super().__init__(genes)
        self.min_value = min_value
        self.max_value = max_value

        if not self.validate():
            raise ValueError("Invalid floating-point chromosome.")

    @classmethod
    def generate_random(cls, length, min_value, max_value):
        if length < 0:
            raise ValueError("Length cannot be negative.")
        if min_value > max_value:
            raise ValueError("min_value cannot exceed max_value.")

        genes = [
            random.uniform(min_value, max_value)
            for _ in range(length)
        ]
        return cls(genes, min_value, max_value)

    def validate(self):
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                return False

        for gene in self.genes:
            if type(gene) not in (int, float):
                return False

            if not math.isfinite(gene):
                return False

            if self.min_value is not None and gene < self.min_value:
                return False

            if self.max_value is not None and gene > self.max_value:
                return False

        return True

    def copy(self):
        new_chromosome = super().copy()
        new_chromosome.min_value = self.min_value
        new_chromosome.max_value = self.max_value
        return new_chromosome


