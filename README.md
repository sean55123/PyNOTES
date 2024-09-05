# NTUPSE_packs
NTUPSE_packs is packed with several useful package for all kind of optimization (eg. simulator-based, equation-oriented).
Specifically, Simulated annealing (SA), Particle Swarm Optimization (PSO), and Bayesian Optimization (BO) are for single objective optimization. Fuzzy, and NSGA2, on the other hand, are for multi-objective optimization. Other files, such Economic.py, Get_variable.py, can cooperate with Aspen Plus to perform optimization.


## Simple example for equation-oriented single objective optimization
Single objective optimization should start from main.py
You have to choose the method that you plan to use and import packages from them.
```python
from Bayesian import rbf_kernel, optimize, GaussianProcess
from Pso import PSO, optimize
from SA import SA, optimize
``` 
After importing you have to design the objective function on your own.
For equation-oriented optimization.
```python
def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    return -(x1**2 - x2/5 + 10)
```
Subsequently, customized your algorith with sepecific information, such as upper and lower bondary, decimal places for all the input parameters, number of iteration, csv file name, collecting variables name.
```python
xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'input 1', 'input 2', 'score1']
```
It should be noted that each algorithm needs to be customized with specific parameters as well.

PSO requires: d (Dimension of matrix), size (population size), c1 and c2 (Exploring and Exploiting robustness)

Bayesian requires: kernel (Currently only rbf_kernel can choose)

Simulated Annealing requires: T0 (Initiating temperature), Tf (Termination temperature), k (Cooling gradient), step (Parameter moving speed), index (0 for contiunous, 1 for discrete random variable generating), X_init (Initial points)
```python
pso = PSO(d=2, size=40, c1=0.5, c2=0.5)
gp = GaussianProcess(kernel=rbf_kernel)
sa = SA(T0=100, Tf=0.1, k=0.85, step=[3, 3], index=[0, 0], X_init=[0, 0])
```
Run the optimization via optimization function.
```python
optimize(n_iterations,
         xMax,
         xMin,
         decimal,
         objective_function,
         gp, # Make sure the desired algorithm is added at here.
         csv_filename,
         wbpath, 
         data_label)
```
## Simple example for simulator-based single objective optimization
For Simulator-based optimiation, you have to call your simulator in objective function.
In this example a process optimization taking TAC as objective is used as example.

Noted!! Setting.py can be used to input variables to Aspen Plus, checking result status, and calculate objective function.

The link2apsen() function can help you link Aspen with Python.
All you need to change is the name of the file and the dispatch number for specific Aspen dispatch.

Aspen V11 -> 37.0

Aspen V12 -> 38.0

Asepn V12.1 -> 39.0

Aspen V14 -> 40.0

```python
def link2aspen():
    global filepath
    filepath = os.path.join(os.path.abspath('.'), 'YourAspenFile.apw')
    aspen = win32.Dispatch('Apwn.Document.37.0') # 40.0 for Aspen V14
    aspen.InitFromFile2(filepath)
    aspen.Visible = 0
    aspen.SuppressDialogs = 1
    return aspen
```
The objective function for simulator-based optimization is as followed.

```python
import Setting as set
import win32com.client as win32 

def objective_function(x):
    global aspen
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
```
For simulator-base optimization with self-defined objective function.
```python
def objective_function(x):
    global aspen
    set.var_input(x, aspen)
    status = set.get_status()
    if status == 0:
        obj = set.Cal_obj(aspen)
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
```
Use the get_status() in setting.py to check the status of simulator.

### It is crucial to control the result of simulator
Remeber to change the description of status in setting.py!!!
```python
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
```
Finally, use the Aspen_saving() function to save the final result.
```python
aspen = link2aspen()
set.Aspen_saving(cost_t, aspen, params, filepath, 'Results')
```

## Multi-objective optimization
In here both Fuzzy and NSGA-II can be used to perform the multi-objective optimization.
For NSGA-II, you can define the pop size, and mutation rate.
```python
nsga2 = NSGA(pop_size=100, mutation_rate=0.1)
```
It should be careful that the objective should be designed in following pqttern:
```python
def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    f1 = x1**2 + x2
    f2 = (x2-2)**2 - x1
    return [f1, f2]
```
Besides, if you're doing bi-objective optimization you can apply the Pareto_plot.py to plot the Pareton front.
<img src='Pareto_plot.png'/>



## Techno-economic analysis
In techno-economic analysis TEA.py and TEA_main.py would be needed.
Fortunately, there would be any of the modifications required in TEA.py, all you have to do is adding TCC, TOC, TWC, TMC to the TEA_main.py.
```python
def cost(UP):
    HPA = 28.04
    Revenue = round(HPA*UP*8000/1000,2)
    TCC     = 220.55
    TOC     = 2.45373105
    TMC     = 0
    W1 = 10.76 + 0.031 + 0.034 + 0.618 + 0.213 + 0.0884 
    W2 = 7.3
    TWC1     = round((W1*3600)*(41/1000) *8000/1000, 2)
    TWC2     = round((W2*3600)*(56/1000) *8000/1000, 2)
    TWC = TWC1 + TWC2
    Output_Eco = [Revenue, TCC, TOC, TMC, TWC]
    
    return Output_Eco 
```
After filling the cost index, you will have to change the P (Number of units handling particulates or solids) and Nnp (Number of units handling fluids). Finally, guessing UP letting the results converge. 
```python
FCI_fact  = 0.18
Tax_rate  = 0.35
d_ratio   = [0.2,0.32,0.192,0.1152,0.1152,0.0576]
Cons_per  = 2
Proj_life  = 12
P          = 0
Nnp        = 50
UP         = 1
Output_Eco = cost(UP)
IRR        = TEA.TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp)
IRR_Target = 0.15
```
For example, in this case by guessing UP to 1, the result will not converge.
```python
UP         = 1
```
The output will be:
```
--------------------------------
UP=          1
IRR=         nan
```
Guessing UP to be 100,
```python
UP         = 100
```
The output will be:
```
--------------------------------
UP=          100
IRR=         6.4779
--------------------------------
UP_new=      15.628
Output_Eco=  [3505.67, 220.55, 2.45373105, 0, 0]
IRR=         0.9632
--------------------------------
UP_new=      13.934
Output_Eco=  [3125.56, 220.55, 2.45373105, 0, 0]
IRR=         0.6077
--------------------------------
UP_new=      13.083
Output_Eco=  [2934.82, 220.55, 2.45373105, 0, 0]
IRR=         0.382
--------------------------------
UP_new=      12.678
Output_Eco=  [2844.04, 220.55, 2.45373105, 0, 0]
IRR=         0.2487
--------------------------------
UP_new=      12.512
Output_Eco=  [2806.61, 220.55, 2.45373105, 0, 0]
IRR=         0.1835
--------------------------------
UP_new=      12.456
Output_Eco=  [2794.07, 220.55, 2.45373105, 0, 0]
IRR=         0.1594
--------------------------------
UP_new=      12.44
Output_Eco=  [2790.57, 220.55, 2.45373105, 0, 0]
IRR=         0.1524
--------------------------------
UP_new=      12.436
Output_Eco=  [2789.68, 220.55, 2.45373105, 0, 0]
IRR=         0.1506
--------------------------------
UP_new=      12.435
Output_Eco=  [2789.46, 220.55, 2.45373105, 0, 0]
IRR=         0.1502
--------------------------------
UP_new=      12.435
Output_Eco=  [2789.38, 220.55, 2.45373105, 0, 0]
IRR=         0.15
```
The final MRSP will be 12.435.

## Required Package
```python
import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32 
import time
import matplotlib.pyplot as plt
import csv
import  numpy_financial as npf
import ast
```

## Acknwoledge
The primary developer is Hsuan-Han Chiu with support from the following contributors.
Bor-Yih Yu (National Taiwan University)
Shiau-Jeng Shen (National Taiwan University)

## References
1. Turton, R., et al., Analysis, synthesis and design of chemical processes. 2008: Pearson 
   Education.
2. J. Kennedy and R. Eberhart, "Particle swarm optimization," Proceedings of ICNN'95 - 
   International Conference on Neural Networks, Perth, WA, Australia, 1995, pp. 1942-1948 vol.4
3. D. Bertsimas and J. Tsitsiklis. "Simulated Annealing." Statist. Sci. 8 (1) 10 - 15, 
   February, 1993.
4. K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan. A fast and elitist multiobjective 
   genetic algorithm: nsga-II. Trans. Evol. Comp, 6(2):182–197, April 2002.
5. Pelikan, M. Bayesian Optimization Algorithm. In: Hierarchical Bayesian Optimization 
   Algorithm. Studies in Fuzziness and Soft Computing, vol 170. Springer, Berlin, Heidelberg.