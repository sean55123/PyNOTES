import os
import numpy as np
import csv

class SA:
    def __init__(self, T0, Tf, k, step, index, X_init):
        self.T0 = T0
        self.Tf = Tf
        self.k = k
        self.step = step
        self.index = index
        self.X_init = np.array(X_init)

    def preheating(self, objective_function):
        self.T = self.T0
        self.score = objective_function(self.X_init)

    def fit(self, decimal, xMax, xMin):
        self.X_next = np.empty(shape=len(self.X_init))
        for i in range(len(self.X_init)):
            if self.index[i] == 0:
                self.X_next[i] = np.round((self.X_init[i] + np.random.uniform(-1, 1) * self.step[i]), decimal[i])
            else:
                self.X_next[i] = np.round(self.X_init[i] + (2 * np.random.random() - 1) * self.step[i], decimal[i])

        self.X_next = np.clip(self.X_next, xMin, xMax)

def Record(n, params, score, name, wbpath, data_label):
    value = [n] + list(params) + [score]
    if os.path.isfile(wbpath):
        with open(name, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(value)
    else:
        with open(name, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_label)
            writer.writerow(value)

def optimize(n_iterations, xMax, xMin, decimal, objective_function, model, csvfile_name, wbpath, data_label):
    csvfile_name += '.csv'
    wbpath += '.csv'
    accept_count = 0
    current_run = 0
    early_stop = 0
    model.preheating(objective_function)
    while model.T > model.Tf:
        if early_stop == 1:
            break
        for i in range(n_iterations):
            model.fit(decimal, xMax, xMin)
            score = objective_function(model.X_next)
            
            if i != 0 and i%5 == 0:
                if model.score == score:
                    early_stop += 1
                if early_stop == 1:
                    break
            
            if score < model.score:
                model.score = score
                model.X_init = model.X_next.copy()
                accept_count += 1
            else:
                if np.random.random() < np.exp(-(score - model.score) / model.T):
                    model.score = score
                    model.X_init = model.X_next.copy()
                    accept_count += 1

            current_run += 1
            Record(current_run, model.X_init, model.score, csvfile_name, wbpath, data_label)

        if model.T == model.T0:
            print('Initial accept rate =', 100 * accept_count / n_iterations)
        print('-----------------------------------------')
        print('Current temperature :', model.T)
        print('Current best score :', model.score)
        print('Current best parameters :', model.X_init)
        
        model.T *= model.k
    
    print('-----------------------------------------')
    print('SA ended!')
    print('Best params:', model.X_init)
    print('Best score:', model.score)
    return model.score