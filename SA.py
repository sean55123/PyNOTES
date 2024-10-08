import numpy as np
import os
import csv

class SA:
    def __init__(self, T0, Tf, k, step, index, X_init):
        self.T0 = T0
        self.Tf = Tf
        self.k = k
        self.step = np.array(step)
        self.index = np.array(index)
        self.X_init = np.array(X_init)

    def preheating(self, objective_function):
        self.T = self.T0
        self.score = objective_function(self.X_init)

    def fit(self, decimal, xMax, xMin):
        xMax = np.array(xMax)
        xMin = np.array(xMin)
        decimal = np.array(decimal, dtype=int)
        
        r = np.zeros(len(self.X_init))
        index_zero = (self.index == 0)
        index_nonzero = (self.index != 0)
        r[index_zero] = np.random.randint(-1, 2, size=np.sum(index_zero))
        r[index_nonzero] = 2 * np.random.rand(np.sum(index_nonzero)) - 1
        self.X_next = self.X_init + r * self.step

        for i in range(len(self.X_next)):
            if decimal[i] == 0:
                self.X_next[i] = int(np.round(self.X_next[i]))
            else:
                self.X_next[i] = round(self.X_next[i], decimal[i]) 
        
        self.X_next = np.clip(self.X_next, xMin, xMax)
        
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
    accept_count = 0
    current_run = 0
    early_stop = 0
    early_stop_threshold = 10
    model.preheating(objective_function)
    best_score = model.score
    best_params = model.X_init.copy()
    T_values = []

    while model.T > model.Tf:
        if early_stop >= early_stop_threshold:
            print("Early stopping triggered.")
            break
        for _ in range(n_iterations):
            model.fit(decimal, xMax, xMin)
            score = objective_function(model.X_next)

            delta_score = score - model.score

            if delta_score < 0 or np.random.rand() < np.exp(-delta_score / model.T):
                model.X_init = model.X_next.copy()
                model.score = score
                accept_count += 1
                if score < best_score:
                    best_score = score
                    best_params = model.X_init.copy()
                early_stop = 0
            else:
                early_stop += 1

            current_run += 1
            Record(current_run, model.X_init, model.score, csvfile_name, wbpath, data_label)

        if model.T == model.T0:
            print(f'Initial accept rate: {100 * accept_count / (n_iterations):.2f}%')
        print('-----------------------------------------')
        print(f'Current temperature: {model.T}')
        print(f'Current best score: {best_score}')
        print(f'Current best parameters: {best_params}')

        T_values.append(model.T)
        model.T *= model.k

    print('-----------------------------------------')
    print('SA ended!')
    print('Best parameters:', best_params)
    print('Best score:', best_score)
    return best_score, best_params