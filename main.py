from Bayesian import rbf_kernel, optimize, GaussianProcess
# from Pso import PSO, optimize
# from SA import SA, optimize
import os
import numpy as np
import matplotlib.pyplot as plt


def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    return -(x1**2 - x2/5 + 10)

xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'input 1', 'input 2', 'score1']

# pso = PSO(d=2, size=40, c1=0.5, c2=0.5)
gp = GaussianProcess(kernel=rbf_kernel)
# sa = SA(T0=100, Tf=0.1, k=0.85, step=[3, 3], index=[0, 0], X_init=[0, 0])

optimize(n_iterations,
         xMax,
         xMin,
         decimal,
         objective_function,
         gp, 
         csv_filename,
         wbpath, 
         data_label)

