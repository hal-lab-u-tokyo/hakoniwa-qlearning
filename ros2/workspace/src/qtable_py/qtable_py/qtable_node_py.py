#!/usr/bin/python
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray, Int32

#install for multiple node executor
from rclpy.executors import SingleThreadedExecutor

import json
import sys
#from . import qtable_model2, qtable_learn_py
import time
import numpy as np
import os

from . import qagent

#print('abspath:     ', os.path.abspath(__file__))

#TODO : 一旦はグローバル変数で宣言するが、ゆくゆくはパラメタで受け取る
robo = "TB3RoboModel"
NUM_STATES = 36 #TODO:正しく設定
ACTION_NUM = 5 #TODO;正しく設定
#model.load('./model/qtable_model.csv')
dis_list = [10. for i in range(60)]
last_state = "00"
last_action = 0
stopped = False
stop_count = 0


class StateSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.sub = self.create_subscription(
            Float64MultiArray,
            'min_arr',
            self.listener_callback,
            10)
        self.sub # prevent unused variable warning
    def listener_callback(self, msg):
        global dis_list
        for i in range(60):
            dis_list[i] = msg.data[i]
        #print(state[0])


class ActionPublisher(Node):
    def __init__(self):
        super().__init__('action_publisher')
        self.publisher_ = self.create_publisher(Int32, 'cmd_dir', 1)

        #subscribe:state
        #self.sub = Node.create_subscription(Float64MultiArray, 'min_arr', self.listener_callback, qos_profile=custom_qos_profile)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        #about learning
        self.ALPHA = 0.1
        self.GAMMA = 0.9
        self.EPSILON = 0.2

    
    def best_action_learning(self):
        global last_action, last_state, stopped, stop_count

        if stopped:
            if stop_count == 0:
                stopped = False
                return 0
            else:
                stop_count -= 1
                return 100


        q =  qagent.Qagent(self.ALPHA, self.GAMMA)
        q.load()
        state = q.dis2state(dis_list)
        print(state)
        best_action = 0

        #collision -> add big minus fee
        if 1 in list(map(int, list(str(state)))):
            q.add_fee(last_state, last_action, -1000)
            best_action = 99
            stop_count += 1
            if stop_count > 6:
                stopped = True
        else:
            # search & learn best action
            q_best = 10.
            best_action = 0

            for i in range(ACTION_NUM):
                if q.select_q(state, i) > q_best:
                    best_action = i
                    q_best = q.select_q(state, i)
            
            q.learning(last_state, last_action, q_best)

            if np.random.rand() < self.EPSILON:
                best_action = np.random.randint(0, 5)

            last_state = q.dis2state(dis_list)
            last_action = best_action
        q.save()
        return best_action

    def timer_callback(self):
        best_action = self.best_action_learning()
        send_msg = Int32()
        #publish:action
        #action = model.get_action(state)

        # if np.mean(state[20:40]) < 0.3:
        #     send_msg.data = 3
        # else:
        #     send_msg.data = 0
        send_msg.data = best_action
        self.publisher_.publish(send_msg)
        self.get_logger().info('Publishing: "%d"' % send_msg.data)


def main(args=None):
    rclpy.init(args=args)
    exec = SingleThreadedExecutor()
    action_publisher = ActionPublisher()
    state_subscriber = StateSubscriber()
    exec.add_node(action_publisher)
    exec.add_node(state_subscriber)
    exec.spin()
    #rclpy.spin(action_publisher)
    #rclpy.spin(state_subscriber)
    exec.destroy_node()
    exec.shutdown()


if __name__ == '__main__':
    main()
