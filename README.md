# Auto Parking using DQN with [Webots](https://www.cyberbotics.com/) & [Airsim](https://microsoft.github.io/AirSim/) simulator

This is a simple implementation of auto-parking using **reinforcement learning** methods with GPS and Lidar sensors.

We have deployed our model on **2 different environments** to validate its superiority.

## Webots Environment

See this method in [Webots ](https://github.com/Huang-Shijie-SDUWH/Reinforcement_Learning_Auto_Parking/tree/master/Webots) directory

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

> And we add some special reward when something bad happened such as collision and drive out of our bounded area or total time out

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

There are possibilities using CNN and a backward camera on the car to train a more robust model, but because the limited time we didn't try that, but we can tell that it can be easily performed by just setting the DQN policy to `"CNNpolicy"` 

> This code is modified from [AirSim/PythonClient/reinforcement_learning at main · microsoft/AirSim](https://github.com/Microsoft/AirSim/tree/main/PythonClient/reinforcement_learning)

## Real World Deployment

![image-20220808184519145](https://s2.loli.net/2022/08/08/gdAkiKp8xYNf1zU.png)

Under Developing
