from species import Species
import random

# Tweakable
C1 = 2.5
C2 = 2.5
C3 = 3
DIS_THRES = 1

class Evaluator:

    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.species_map = {}
        self.score_map = {}
        self.genomes = []
        self.species = set()
        self.threshold = 50000

    def evaluate(self):
        mutated_connection_genes = {}
        if self.species:
            for species in self.species:
                species.update_rep()
                # species.genomes = set()
        # Assign genomes to species.
        else:
            for genome in self.genomes:
                found_species = False
                for species in self.species:
                    N = max(len(genome.connection_genes), len(species.rep.connection_genes))
                    if N < 20:
                        N = 1
                    if genome.get_compatibility_distance(species.rep, C1, C2, C3, N) < DIS_THRES:
                        species.add_genome(genome)
                        self.species_map[genome.id] = species
                        found_species = True
                        break

                if not found_species:
                    species = Species(genome)
                    self.species.add(species)
                    self.species_map[genome.id] = species

        # Get the adjusted fitness of the species.
        for genome in self.genomes:
            fitness = genome.fitness
            species = self.species_map[genome.id]
            adj_fitness = fitness / \
                (len(species.genomes) if species.genomes else 1)
            species.add_fitness(adj_fitness)
            self.score_map[genome.id] = adj_fitness

        print('Species:', len(self.species))
        # Put the best genomes of each species into the next generation.
        next_generation = []
        for species in self.species:
            sorted_genomes = sorted(species.genomes, key=lambda x: x.fitness, reverse=True)
            fittest_genome = sorted_genomes[0]
            next_generation.append(fittest_genome)

        print('Best performing genomes in each species')
        for genome in next_generation:
            print('Genome:', genome.id, 'Species:', self.species_map[genome.id], 'Fitness:', genome.fitness)

        # Check if we're done.
        best_generations = sorted(next_generation, key=lambda x: x.fitness, reverse=True)

        if best_generations[0].fitness > self.threshold:
            return True, best_generations[0]

        # Fill up the rest of the population with crossovers.
        while len(next_generation) < self.pop_size:
            index = random.uniform(0, len(self.species))
            species = self.get_random_species()
            sorted_genomes = sorted(
                species.genomes, key=lambda x: x.fitness, reverse=True)
            # parentA = random.choice(species.genomes)
            # Let the cross over happen between the best genomes.
            parentA = self.get_random_genome(species)
            parentB = self.get_random_genome(species)
            while parentB == parentA:
                if len(species.genomes) < 2:
                    break
                parentB = self.get_random_genome(species)

            new_genome = parentA.cross(parentB)

            if random.random() < 0.8:
                new_genome.mutate()

            if random.random() < 0.05:
                # Make sure that existing connections have the same innovation numbers
                nc = new_genome.mutate_add_connection()
                # If mutation happened.
                if nc:
                    nc_key = (nc.in_node, nc.out_node)
                    if not mutated_connection_genes.get(nc_key):
                        mutated_connection_genes[nc_key] = nc.innovation
                    else:
                        nc.innovation = mutated_connection_genes[nc_key]

            if random.random() < 0.03:
                # Make sure that existing connections have the same innovation numbers
                nc_in, nc_out = new_genome.mutate_add_node()
                # If mutation happened.
                if nc_in and nc_out:
                    nc_in_key = (nc_in.in_node, nc_in.out_node)
                    if not mutated_connection_genes.get(nc_in_key):
                        mutated_connection_genes[nc_in_key] = nc_in.innovation
                    else:
                        nc_in.innovation = mutated_connection_genes[nc_in_key]

                    nc_out_key = (nc_out.in_node, nc_out.out_node)
                    if not mutated_connection_genes.get(nc_out_key):
                        mutated_connection_genes[nc_out_key] = nc_out.innovation
                    else:
                        nc_out.innovation = mutated_connection_genes[nc_out_key]

            next_generation.append(new_genome)

        for species in self.species:
            species.genomes = set()

        for genome in next_generation:
            found_species = False
            for species in self.species:
                N = max(len(genome.connection_genes), len(species.rep.connection_genes))
                if N < 20:
                    N = 1
                if genome.get_compatibility_distance(species.rep, C1, C2, C3, N) < DIS_THRES:
                    species.add_genome(genome)
                    self.species_map[genome.id] = species
                    found_species = True
                    break

            if not found_species:
                species = Species(genome)
                self.species.add(species)
                self.species_map[genome.id] = species

        self.genomes = next_generation[:]
        return False, best_generations[0]

    def get_random_species(self):
        index = int(random.uniform(0, len(self.species)-1))
        return list(self.species)[int(round(index))]
        # total_weight = 0.0
        # for species in self.species:
        #     total_weight += species.adj_fitness

        # threshold = random.random() * total_weight
        # meter = 0.0
        # for species in self.species:
        #     meter += species.adj_fitness
        #     if meter >= threshold:
        #         return species

    def get_random_genome(self, species):
        genomes = species.genomes
        indx = random.uniform(0, len(genomes)-1)
        return list(genomes)[int(round(indx))]
        # total_weight = 0.0
        # for genome in genomes:
        #     total_weight += genome.fitness

        # threshold = random.random() * total_weight
        # meter = 0.0
        # for genome in genomes:
        #     meter += genome.fitness
        #     if meter >= threshold:
        #         return genome
