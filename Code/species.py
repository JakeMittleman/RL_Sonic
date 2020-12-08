import random

class Species:

    def __init__(self, rep):
        self.genomes = set()
        self.genomes.add(rep)
        self.rep = rep
        self.adj_fitness = 0

    def add_genome(self, genome):
        self.genomes.add(genome)

    def add_fitness(self, fitness):
        self.adj_fitness += fitness

    def update_rep(self):
        index = random.uniform(0, len(self.genomes)-1)
        self.rep = list(self.genomes)[int(round(index))]

    def __str__(self):
        return str.format('{}', self.rep.id)