#!/bin/bash

source install/setup.bash
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib
if [ $# -ne 1 -a $# -ne 2 -a $# -ne 3 ]
then
	echo "Usage: $0 <pkgname> [args]"
	exit 1
fi

#run ros2_operation
ros2 run ${1}_op ${1}_op_node ${2} ${3}

#run ros2 learning
#ros2 run q_table_py qtable_node_py
#ros2 run ${1} ${1}_node ${2} ${3} 
