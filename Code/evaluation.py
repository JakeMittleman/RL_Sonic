from species import Species
import random

class Evaluator:

    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.species_map = {}
        self.score_map = {}
        self.genomes = []
        self.species = []

    def evaluate(self):
        for genome in self.genomes:
            found_species = False

            for species in self.species:
                if genome.get_compatibility_distance(species.rep, 1.0, 1.0, 0.4) < 3.0:
                    species.add_gene(genome)
                    self.species_map[genome.id] = species
                    found_species = True

            if not found_species:
                species = Species(genome)
                self.species_map[genome.id] = species

        for genome in self.genomes:
            fitness = genome.fitness
            species = self.species_map[genome.id]
            adj_fitness = fitness / (len(species.genomes) if species.genomes else 1)
            species.add_fitness(adj_fitness)
            self.score_map[genome.id] = adj_fitness

        next_generation = []
        for species in self.species:
            sorted_genomes = sorted(species.genomes, key=lambda x: x.fitness, reverse=True)
            fittest_genome = sorted_genomes[0]
            next_generation.append(fittest_genome)

        while len(next_generation) < self.pop_size:
            species = self.get_random_species()

            parentA = self.get_random_genome(species)
            parentB = self.get_random_genome(species)
            while parentB == parentA:
                parentB = self.get_random_genome(species)

            new_genome = parentA.cross(parentB)

            if random.random() < 0.8:
                new_genome.mutate()

            if random.random() < 0.05:
                new_genome.mutate_add_connection()

            if random.random() < 0.03:
                new_genome.mutate_add_node()


            next_generation.append(new_genome)

        self.genomes = next_generation

    def get_random_species(self):
        total_weight = 0.0
        for species in self.species:
            total_weight += species.adj_fitness

        threshold = random.random() * total_weight
        meter = 0.0
        for species in self.species:
            meter += species.adj_fitness
            if meter >= threshold:
                return species

    def get_random_genome(self, species):
        genomes = species.genomes
        total_weight = 0.0
        for genome in genomes:
            total_weight += genome.fitness

        threshold = random.random() * total_weight
        meter = 0.0
        for genome in genomes:
            meter += genome.fitness
            if meter >= threshold:
                return genome
