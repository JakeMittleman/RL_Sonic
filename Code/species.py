class Species:

    def __init__(self, rep):
        self.genomes = [rep]
        self.rep = rep
        self.adj_fitness = 0

    def add_genome(self, genome):
        self.genomes.append(genome)

    def add_fitness(self, fitness):
        self.adj_fitness += fitness

    def __str__(self):
        return str.format('{}', self.rep.id)