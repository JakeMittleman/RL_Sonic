import neural_network
import retro
from innovation_tracker import InnovationTracker
from evaluation import Evaluator
import random

POPULATION_SIZE = 10

def main():
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    population = []
    innovation_tracker = InnovationTracker()
    evaluator = Evaluator(POPULATION_SIZE)

    for i in range(POPULATION_SIZE):
        population.append(neural_network.NeuralNetwork.create(1120, 12, innovation_tracker))

    for nn in population:
        # do sonic shit
        obs = env.reset()
        env.render()
        # [NA, Jump, NA, NA, Up, Down, Left, Right, Jump, NA, NA, NA]
        done = False
        while not done:
            obs, rew, done, info = env.step(nn.activate([random.random() for _ in range(1120)]))
            print(info)
            nn.genome.fitness += rew
            if done:
                obs = env.reset()
        env.close()


if __name__ == "__main__":
    main()