# from Bayesian import rbf_kernel, optimize, GaussianProcess
from Pso import PSO, optimize
# from SA import SA, optimize
import Setting as set
import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32 
import time


filepath = os.path.join(os.path.abspath('.'), 'YourAspenFile.apw')
aspen = win32.Dispatch('Apwn.Document.37.0') # 40.0 for Aspen V14
aspen.InitFromFile2(filepath)
aspen.Visible = 0
aspen.SuppressDialogs = 1

def objective_function(x):
    set.var_input(x, aspen)
    status = set.get_status()
    if status == 0:
        obj = set.TAC_cal(aspen)
    else:
        obj = 10e7
        aspen.close()
        aspen.quit()
        time.sleep(0.5)
        aspen = win32.Dispatch('Apwn.Document.37.0') # 40.0 for Aspen V14
        aspen.InitFromFile2(filepath)
        aspen.Visible = 0
        aspen.SuppressDialogs = 1
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

optimize(n_iterations,
         xMax,
         xMin,
         decimal,
         objective_function,
         pso, 
         csv_filename,
         wbpath, 
         data_label)