from config import Config
from action import Action
import math


class Agent:
    def __init__(self, k, p, config: Config, reaction_strategy='blind'):
        self.k = math.floor(k)
        self.p = math.floor(p)

        self.config = config
        self.score = 0
        self.steps_after_plan = 0
        self.position = [0, 0]
        self.action_to_do = []
        self.target = None
        self.last_holes = None

        # self.seed = seed
        self.reaction_strategy = reaction_strategy

    def get_action(self, env):
        if self.steps_after_plan % (self.k + self.p) == 0 or len(self.action_to_do) == 0:
            self.plan(env)

        if self.reaction_strategy != 'blind' and self.target and self.target not in env.holes:
            if self.reaction_strategy == 'disappear':
                self.plan(env)
            elif self.reaction_strategy == 'any_appear':
                for hole in env.holes:
                    if hole not in self.last_holes:
                        self.plan(env)
                        break
            elif self.reaction_strategy == 'near_appear':
                for hole in env.holes:
                    if hole not in self.last_holes and \
                            abs(hole[0] - self.position[0]) + abs(hole[1] - self.position[1]) < \
                            abs(self.target[0] - self.position[0]) + abs(self.target[1] - self.position[1]):
                        self.plan(env)
                        break
        else:
            if self.steps_after_plan < self.p:
                self.steps_after_plan += 1
                return Action.STOP
            elif self.steps_after_plan < self.p + self.k:
                if len(self.action_to_do) > 0:
                    self.steps_after_plan += 1
                    return self.action_to_do.pop(0)
                else:
                    return Action.STOP
            else:
                return Action.STOP
        return Action.STOP

    def plan(self, env):
        self.steps_after_plan = 0
        self.action_to_do = []
        self.last_holes = env.holes.copy()

        target_hole = self.plan_selection(env)
        if target_hole:
            self.target = target_hole.position
            target_x, target_y = target_hole.position
            agent_x, agent_y = self.position
            if agent_x >= target_x:
                self.action_to_do.extend([Action.LEFT] * (agent_x - target_x))
            else:
                self.action_to_do.extend([Action.RIGHT] * (target_x - agent_x))

            if agent_y >= target_y:
                self.action_to_do.extend([Action.UP] * (agent_y - target_y))
            else:
                self.action_to_do.extend([Action.DOWN] * (target_y - agent_y))

    def plan_selection(self, env):
        max_score = 0
        max_hole = None
        for key in env.holes:
            hole = env.holes[key]
            hole_score = self.utility(hole)
            if hole_score > max_score:
                max_score = hole_score
                max_hole = hole
        return max_hole

    def utility(self, hole):
        distance = abs(self.position[0] - hole.position[0]) + abs(self.position[1] - hole.position[1])
        score = hole.score
        age = hole.age
        return self.config.u_dis * distance + self.config.u_score * score + self.config.u_age * age

    def get_effectiveness(self, env):
        if env.history_total_score == 0:
            return 0
        return self.score / env.history_total_score
