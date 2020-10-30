import retro
from runRightAgent import runRightAgent

def main():
    env = retro.make(game='SonicTheHedgehog2-Genesis')
    obs = env.reset()
    agent = runRightAgent()
    # [NA, Jump, NA, NA, Up, Down, Left, Right, Jump, NA, NA, NA]
    while True:
        obs, rew, done, info = env.step(agent.getAction())
        env.render()
        if done:
            obs = env.reset()
    env.close()

if __name__ == "__main__":
    main()
