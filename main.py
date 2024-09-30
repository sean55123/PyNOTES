from Bayesian import rbf_kernel, optimize, GaussianProcess
import numpy as np
import os
import time

def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    return -(x1**2 - x2/5 + 10)

xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 50
csv_filename = 'try_new'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'input 1', 'input 2', 'score1']

gp = GaussianProcess(kernel=rbf_kernel)

start = time.perf_counter()
final_population = optimize(n_iterations,
                            xMax,
                            xMin,
                            decimal,
                            objective_function,
                            gp, 
                            csv_filename,
                            wbpath, 
                            data_label)
end = time.perf_counter()
print(f"Required time {end - start}")