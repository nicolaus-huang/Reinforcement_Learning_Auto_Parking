import numpy as np
import airsim

import gym
from gym import spaces
import math

class AirSimEnv(gym.Env):
    metadata = {"render.modes": ["rgb_array"]}

    def __init__(self):
        self.observation_space = spaces.Dict({
            'position': spaces.Box(low=-30, high=30, shape=(2,), dtype=np.float32),
            'orientation': spaces.Box(low=-math.pi, high=math.pi, shape=(1,), dtype=np.float32)
        })
        self.viewer = None

    def __del__(self):
        raise NotImplementedError()

    def _get_obs(self):
        raise NotImplementedError()

    def _compute_reward(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def step(self, action):
        raise NotImplementedError()

    def render(self):
        return self._get_obs()
