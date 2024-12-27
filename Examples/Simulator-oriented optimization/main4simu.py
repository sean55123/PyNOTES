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
    aspen.Tree.FindNode(r"\Data\Streams\OILIN\Input\TOTFLOW\MIXED").value = Vars[0]
    aspen.Tree.FindNode(r"\Data\Streams\OILIN\Input\TEMP\MIXED").value = Vars[1]
    aspen.Tree.FindNode(r"\Data\Streams\INPUT\Input\TEMP\MIXED").value = Vars[2]
    aspen.Tree.FindNode(r"\Data\Blocks\HX2\Input\VALUE").value = Vars[2]
    aspen.Tree.FindNode(r"\Data\Blocks\COOLER\Input\DUTY").value = -Vars[3]
    aspen.Tree.FindNode(r"\Data\Blocks\HX1\Input\VALUE").value = Vars[4]
    aspen.Tree.FindNode(r"\Data\Blocks\R1\Input\NTUBE").value = Vars[5]
    aspen.Tree.FindNode(r"\Data\Blocks\R1\Input\LENGTH").value = Vars[6]

    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C2H4\Input\PRE_EXP\1").Value   = Vars[7]*409.18
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C2H6\Input\PRE_EXP\1").Value   = Vars[7]*59.172
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C3H6\Input\PRE_EXP\1").Value   = Vars[7]*432.667
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C3H8\Input\PRE_EXP\1").Value   = Vars[7]*1.562
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C4H8\Input\PRE_EXP\1").Value   = Vars[7]*0.21
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C4H10\Input\PRE_EXP\1").Value  = Vars[7]*9.289E-5
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C5DH\Input\PRE_EXP\1").Value   = Vars[7]*2.63336E-5
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C6DH\Input\PRE_EXP\1").Value   = Vars[7]*8.04639E-6
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C7DH\Input\PRE_EXP\1").Value   = Vars[7]*2.19447E-6
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\CH4\Input\PRE_EXP\1").Value    = Vars[7]*45.804
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\RWGS\Input\PRE_EXP\1").Value   = Vars[7]*61.95
    
    aspen.Tree.FindNode(r"\Data\Blocks\R2\Input\NTUBE").value = Vars[8]
    aspen.Tree.FindNode(r"\Data\Blocks\R2\Input\LENGTH").value = Vars[9]

    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C2H4D\Input\PRE_EXP\1").Value  = Vars[10]*409.18
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C2H6D\Input\PRE_EXP\1").Value  = Vars[10]*59.172
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C3H6D\Input\PRE_EXP\1").Value  = Vars[10]*432.667    
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C3H8D\Input\PRE_EXP\1").Value  = Vars[10]*1.562
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C4H8D\Input\PRE_EXP\1").Value  = Vars[10]*0.21
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C4H10D\Input\PRE_EXP\1").Value = Vars[10]*9.289E-5
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C5DHD\Input\PRE_EXP\1").Value  = Vars[10]*2.63336E-5
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C6DHD\Input\PRE_EXP\1").Value  = Vars[10]*8.04639E-6
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\C7DHD\Input\PRE_EXP\1").Value  = Vars[10]*2.19447E-6
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\CH4D\Input\PRE_EXP\1").Value   = Vars[10]*45.804
    aspen.Tree.FindNode(r"\Data\Reactions\Reactions\RWGSD\Input\PRE_EXP\1").Value  = Vars[10]*61.95   
    aspen.Engine.Run2()

def Cal_obj(aspen):
    status = get_status(aspen)
    if status == 0:
                  
        C2 = aspen.Tree.FindNode(r"\Data\Streams\OUT\Output\MASSFLOW\MIXED\C2H4").value
        C3 = aspen.Tree.FindNode(r"\Data\Streams\OUT\Output\MASSFLOW\MIXED\C3H6").value 
        C4 = aspen.Tree.FindNode(r"\Data\Streams\OUT\Output\MASSFLOW\MIXED\C4H8-2").value 
            
        SC = (-C2*1.200 - C3*1.133 - C4*1.301)*8000/1000
        
        # define penalty
        T1Max = aspen.Tree.FindNode(r"\Data\Blocks\R1\Output\TMAX").value
        T2Max = aspen.Tree.FindNode(r"\Data\Blocks\R2\Output\TMAX").value
        R1out = aspen.Tree.FindNode(r"\Data\Streams\PTOC\Output\TEMP_OUT\MIXED").value
        R2out = aspen.Tree.FindNode(r"\Data\Streams\OUT\Output\TEMP_OUT\MIXED").value
        PEN4 = aspen.Tree.FindNode(r"\Data\Streams\OILIN\Output\MASSFLMX\MIXED").value * 1e-3

        if (T1Max > 360):
            PEN1= 100000
            print("T1 temp too high")
        else:
            PEN1 = 0
            
        if (T2Max > 360):
            PEN2= 100000
            print("T2 temp too high")
        else:
            PEN2 = 0
        if (R1out > T1Max) or (R2out > T2Max):
            PEN3 = 1e6
        else:
            PEN3 = 0
        
        obj = PEN1+PEN2+PEN3+PEN4+SC 
    else:
        obj = 1e10
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

    sta2 = aspen.Tree.FindNode(r"\Data\Blocks\R1").AttributeValue(12) & 1 == 1
    sta3 = aspen.Tree.FindNode(r"\Data\Blocks\HX1").AttributeValue(12) & 1 == 1
    sta4 = aspen.Tree.FindNode(r"\Data\Blocks\R2").AttributeValue(12) & 1 == 1
    sta5 = aspen.Tree.FindNode(r"\Data\Blocks\HX2").AttributeValue(12) & 1 == 1
    results = [sta, sta2, sta3, sta4, sta5]
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
Aspen_saving(cost_t, aspen, params, folder_path, 'Results', var_input)