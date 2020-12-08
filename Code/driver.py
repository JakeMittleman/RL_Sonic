import neural_network
import retro
from innovation_tracker import InnovationTracker
from evaluation import Evaluator
import random
import cv2
import numpy as np

POPULATION_SIZE = 20

def main():
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    population = []
    evaluator = Evaluator(POPULATION_SIZE)

    for i in range(POPULATION_SIZE):
        population.append(neural_network.NeuralNetwork.create(
            100, 12))

    for nn in population:
        evaluator.genomes.append(nn.genome)

    isNotDone = True
    generation = 0

    inx, iny, inc = env.observation_space.shape

    inx = int(inx/8)
    iny = int(iny/8)


    while isNotDone:
        print('Generation:', generation)
        for nn in population:
            # do sonic shit
            runRew = 0
            obs = env.reset()
            env.render()
            # [NA, Jump, NA, NA, Up, Down, Left, Right, Jump, NA, NA, NA]
            done = False
            frames = 0
            info = {'x': 96, 'y': 656}
            last_x = 96
            stuck_x = 96
            score_mul = 1
            while not done:

                obs = cv2.resize(obs, (inx, iny))
                obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
                obs = np.reshape(obs, (inx,iny))

                inputs = []
                for i in range(len(obs)//2-5, len(obs)//2+5):
                    for j in range(len(obs[0])//2-5, len(obs[0])//2+5):
                        inputs.append(obs[i][j])

                inputsfromnn = nn.activate(inputs)
                # inputsfromnn = nn.activate([info['x'], info['y']])
                # inputsfromnn = nn.activate([info['x']])
                obs, rew, done, info = env.step(inputsfromnn)
                if frames == 0:
                    start_x = info['x']

                frames += 1
                # runRew += rew
                env.render()
                runRew = 0

                if frames % 300 == 0:
                    if last_x == info['x']:
                        done = True
                    else:
                        last_x = info['x']

                if frames % 600 == 0:
                    if abs(stuck_x - info['x']) < 250:
                        # print(stuck_x, info['x'])
                        done = True
                        score_mul = 0.75
                    else:
                        stuck_x = info['x']

                if done:
                    runRew = info['x'] - 96
                    if info['level_end_bonus'] > 0:
                        runRew += 50000
                    nn.genome.fitness = runRew * score_mul
                    runRew = 0
                    obs = env.reset()

        finished_learning, best_genome = evaluator.evaluate()
        if finished_learning:
            print('Sonic beat the level!')
            print('It took', generation,
                  'generations! It achieved a fitness of', best_genome.fitness)
            # Save the playback.
            exit()
        population = []
        for genome in evaluator.genomes:
            population.append(neural_network.NeuralNetwork(genome))
        generation += 1


if __name__ == "__main__":
    main()
