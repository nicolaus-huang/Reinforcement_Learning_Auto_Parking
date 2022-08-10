# Auto Parking using DQN with [Webots](https://www.cyberbotics.com/) & [Airsim](https://microsoft.github.io/AirSim/) simulator

This is a simple implementation of auto-parking using **reinforcement learning** methods with GPS and Lidar sensors.

We have deployed our model on **2 different environments** to validate its superiority.

## Airsim Environment

### Quick Start

1. download the [Neighborhood4](https://github.com/Huang-Shijie-SDUWH/Reinforcement_Learning_Auto_Parking/releases/download/1.0/Neighborhood4.zip)  environment from the release ( modified from [swri-robotics/Neighborhood](https://github.com/swri-robotics/Neighborhood) )

2. unzip the environment

3. run the Unreal Engine generated .exe file in the environment package

4. clone this repository and cd into the Airsim directory then execute the evaluation by 

   ```shell
   python eval.py
   ```

> This environment is manually controllable, you can impress F10 to see the control panel

### Training

follow the instructions upon, train the model by

```
python dqn_car.py
```



### Methods

We train an agent by setting a reward function by

![image-20220808191559048](https://s2.loli.net/2022/08/08/lo46cOyn8LjbPUs.png)

where the rewards are calculated as follows respectively

![image-20220808191658029](https://s2.loli.net/2022/08/08/5NOvxcZRfakndIQ.png)

> Some of the functions are modified from [Train PPO Agent for Automatic Parking Valet - MATLAB & Simulink](https://www.mathworks.com/help/releases/R2020b/reinforcement-learning/ug/train-ppo-agent-for-automatic-parking-valet.html), and we added some special reward when something bad happened such as collision and drive out of our bounded area or total time out

The reward function can be viewed like this

![figure](https://s2.loli.net/2022/08/08/lGfXLVu6N3UdeFm.png)

We defined **11 kinds** of actions of our car, which can be illustrated mainly by the figure below

![car1](https://s2.loli.net/2022/08/08/f2X6hp8WJwzVRbc.png)

there a 10 directions each performs as an action, and we set a stop action which can raise the brake.

### Results

![pos](https://s2.loli.net/2022/08/08/BtMD3271esLaqCd.png)

![image-20220808190143412](https://s2.loli.net/2022/08/08/oibEIgYzO2vR6aV.png)

We finally made a stable auto-parking model after about 4000 episodes training, countless fails, 15 days figuring out problems and adjusting the hyper parameters using the **relative** distance and orientation.

### Extend

There are possibilities using CNN and a backward camera on the car to train a more robust model, but because the queite simple environment(thus CNN can not extract ample valid information) we didn't try that, but we can tell that it can be easily performed by just setting the DQN policy to `"CNNpolicy"` 

> This code is modified from [AirSim/PythonClient/reinforcement_learning at main · microsoft/AirSim](https://github.com/Microsoft/AirSim/tree/main/PythonClient/reinforcement_learning)


## Webots Environment
![car.jpg](https://s2.loli.net/2022/08/08/lhq6tCi5SfzdcNp.jpg)

> python==3.8
> gym==0.21.0
> numpy==1.22.3
> stable_baselines3==1.6.0
> torch==1.12.0

configure python interpreter in 

![9SQ56K8N_~Z_4I72RL1Y4EW.png](https://s2.loli.net/2022/08/08/EOfteQJKZNPxIS9.png)

### observation:

- position

- orientation

- distance_sensor_value


We can simply add any sensors including camera,lidar to the car. The observation we choose is based on the reality.

### reward:

see function in `.\Webots\controllers\rl_controller\rl_controller.py`  compute_reward

### environments and action code:

```
.\Webots\controllers\rl_controller\car_controller.py
```



### train code:

```
.\Webots\controllers\rl_controller\rl_controller.py
```



### algorithm:

DQN

### training_logs:

`.\Webots\controllers\rl_controller\训练记录`

### result:

![park_pose](https://s2.loli.net/2022/08/08/Xfh5UTtqwIomk3a.png)

![logs](https://s2.loli.net/2022/08/08/mUc8kNtgsLxKnoR.png)

## Real World Deployment

![image-20220808184519145](https://s2.loli.net/2022/08/08/gdAkiKp8xYNf1zU.png)

Under Developing
