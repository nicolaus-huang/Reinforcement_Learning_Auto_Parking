import setup_path
import airsim
import numpy as np
import math
import time

import gym
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv

class AirSimCarEnv(AirSimEnv):
    def __init__(self, ip_address, image_shape):
        super().__init__(image_shape)

        self.image_shape = image_shape
        self.start_ts = 0

        self.state = {
            "position": np.zeros(3),
            "prev_position": np.zeros(3),
            "pose": None,
            "prev_pose": None,
            "collision": False,
        }

        self.car = airsim.CarClient(ip=ip_address)
        self.action_space = spaces.Discrete(6)

        self.image_request = airsim.ImageRequest(
            "0", airsim.ImageType.DepthPerspective, True, False
        )

        self.car_controls = airsim.CarControls()
        self.car_state = None


    def _setup_car(self):
        self.car.reset()
        self.car.enableApiControl(True)
        self.car.armDisarm(True)
        time.sleep(0.01)

        
        # self.action = 0
        # self.car_controls.throttle = 1
        # self.car_controls.is_manual_gear = False
        # self.car_controls.steering = 0
        # self.car.setCarControls(self.car_controls)
        # print("Go Forward")
        # time.sleep(4.2)   # let car drive a bit

    def __del__(self):
        self.car.reset()
        

        # self.action = 0
        # self.car_controls.throttle = 1
        # self.car_controls.is_manual_gear = False
        # self.car_controls.steering = 0
        # self.car.setCarControls(self.car_controls)
        # print("Go Forward")
        # time.sleep(4.2)   # let car drive a bit

    def _do_action(self, action):
        self.car_controls.brake = 0
        self.car_controls.throttle = -0.5
        self.car_controls.is_manual_gear = True
        self.car_controls.manual_gear = -1
        self.car_controls.steering = 0

        if action == 0:
            self.car_controls.throttle = 0
            self.car_controls.brake = 1
        elif action == 1:
            self.car_controls.steering = 0
        elif action == 2:
            self.car_controls.steering = 0.5
        elif action == 3:
            self.car_controls.steering = -0.5
        elif action == 4:
            self.car_controls.steering = 0.25
        else:
            self.car_controls.steering = -0.25

        self.car.setCarControls(self.car_controls)
        time.sleep(1)

    def transform_obs(self, response):
        img1d = np.array(response.image_data_float, dtype=np.float)
        img1d = 255 / np.maximum(np.ones(img1d.size), img1d)
        img2d = np.reshape(img1d, (response.height, response.width))

        from PIL import Image

        image = Image.fromarray(img2d)
        im_final = np.array(image.resize((84, 84)).convert("L"))

        return im_final.reshape([84, 84, 1])

    def _get_obs(self):
        responses = self.car.simGetImages([self.image_request])
        image = self.transform_obs(responses[0])

        self.car_state = self.car.getCarState()

        self.state["prev_pose"] = self.state["pose"]
        self.state["pose"] = self.car_state.kinematics_estimated
        self.state["collision"] = self.car.simGetCollisionInfo().has_collided

        return image

    def _compute_reward(self):
        MAX_SPEED = 0
        MIN_SPEED = -10
        # THRESH_DIST = 3.5
        BETA = 1
        ALPHA = 40
        # positon(11.262, -17.765, 0.251) orientation(0, 0, -1, 0)

        best_or = np.array([0, 0, -1, 0])
        best_pt = np.array([7.306, 11.489, 0.140])
        car_pt = self.state["pose"].position.to_numpy_array()
        car_or = self.state["pose"].orientation.to_numpy_array()
        # print(self.state["pose"])
        # print("orientation_distance", car_or-best_or, np.linalg.norm(car_or-best_or))\
        eula = airsim.to_eularian_angles(self.state["pose"].orientation)[2]
        # print(airsim.to_eularian_angles(self.state["pose"].orientation))
        reward = 0
        reward_dist = 0
        reward_orit = 0
        dist = 0
        reward_steering = 0
        # if car_pt[0] < -5 or car_pt[0] > 15 or car_pt[1] < -37 or car_pt[1] > 0:
        if car_pt[0] < -7 or car_pt[0] > 10 or car_pt[1] < -8 or car_pt[1] > 24:
            reward = -50
        else:
            dist = 0.05 * (car_pt[0]-best_pt[0]) * (car_pt[0]-best_pt[0]) + 0.04 * (car_pt[1]-best_pt[1]) * (car_pt[1]-best_pt[1])
            reward_dist = 2 * math.exp(- BETA * dist)
            reward_orit = 0.5 * math.exp(- ALPHA * min(math.pi - eula, math.pi + eula))
            reward_steering = - 0.05 * self.car_controls.steering * self.car_controls.steering

            reward = reward_dist + reward_orit + reward_steering

        done = 0
        if reward < -0.5:
            done = 1
        if self.state["collision"]:
            reward = reward - 50
            done = 1
        if done == 0 and np.linalg.norm(car_pt-best_pt) < 1 and (eula > 3 or eula < -3) and self.car_controls.brake == 1:
            self.car_controls.throttle = 0
            self.car_controls.brake = 1
            self.car.setCarControls(self.car_controls)
            time.sleep(3)
            done = 1
            reward = reward + 100
            print("Done!")
        # print(car_pt)
        print("speed",self.car_state.speed,"position",reward_dist,"orientation",reward_orit)
        print("reward",reward)
        return reward, done

    def step(self, action):
        self._do_action(action)
        obs = self._get_obs()
        reward, done = self._compute_reward()

        return obs, reward, done, self.state

    def reset(self):
        self._setup_car()
        self._do_action(1)
        
        return self._get_obs()
