# 引数で学習と実行を分岐？
# for learning

import json
import sys
from . import qtable_model2
import time
import numpy as np

#TODO : 一旦はグローバル変数で宣言するが、ゆくゆくはパラメタで受け取る
robo = "TB3RoboModel"
num_states = 2 #TODO:正しく設定
actions = 5 #TODO;正しく設定
episode_limit = 100

#subscribe total_reward

if episode < episode_limit and total_time < total_time_limit:
    total_time = 0  #subscrive instead
    state = 0 #subscrive instead
    total_reward = 0 #subscrive instead 
    #TODO:subscribe:state
    action = model.get_action(state)
    next_state, reward, done, _ = env.step(action) #なにこれ？
    total_reward = total_reward + reward
    #print("state=" + str(state))
    #print("reward=" + str(reward))
    #print("action=" + str(action))
    #print("done=" + str(done))
    #print("total_time=" + str(total_time))

    #実行結果をもとに学習
    model.learn(state, action, reward, next_state)

    #TODO:publish action
    #subscribe episode
    #publish total_reward
    #subscribe total_time
    env.reset()
    model.save('./dev/ai/qtable_model.csv')
    print("episode=" + str(episode) + " total_time=" + str(total_time) + " total_reward=" + str(total_reward))

else:
    done = False
    print("END")
    env.reset()
    sys.exit(0)