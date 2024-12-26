from Pynotes.Pso import PSO, optimize
from Pynotes.Aspen_commander import link2aspen
import Pynotes.Setting as set
import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32 
import time

def objective_function(x):
    global filepath
    aspen, filepath = link2aspen('YourAspenFile.apw')
    set.var_input(x, aspen)
    status = set.get_status()
    if status == 0:
        obj = set.TAC_cal(aspen)
        obj = [obj, status]
    else:
        obj = [10e7, status]
        aspen.close()
        aspen.quit()
        time.sleep(0.5)
        aspen, filepath = link2aspen('YourAspenFile.apw')
    return obj

xMax, xMin = [36, 44, 17, 54, 30, 25, 36, 17], [20, 28, 3, 30, 10, 19, 24, 1]
decimal = [0, 2, 0, 0, 2, 0, 0, 0]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'HPC NT', 'HPC P', 'HPC FT', 'LPC NT', 'LPC P', 'LPC FT', 'DEM NT', 'DEM FT', 'TAC']

pso = PSO(d=2, size=40, c1=0.5, c2=0.5)
# gp = GaussianProcess(kernel=rbf_kernel)
# sa = SA(T0=100, Tf=0.1, k=0.85, step=[3, 3], index=[0, 0], X_init=[0, 0])

start_time = time.perf_counter()
score, params = optimize(n_iterations,
                xMax,
                xMin,
                decimal,
                objective_function,
                pso, 
                csv_filename,
                wbpath, 
                data_label)
end_time = time.perf_counter()
cost_t = round(end_time - start_time, 1)

folder_path = os.path.dirname(filepath)
aspen = link2aspen('YourAspenFile.apw')[0]
set.Aspen_saving(cost_t, aspen, params, folder_path, 'Results')