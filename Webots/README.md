## Webots Environment

![car.jpg](https://s2.loli.net/2022/08/08/lhq6tCi5SfzdcNp.jpg)

> Python==3.8 stable-baselines3 pytorch ==1.12 stable-baselines3 == 1.6.0
>

configure python interpreter in 

![9SQ56K8N_~Z_4I72RL1Y4EW.png](https://s2.loli.net/2022/08/08/EOfteQJKZNPxIS9.png)

### observation

- position
- orientation
- distance_sensor_value

### reward

see function in `Webots/rl_controller.py  compute_reward`

### environments and action code

```
python Webots/car_controller.py
```



### train code

```
python Webots/rl_controller.py/rl_controller.py
```



### algorithm

DQN

### Result

![park_pose](https://s2.loli.net/2022/08/08/Xfh5UTtqwIomk3a.png)

![logs](https://s2.loli.net/2022/08/08/mUc8kNtgsLxKnoR.png)



