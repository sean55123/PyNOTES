import numpy as np
import os
import csv


class PSO:
    def __init__(self, d, size, c1, c2):      
        self.d = d
        self.size = size
        self.c1, self.c2 = c1, c2


    def initialization(self, objective_function, n_iterations, xMax, xMin, decimal):
        self.w = 0.9 - ((0.9-0.4)/n_iterations)*np.linspace(0, n_iterations, n_iterations)
        self.xMax, self.xMin = xMax, xMin
        self.vMin = list(map(lambda x, y: -0.2*(x-y), self.xMax, self.xMin))
        self.vMax = list(map(lambda x, y: 0.2*(x-y), self.xMax, self.xMin))
        self.decimal = decimal
        self.position = np.array(list(map(lambda x, y, z: np.round(np.random.uniform(x, y, [self.size, self.d]), z), self.xMin, self.xMax, self.decimal))).transpose()
        self.velocity = np.array(list(map(lambda x, y, z: np.round(np.random.uniform(x, y, [self.size, self.d]), z), self.vMin, self.vMax, self.decimal))).transpose()
        self.fit(objective_function)
        self.local_best = np.copy(self.position)
        self.local_best_score = np.copy(self.score).reshape(self.d, self.size)
        self.index = (lambda x: [x//self.size, x%self.size])(np.argmin(self.local_best_score))
        self.global_best = self.local_best[self.index[0]][self.index[1]]
        self.global_best_score = self.local_best_score[self.index[0]][self.index[1]]

    def fit(self, objective_function):
        self.score = []
        for i in range(self.d):
            self.score.append([])
            for j in range(self.size):
                self.score[i].append(objective_function(self.position[i][j]))


    def direction_improvement(self, current_iteration, objective_function):
        for j in range(self.d):
            for k in range(self.size):
                self.velocity[j][k] = (self.w[current_iteration]*self.velocity[j][k]
                                        +self.c1*np.random.rand(len(self.position[j][k]))*(self.local_best[j][k] - self.position[j][k])
                                        +self.c2*np.random.rand(len(self.position[j][k]))*(self.global_best - self.position[j][k]))
                self.velocity[j][k] = np.clip(self.velocity[j][k], self.vMin, self.vMax)
                self.velocity[j][k] = np.array(list(map(lambda x, y: np.round(x, y), self.velocity[j][k], self.decimal)))
                self.position[j][k] = self.position[j][k] + self.velocity[j][k]
                self.position[j][k] = np.clip(self.position[j][k], self.xMin, self.xMax)
                self.position[j][k] = np.array(list(map(lambda x, y: np.round(x, y), self.position[j][k], self.decimal)))
        
        self.fit(objective_function)

        for j in range(self.d):
            for k in range(self.size):
                if self.score[j][k] < self.local_best_score[j][k]:
                    self.local_best[j][k] = self.position[j][k]
                    self.local_best_score[j][k] = self.score[j][k]
                    if self.local_best_score[j][k] < self.global_best_score:
                        self.global_best = self.local_best[j][k]
                        self.global_best_score = self.local_best_score[j][k]
        

def Record(n, params, score, name, wbpath, data_label):
    value = [n] + list(params) + [score]
    if os.path.isfile(wbpath):
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(value)
    else:
        with open(name, 'a+', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_label)
            writer.writerow(value)


def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, name, wbpath, data_label):
    model.initialization(objective_function, n_iterations, xMax, xMin, decimal)
    current_score = model.global_best_score
    early_stop = 0
    for i in range(n_iterations):
        if i != 0 and i % 5 == 0:
            if current_score == model.global_best_score:
                early_stop += 1
            else:
                current_score = model.global_best_score
            if early_stop == 1:
                break
                
        model.direction_improvement(i, objective_function)
        Record(i+1, model.global_best, model.global_best_score, name, wbpath, data_label)
        print('-----------------------------------------')
        print('Current run :', i+1)
        print('Current best score :', model.global_best_score)
        print('Current best parameters :', model.global_best)

    print('-----------------------------------------') 
    print('PSO ended!')
    print('Best params:', model.global_best)
    print('Best score:', model.global_best_score)   