from Bayesian import rbf_kernel, optimize, GaussianProcess
# from Pso import PSO, optimize
# from SA import SA, optimize
import os
import numpy as np
import matplotlib.pyplot as plt

n_objectives = 2
xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 30
csv_filename = 'try'
data_label = ['num of runs', 'input 1', 'input 2', 'score']

# pso = PSO(d=2, size=40, c1=0.5, c2=0.5)
gp = GaussianProcess(kernel=rbf_kernel)
# sa = SA(T0=100, Tf=0.1, k=0.85, step=[3, 3], index=[0, 0], X_init=[0, 0])
method = gp

def multi_objective_function(x, index=0, index_i=0):
    x1 = x[0]
    x2 = x[1]
    
    obj = [
            x1**2 - x2/5,
            (x1 - x2**2),
    ]
    
    if index_i == 0:
        return obj[index]
    else:
        return -(obj[index])

def objective_function(x, index_i):
    return multi_objective_function(x, index, index_i)

def fuzzy_objective_function(x):
    x1 = x[0]
    x2 = x[1]
    
    obj = [
            x1**2 - x2/5,
            (x1 - x2**2),
    ]
    obj = np.array(obj)
    obj = (max_scores-obj)/scores
    obj = max(((max_scores-obj)/scores))
    return -obj
    

scores = np.zeros(n_objectives*2)
num = -1

for i in range(n_objectives):
    index = i
    filename1 = csv_filename + '_target' + str(i+1)
    for j in range(2):
        num += 1
        for k in range(2):
            filename2 = filename1 + '_run' + str(k+1)
            if j == 1:
                index_i = 1
                filename3 = filename2 + '_minimize'
                wbpath = os.path.join(os.path.abspath('.'), filename3)

                res = optimize(n_iterations,
                               xMax,
                               xMin,
                               decimal,
                               lambda x: objective_function(x, index_i),
                               method, 
                               filename3,
                               wbpath, 
                               data_label)
                if k == 0:
                    scores[num] = -res
                else:
                    if -res > scores[num]:
                        scores[num] = -res
            
            else:
                index_i = 0
                filename3 = filename2 + '_maximize'
                wbpath = os.path.join(os.path.abspath('.'), filename3)
                res = optimize(n_iterations,
                               xMax,
                               xMin,
                               decimal,
                               lambda x: objective_function(x, index_i),
                               method, 
                               filename3,
                               wbpath, 
                               data_label)
                if k == 0:
                    scores[num] = res
                else:
                    if scores[num] > res:
                        scores[num] = res
                        
print('-----------------------------------------') 
print('Results from previous runs: ', scores)
max_scores = []
for i in range(n_objectives):
    max_scores.append(scores[2*i+1])
min_scores = np.array(max_scores)
scores = np.diff(scores.reshape(n_objectives, -1)).flatten()
csv_filename += '_fuzzy'
wbpath = os.path.join(os.path.abspath('.'), csv_filename)
res = optimize(n_iterations,
               xMax,
               xMin,
               decimal,
               fuzzy_objective_function,
               method, 
               csv_filename,
               wbpath, 
               data_label)

print('-----------------------------------------') 
print(f"Fuzzy final satisfication {-res:.2%}")