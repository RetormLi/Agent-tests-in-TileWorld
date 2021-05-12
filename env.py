import random
from agent import Agent
from config import Config
from action import Action


class Hole:
    def __init__(self, gamma, config: Config, env):
        while True:
            x = random.randint(0, env.size - 1)
            y = random.randint(0, env.size - 1)
            if (x, y) not in env.holes:
                self.position = (x, y)
                break

        self.config = config
        # self.seed = seed
        self.life_expectancy = 0
        self.score = 0
        self.age = 0
        self.init_random_parameter(gamma)

    def init_random_parameter(self, gamma):
        # taken from random distribution
        # random.seed(self.seed)
        self.life_expectancy = random.uniform(self.config.l_min / gamma,
                                              self.config.l_max / gamma)
        self.score = random.uniform(self.config.score_min, self.config.score_max)

    def get_position(self):
        return self.position


class Tileworld:
    def __init__(self, gamma, config: Config):
        self.gamma = gamma
        self.size = config.size
        self.config = config
        # self.seed = seed
        self.holes = dict()
        self.obstacles = None
        self.time_after_gen_hole = 0
        self.gestation_period = 0
        self.history_total_score = 0
        self.gen_hole()

    def advance(self, action, agent: Agent):
        self.interact(action, agent)
        new_position = tuple(agent.position)
        if new_position in self.holes.copy():
            hole_to_fill = self.holes[new_position]
            agent.score += hole_to_fill.score
            self.holes.pop(new_position)
            self.gen_hole()
        self.time_check()

    def interact(self, action, agent: Agent):
        if action == Action.UP:
            agent.position[1] = max(agent.position[1] - 1, 0)
        if action == Action.DOWN:
            agent.position[1] = min(agent.position[1] + 1, self.size - 1)
        if action == Action.LEFT:
            agent.position[0] = max(agent.position[0] - 1, 0)
        if action == Action.RIGHT:
            agent.position[0] = min(agent.position[0] + 1, self.size - 1)

    def time_check(self):
        for key in self.holes.copy():
            hole = self.holes[key]
            hole.age += 1
            if hole.age >= hole.life_expectancy:
                self.holes.pop(key)

        self.time_after_gen_hole += 1
        if self.time_after_gen_hole >= self.gestation_period:
            self.gen_hole()

    def gen_hole(self):
        new_hole = Hole(self.gamma, self.config, self)
        new_position = new_hole.get_position()
        self.holes[new_position] = new_hole
        # random.seed(self.seed)
        self.gestation_period = random.uniform(self.config.g_min / self.gamma,
                                               self.config.g_max / self.gamma)
        self.time_after_gen_hole = 0
        self.history_total_score += new_hole.score

    def get_holes(self):
        return self.holes
