from Pynotes.Pso import PSO, optimize
from Pynotes.Aspen_commander import link2aspen, TAC_cal, Aspen_saving
import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32 
import time

# =======================================================================================
# This part is for Aspen setting
# =======================================================================================
def var_input(Vars,aspen):        
    aspen.Tree.FindNode(r"\Data\Blocks\DIST\Input\NSTAGE").value = Vars[0]
    aspen.Tree.FindNode(r"\Data\Blocks\DIST\Input\FEED_STAGE\INPUT").value = Vars[1]
    aspen.Tree.FindNode(r"\Data\Blocks\DIST\Input\BASIS_D").value = Vars[2]
    aspen.Tree.FindNode(r"\Data\Blocks\DIST\Input\BASIS_RR").value = Vars[3]
    aspen.Engine.Run2()

def Cal_obj(aspen):
    """Customize your objective function here.
    """
    status = get_status(aspen)
    if status == 0:
        obj = 0
    return obj  

def get_status(aspen, Display=1):
    status = 1 # Status 0 for converge, 1 for diverge
    Node = aspen.Tree.FindNode(r"\Data\Results Summary\Run-Status")
    if Node == None:
        sta = 32
    elif (Node.AttributeValue(12) & 1 ==1) or (Node.AttributeValue(12) & 4 == 4):
        sta = 1
    else:
        sta = 32

    sta2 = aspen.Tree.FindNode(r"\Data\Blocks\DIST").AttributeValue(12) & 1 == 1
    results = [sta, sta2]
    if sum(results) == len(results):
        status = 0
    if Display == 1:
        if status == 0:
            print("Results available")
        else:
            print("Results with errors")
    return status


def objective_function(x):
    global filepath
    aspen, filepath = link2aspen('YourAspenFile.apw')
    var_input(x, aspen)
    status = get_status()
    if status == 0:
        obj = TAC_cal(aspen) # Self-deifined objective please use Cal_obj function
        obj = [obj, status]
    else:
        obj = [10e7, status]
        aspen.close()
        aspen.quit()
        time.sleep(0.5)
        aspen, filepath = link2aspen('YourAspenFile.apw')
    return obj



# =======================================================================================
# This part is for optimization method setting
# =======================================================================================
xMax, xMin = [30, 20, 150, 10], [10, 15, 50, 0.01]
decimal = [0, 0, 2, 2]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ["num of runs", "Num of stage", "Input stage", "Distillate rate", "Reflux ratio", "TAC"]

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
Aspen_saving(cost_t, aspen, params, folder_path, 'Results', var_input)