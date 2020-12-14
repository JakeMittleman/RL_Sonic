import matplotlib.pyplot as pp

gen_scores = [0 for _ in range(141)]

with open("../gens/gens.txt") as file:
    line = file.readline()
    gen_index = 0
    max_fitness = float("-inf")
    while line:
        if "Generation" in line:
            split_line = line.split()
            gen_index = int(split_line[1])
            max_fitness = float("-inf")

        elif "Fitness" in line:
            split_line = line.split()
            fitness = split_line[-1]
            if float(fitness) > max_fitness:
                max_fitness = float(fitness)
                gen_scores[gen_index] = max_fitness

        line = file.readline()

pp.plot([i for i in range(len(gen_scores))], gen_scores)
pp.xlabel("generations")
pp.ylabel("fitness")
pp.savefig("../output/plots")


