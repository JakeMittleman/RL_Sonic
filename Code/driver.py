import neural_network
import retro
from evaluation import Evaluator
from PIL import Image, ImageDraw
import cv2
import numpy as np
import os

POPULATION_SIZE = 150


def main():
    env = retro.make(game='SonicTheHedgehog2-Genesis', record='../output/recordings')
    recording_iteration = -2
    population = []
    evaluator = Evaluator(POPULATION_SIZE)

    for i in range(POPULATION_SIZE):
        population.append(neural_network.NeuralNetwork.create(
            70, 12))

    for nn in population:
        evaluator.genomes.append(nn.genome)

    isNotDone = True
    generation = 0

    inx, iny, inc = env.observation_space.shape

    inx = int(inx/32)
    iny = int(iny/32)

    level_map = Image.open("../level_map.png").convert("RGB")

    max_fitness = 0

    # 300 x 100
    # 36 x 24
    # 300 / 36 = 36

    next_delete = False


    while isNotDone:
        print('\n------------\nGeneration: %d\n-----------' % generation)
        for nn in population:
            draw = ImageDraw.Draw(level_map)
            delete = next_delete
            # do sonic shit
            runRew = 0
            obs = env.reset()
            env.render()
            # [NA, Jump, NA, NA, Up, Down, Left, Right, Jump, NA, NA, NA]
            done = False
            frames = 0
            info = {'x': 96, 'y': 656}
            draw.line((info['x'], info['y'], info['x'], info['y']), fill=(255, 0, 0), width=5)
            last_x = 96
            last_y = 656
            stopped_x = 96
            stuck_x = 96
            score_mul = 1
            while not done:

                obs = cv2.resize(obs, (inx, iny))
                obs = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
                obs = np.reshape(obs, (inx,iny))

                # inputs = []
                # for i in range(len(obs)//2-5, len(obs)//2+5):
                #     for j in range(len(obs[0])//2-5, len(obs[0])//2+5):
                #         inputs.append(obs[i][j])

                inputsfromnn = nn.activate(list(np.ndarray.flatten(obs)))
                # inputsfromnn = nn.activate([info['x'], info['y']])
                # inputsfromnn = nn.activate([info['x']])
                obs, rew, done, info = env.step(inputsfromnn)
                draw.line((last_x, last_y, info['x'], info['y']), fill=(255, 0, 0), width=5)
                if frames == 0:
                    start_x = info['x']

                frames += 1
                # runRew += rew
                env.render()
                runRew = 0

                if frames % 300 == 0:
                    if stopped_x == info['x']:
                        done = True
                    else:
                        stopped_x = info['x']

                last_x = info['x']
                last_y = info['y']

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
                    nn.genome.fitness = runRew * score_mul + info['rings'] * 5 - (frames / 60)
                    if nn.genome.fitness > max_fitness:
                        max_fitness = nn.genome.fitness
                        level_map.save("../output/maps/level_map_%d-%d.png" % (int(max_fitness), recording_iteration), "PNG")
                        next_delete = False
                    else:
                        level_map = Image.open("../level_map.png").convert("RGB")
                        next_delete = True

                    recording_iteration += 1

                    runRew = 0

                    if delete:
                        number = "0" * (6 - len(str(recording_iteration))) + str(recording_iteration)
                        path = "../output/recordings/SonicTheHedgehog2-Genesis-EmeraldHillZone.Act1-%s.bk2" % number
                        if os.path.exists(path):
                            os.remove(path)

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