import csv
import os
import numpy as np

class Qagent:
    #Q 学習機本体
    def __init__(self, alpha, gamma, initial_q=10.0):
        #Q 値、学習係数、伝播係数の設定
        self._values = {}
        self._alpha = alpha
        self._gamma = gamma
        self._initial_q = initial_q
        self.score_list = [20., 5., 5., -5., -5.]
        csv_path = os.getcwd() + "/qmodel.csv"
        
        if not os.path.isfile(csv_path):
            with open(csv_path, 'w') as f:
                f.write('')
        self.modelcsv = "./qmodel.csv"

        # with open(self.modelcsv, 'r') as f:
        #     reader = csv.reader(f)
        #     l = [row for row in reader]

        # print(l)

    def model_reset(self):
         with open(self.modelcsv, 'w') as f:
                f.write('')


    def dis2state(self, distance_array):
        state = ""
        state_size = 2
        dis_ind_list = [0 for i in range(state_size)]
        area_size = len(distance_array) // state_size
        for i in range(state_size):
            dis_mean = np.mean(distance_array[area_size * i:area_size * (i+1)])
            dis_min = min(distance_array[area_size * i:area_size * (i+1)])
            if dis_min < 0.03:
                #collision
                dis_ind_list[i] = 1
            else:
                if dis_mean < 0.1:
                    dis_ind_list[i]  = 2
                elif dis_mean < 0.2:
                    dis_ind_list[i]  = 3
                elif dis_mean < 0.3:
                    dis_ind_list[i]  = 4
                else:
                    dis_ind_list[i]  = 5      
        state_str = "".join(list(map(str, dis_ind_list)))
        state = int(state_str)
        return state

    def select_q(self, state, act):
        #状態とアクションをキーに、q 値取得
        if ((state, act) in self._values.keys()):
            #print("happy")
            return self._values[(state, act)]
        else:
            # Q 値が未学習の状況なら、Q 初期値
            # print(self._values.keys())
            self._values[(state, act)] = self._initial_q
            return self._initial_q

    def save(self):
        with open(self.modelcsv, 'w') as f:
            writer = csv.DictWriter(f, self._values.keys())
            writer.writeheader()
            writer.writerow(self._values)
            
    def load(self):
        with open(self.modelcsv) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key, value in row.items():
                    tpl_key = eval(key)
                    self._values[tpl_key] = float(value)
        # for key, value in self._values.items():
        #     print(type(value))


    def set(self, state, act, q_value):
        #Q 値設定
        self._values[(state, act)] = q_value

    def learning(self, state, act, max_q):
        #Q 値更新
        pQ = self.select_q(state, act)
        new_q = pQ + self._alpha * (self.score_list[act] + self._gamma * max_q - pQ)
        #print(new_q - pQ)
        self.set(state, act, new_q)

    def add_fee(self, state, act, fee):
        #報酬を与える
        pQ = self.select_q(state, act)
        new_q = pQ + self._alpha * (fee - pQ)
        self.set(state, act, new_q)