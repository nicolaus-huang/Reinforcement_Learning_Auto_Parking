import gym
from gym import spaces
from car_controller import Car
import numpy as np
from stable_baselines3.common.env_checker import check_env
import math
from stable_baselines3 import DQN

class AutoParkEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(AutoParkEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(2)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Dict({
            'position':spaces.Box(low=np.array([-1.0, -3.0]), high=np.array([5.0, 2.0]),dtype=np.float64),
            'sensor':spaces.Box(low=0.0,high=1024.0,shape=(16,),dtype=np.float64),
            'orientation':spaces.Box(low=-0.5,high=4.0,shape=(1,),dtype=np.float64)
        })
        self.car=Car()
        self.gobackward=0
        self.turn=1
    def compute_reward(self,observation,collision):
        position=observation["position"]
        orientation=observation["orientation"]
        x=position[0]
        y=position[1]
        angle=orientation[0]
        done=0
        reward=0
        if x >= -2.5 and x <= 0.4 and angle<0:   #提前转向进不去
            reward=-100*(0.4-x)#他以为这样好 x=0.4是为0,之前为负数
            done=1
        elif x >= -2.5 and x <= 1.6 and angle>2: #正确前进
            reward=100*(1-x)
            done=0
        elif x >= 0.6 and x <= 1.6 and y<-0.5 and (angle>-1.6 and angle<-1.4):  #该转向时转向还没成功停进去0.4就能停但它非得提前转
            reward=300*(x-0.4)*(1.6-x)
            done=0
        # elif x >= 0.4 and x <= 1.6 and y<-0.5 and (angle>2):  #该转向时不转向
        #     reward=10*(1-x)
        #     done=0
        elif  x >= 0.4 and x <= 1.6 and (angle>-1):#转向两次没法停
            reward=-30
            done=1
        elif x>=0.4 and x<=1.6 and y>=-0.5 and y<=0.5  and (angle>-1.6 and angle<-1.4):#停车成功
            print("停车成功")
            reward=300
            done=1
        elif x>=1.6:#越界
            reward=-60
            done=1
        elif collision:#碰撞
            reward=-50
            done=1
        else:#还能停车,再往前就不行
            print("不连续点")
        return reward,bool(done)
    def step(self, action):
        if action==self.gobackward:
            self.car.go_backward()
        else:
            self.car.turn()
        observation=self.car.get_observation()
        collision=self.car.detect_collision()
        reward,done=self.compute_reward(observation,collision)
        info={}
        return observation, reward, done, info
    def reset(self):
        self.car.reset()
        return self.car.get_observation()

    def render(self, mode='human'):
        ...
    def close (self):
        ...

env =AutoParkEnv()
model = DQN.load("train_model_distance_sensor_300000.zip")
# model = DQN("MultiInputPolicy", env, verbose=1,tensorboard_log="./log",learning_starts=50000)
# model.learn(total_timesteps=500000, log_interval=4)#学习
# model.save("auto5")

obs = env.reset()
# model.save("auto4")
# model.learn(total_timesteps=100000, log_interval=4)#学习

while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    print("obs","reward","done",obs,reward,done)
    env.render()
    if done:
      obs = env.reset()
