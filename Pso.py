import numpy as np
import os
import csv

class PSO:
    def __init__(self, d, size, c1, c2):      
        self.d = d
        self.size = size
        self.c1 = c1
        self.c2 = c2

    def initialization(self, objective_function, n_iterations, xMax, xMin, decimal):
        self.w = np.linspace(0.9, 0.4, n_iterations) 
        self.xMax = np.array(xMax)
        self.xMin = np.array(xMin)
        self.decimal = decimal
        self.vMin = -0.2 * (self.xMax - self.xMin)
        self.vMax = 0.2 * (self.xMax - self.xMin)
        
        self.position = np.random.uniform(self.xMin, self.xMax, (self.size, self.d))
        self.velocity = np.random.uniform(self.vMin, self.vMax, (self.size, self.d))
        
        for dim in range(self.d):
            self.position[:, dim] = np.round(self.position[:, dim], decimals=self.decimal[dim])
            self.velocity[:, dim] = np.round(self.velocity[:, dim], decimals=self.decimal[dim])
        
        self.score = np.apply_along_axis(objective_function, 1, self.position)
        
        self.local_best = np.copy(self.position)
        self.local_best_score = np.copy(self.score)
        idx = np.argmin(self.local_best_score)
        self.global_best = self.local_best[idx]
        self.global_best_score = self.local_best_score[idx]

    def direction_improvement(self, iteration, objective_function):
        r1 = np.random.rand(self.size, self.d)
        r2 = np.random.rand(self.size, self.d)
        w = self.w[iteration]
        self.velocity = (w * self.velocity
                         + self.c1 * r1 * (self.local_best - self.position)
                         + self.c2 * r2 * (self.global_best - self.position))
        self.velocity = np.clip(self.velocity, self.vMin, self.vMax)
        for dim in range(self.d):
            self.velocity[:, dim] = np.round(self.velocity[:, dim], decimals=self.decimal[dim])
        
        self.position += self.velocity
        self.position = np.clip(self.position, self.xMin, self.xMax)
        for dim in range(self.d):
            self.position[:, dim] = np.round(self.position[:, dim], decimals=self.decimal[dim])
            
        self.score = np.apply_along_axis(objective_function, 1, self.position)
        
        improved = self.score < self.local_best_score
        self.local_best[improved] = self.position[improved]
        self.local_best_score[improved] = self.score[improved]
        
        idx = np.argmin(self.local_best_score)
        if self.local_best_score[idx] < self.global_best_score:
            self.global_best = self.local_best[idx]
            self.global_best_score = self.local_best_score[idx]


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

def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, csvfile_name, wbpath, data_label):
    csvfile_name += '.csv'
    wbpath += '.csv'
    model.initialization(objective_function, n_iterations, xMax, xMin, decimal)
    current_score = model.global_best_score
    early_stop_counter = 0

    for i in range(n_iterations):
        model.direction_improvement(i, objective_function)

        if model.global_best_score < current_score:
            current_score = model.global_best_score
            early_stop_counter = 0
        else:
            early_stop_counter += 1
            if early_stop_counter >= 10:
                print("Early stopping triggered.")
                break
        
        Record(i+1, model.global_best, model.global_best_score, csvfile_name, wbpath, data_label)
        print('-----------------------------------------')
        print(f'Iteration: {i+1}')
        print(f'Current best score: {model.global_best_score}')
        print(f'Current best parameters: {model.global_best}')

    print('-----------------------------------------') 
    print('PSO ended!')
    print('Best parameters:', model.global_best)
    print('Best score:', model.global_best_score)   
    return model.global_best_score, model.global_best