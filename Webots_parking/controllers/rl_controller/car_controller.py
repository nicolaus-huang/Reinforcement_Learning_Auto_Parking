"""car_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, TouchSensor, Emitter,Supervisor
import struct
import numpy as np

# Enter here exit cleanup code.
class Car(Supervisor):
    def __init__(self):
        super(Car, self).__init__()
        self.time_step = int(self.getBasicTimeStep())  # get the time step of the current world.
        self.touchsensor = []  # 碰撞传感器tag
        self.wheels = []  # 电机tag,通过此来获取对电机的控制
        self.self_node=self.getFromDef('PAT')
        self.so=[]
        self.node=self.getFromDef('PAT')
        self.translation_field = self.node.getField('translation')
        self.rotation_field=self.node.getField("rotation")
        wheels_names = ["front right wheel", "front left wheel", "back right wheel", "back left wheel"]  # 电机名称
        so_names=["so0","so1","so2","so3","so4","so5","so6","so7","so8","so9","so10","so11","so12","so13","so14","so15"]
        touchsensor_names = ["touchsensor1", "touchsensor2", "touchsensor3", "touchsensor4"]  # 碰撞传感器名称
        for i in range(4):#初始化电机(轮子)和touchsensor(检测碰撞)
            self.wheels.append(self.getDevice(wheels_names[i]))  # 获得tag,进而获得对电机的控制
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)
            self.touchsensor.append(self.getDevice(touchsensor_names[i]))
            self.touchsensor[i].enable(self.time_step)
        for i in range(16):#初始化声纳(距离传感器)
            self.so.append(self.getDevice(so_names[i]))
            self.so[i].enable(self.time_step)
        self.gps = self.getDevice("gps")
        self.gps.enable(self.time_step)
        # self.step(self.time_step)
        self.state="state"
        self.node.saveState(self.state)

    def get_angle(self):  # 获得rotation里面的angle,orientaion为四元数(停车成功时,angle应为1.57)
        orientation = self.rotation_field.getSFRotation()
        return np.array([orientation[3]])


    def get_so_value(self):#获得声纳传感器读数,注意0是没有障碍,越大离障碍越近
        distance=[]
        for i in range(16):
            distance.append(self.so[i].getValue())
        return np.array(distance)

    def go_backward(self):  # 前进
        leftSpeed = -1.0
        rightSpeed = -1.0
        self.wheels[0].setVelocity(leftSpeed)
        self.wheels[1].setVelocity(rightSpeed)
        self.wheels[2].setVelocity(leftSpeed)
        self.wheels[3].setVelocity(rightSpeed)
        self.step(3000)  # 让机器人在上面设置的参数里运行这么长时间



    def turn(self):  # 转向
        leftSpeed = -1.0
        rightSpeed = 1.0
        self.wheels[0].setVelocity(rightSpeed)
        self.wheels[1].setVelocity(leftSpeed)
        self.wheels[2].setVelocity(rightSpeed)
        self.wheels[3].setVelocity(leftSpeed)
        self.step(4214)  # 让机器人在上面设置的参数里运行这么长时间,转九十度


    def get_position(self):  # 获得当前位置
        '''

        :return: [x,y,z],成功时x为0.8,y为0.2
        '''
        return np.array(self.gps.getValues()[0:2])



    def detect_collision(self):  # 返回大于0则碰撞
        touchvalue = 0
        for i in range(4):
            touchvalue = touchvalue + self.touchsensor[i].getValue()
        return touchvalue


    def reset(self):  # 回到起始位置和起始方向
        # orginalPosition = [4, -2, 0]
        originalRotation = [0, 0, 1, 3.14]  # 初始旋转四元素,停车成功时最后一个应为1.57,其余在运行时基本不变(会变一点,误差原因)
        # self.translation_field.setSFVec3f(orginalPosition)
        # self.rotation_field.setSFRotation(originalRotation)  #这么设置试验次数多就小车就离体了
        self.node.loadState(self.state)
        for i in range(4):#反正得这么设置一下，要不报错
            self.wheels[i].setPosition(float('inf'))
            self.wheels[i].setVelocity(0.0)
        self.rotation_field.setSFRotation(originalRotation)
        self.step(self.time_step)#应该运行一下这个。。。不然雷达数据有问题
        # self.node.restartController()

    def test(self):
        while 1:
            self.go_backward()
            self.turn()

    def get_observation(self):
        # self.step(self.time_step)
        obs_dict={
            "position":self.get_position(),
            "sensor":self.get_so_value(),
            "orientation":self.get_angle()
        }
        return obs_dict
#
# car=Car()
# car.go_forward()
# print(car.get_observation())
# car.turn_right()
# print("right1",car.get_observation())
# car.turn_right()
# print("right2",car.get_observation())
