import os
import gym
import robotics_gym
from robotics_gym.envs import specs
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import deque
from dl_learning.methods.q_learning import QLearning


if __name__ == "__main__":

    os.environ['ROBOT_INITIAL_POSE'] = "-x -3.00162 -y -7.99707 -z 0.000693 -R -0.000329 -P -0.020618 -Y 0.001136"
    specs.environment_specs.launchfile = 'turtlebot2_octa.launch'
    sns.set()
    scores = deque(maxlen=100)
    n_episodes = 1000
    env = gym.make('Turtlebot2LaserEnv-v0')

    actions = range(env.action_space.n)

    q_learning = QLearning(actions)

    cumulative_reward = np.array(range(n_episodes))
    steps_per_episode = np.array(range(n_episodes))

    for e in range(n_episodes):
        current_state = str(env.reset())
        done = False
        G = 0.0
        steps = 0

        while not done:
            env.render(mode='human')

            action = q_learning.get_action(current_state)
            obs, reward, done, info = env.step(action)
            next_state = str(obs)

            q_learning.learn(current_state, action, reward, next_state)

            current_state = next_state
            steps += 1
            G += reward

        cumulative_reward[e] = G
        steps_per_episode[e] = steps
        scores.append(steps)

        mean_score = np.mean(scores)
        if e % 100 == 0:
            print('[Episode {}] - Mean survival time over last 100 episodes was {} ticks.'.format(e, mean_score))

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(np.array(range(n_episodes)), steps_per_episode)
    ax1.set_ylabel('episode length')

    ax2 = fig.add_subplot(212)
    ax2.plot(np.array(range(n_episodes)), cumulative_reward)
    ax2.set_xlabel('episodes')
    ax2.set_ylabel('episode reward')

    plt.show()

    env.close()