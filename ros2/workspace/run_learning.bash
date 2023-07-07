#!/bin/bash

source install/setup.bash
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib
#run ros2 learning
ros2 run qtable_py qtable_node_py
#ros2 run ${1} ${1}_node ${2} ${3} 
