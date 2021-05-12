from env import Tileworld
from config import Config
from agent import Agent
import random
import numpy as np
import matplotlib.pyplot as plt

config = Config()


def single_test(gamma, k, p, reaction):
    result = []
    for game in range(5):
        # seed = random.random()
        env = Tileworld(gamma, config)
        agent = Agent(k, p, config, reaction)
        for time_step in range(config.game_length):
            action = agent.get_action(env)
            env.advance(action, agent)
        result.append(agent.get_effectiveness(env))
    return result


def characterization(k, p, reaction='blind'):
    eff_list = []
    eff_low = []
    eff_high = []
    gamma_list = []
    lg10gamma_list = []
    for lg10gamma in np.linspace(0, 2, 15, endpoint=True):
        gamma = 10 ** lg10gamma

        lg10gamma_list.append(lg10gamma)
        gamma_list.append(gamma)

        eff = single_test(gamma, k, p, reaction)
        eff_list.append(np.mean(eff))
        eff_low.append(np.min(eff))
        eff_high.append(np.max(eff))

    return gamma_list, lg10gamma_list, eff_list, eff_low, eff_high


def exp1():
    gamma_list, lg10gamma_list, eff_list, eff_low, eff_high = characterization(10, 1)

    plt.plot(gamma_list, eff_list)
    plt.fill_between(gamma_list, eff_low, eff_high, alpha=0.2)
    plt.xlabel(r'$\gamma$')
    plt.ylabel(r'$\epsilon$')
    plt.title('Figure 1: Effect of Rate of World Change')
    plt.show()

    plt.plot(lg10gamma_list, eff_list)
    plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)
    plt.xlabel(r'$\log_{10}\gamma$')
    plt.ylabel(r'$\epsilon$')
    plt.title(r'Figure 2: Effect of Rate of World Change ($\log$ x-scale)')
    plt.show()


def exp2():
    for p in [0.5, 1, 2, 4]:
        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(2 * config.size, p)
        plt.plot(lg10gamma_list, eff_list, label='p=' + str(p))
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

    plt.legend()
    plt.xlabel(r'$\log_{10}\gamma$')
    plt.ylabel(r'$\epsilon$')
    plt.title(r'Figure 3: Effect of Planning Time (bold agent)')
    plt.show()

    for p in [0.5, 1, 2, 4]:
        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(1, p)
        plt.plot(lg10gamma_list, eff_list, label='p=' + str(p))
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

    plt.legend()
    plt.xlabel(r'$\log_{10}\gamma$')
    plt.ylabel(r'$\epsilon$')
    plt.title(r'Figure 4: Effect of Planning Time (cautious agent)')
    plt.show()


def exp3():
    i = 5
    p = 4
    k_list = [1, 4, 2 * config.size]
    labels = ['cautious', 'normal', 'bold']
    for p in [4, 2, 1]:
        for k, label in zip(k_list, labels):
            _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(k, p)
            plt.plot(lg10gamma_list, eff_list, label=label)
            plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

        plt.legend()
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.ylabel(r'$\epsilon$')
        plt.title('Figure %d: Effect of Degree of Boldness (p=%d)' % (i, p))
        plt.show()
        i += 1


def exp4():
    i = 8
    bold_k = 2 * config.size
    for p in [2, 1]:
        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(bold_k, p)
        plt.plot(lg10gamma_list, eff_list, label='blind commitment')
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(bold_k, p, 'disappear')
        plt.plot(lg10gamma_list, eff_list, label='target disappearance')
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(bold_k, p, 'any_appear')
        plt.plot(lg10gamma_list, eff_list, label='target dis. or near')
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(bold_k, p, 'near_appear')
        plt.plot(lg10gamma_list, eff_list, label='target dis. or any')
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)

        plt.legend()
        plt.xlabel(r'$\log_{10}\gamma$')
        plt.ylabel(r'$\epsilon$')
        plt.title('Figure %d: Effect of Reaction Strategy (p=%d)' % (i, p))
        plt.show()
        i += 1

    k_list = [1, 4, 2 * config.size]
    labels = ['cautious', 'normal', 'bold']
    for k, label in zip(k_list, labels):
        _, lg10gamma_list, eff_list, eff_low, eff_high = characterization(k, 1, 'disappear')
        plt.plot(lg10gamma_list, eff_list, label=label)
        plt.fill_between(lg10gamma_list, eff_low, eff_high, alpha=0.2)
    plt.legend()
    plt.xlabel(r'$\log_{10}\gamma$')
    plt.ylabel(r'$\epsilon$')
    plt.title('Figure 10: Effect of Degree of Boldness (reactive agent, p=1)')
    plt.show()


def main():
    # exp1()
    # exp2()
    # exp3()
    exp4()


main()
