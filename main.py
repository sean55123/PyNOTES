from NSGA2 import NSGA, optimize
import numpy as np
import os
import time

nsga2 = NSGA(pop_size=100, mutation_rate=0.1)

def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    f1 = x1**2 + x2
    f2 = (x2-2)**2 - x1
    return [f1, f2]

xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'input 1', 'input 2', 'Objective']

start = time.perf_counter()
final_population = optimize(n_iterations,
                            xMax,
                            xMin,
                            decimal,
                            objective_function,
                            nsga2, 
                            csv_filename,
                            wbpath, 
                            data_label)
end = time.perf_counter()
print(f"Required time {end - start}")