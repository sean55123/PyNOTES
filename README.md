# NTUPSE_packs
NTUPSE_packs is packed with several useful package for all kind of optimization (eg. simulator-based, equation-oriented).
Specifically, Simulated annealing (SA), Particle Swarm Optimization (PSO), and Bayesian Optimization (BO) are for single objective optimization. Fuzzy, and NSGA2, on the other hand, are for multi-objective optimization. Other files, such Economic.py, Get_variable.py, can cooperate with Aspen Plus to perform optimization.


## Simple example
Single objective optimization should start from main.py
You have to choose the method that you plan to use and import packages from them.
'''python
from Bayesian import rbf_kernel, optimize, GaussianProcess
from Pso import PSO, optimize
from SA import SA, optimize
'''
After importing you have to design the objective function on your own.
For equation-oriented optimization.
'''python
def objective_function(x):
    x1 = x[0]
    x2 = x[1]
    return -(x1**2 - x2/5 + 10)
'''
For Simulator-based optimiation, you have to call your simulator in objective function.
In this example a process optimization taking TAC as objective is used as example.

Noted!! Setting.py can be used to input variables to Aspen Plus, checking result status, and calculate objective function.
'''python
import Setting.py as set

filepath = os.path.join(os.path.abspath('.'),'YourAspenFile.apw')
aspen = win32.Dispatch('Apwn.Document.40.0') # 40.0 for Aspen V14
aspen.InitFromFile2(filepath)
aspen.Visible = 0
aspen.SuppressDialogs = 1

def objective_function(x):
    set.var_input(x, aspen)
    obj = set.TAC_cal(aspen)
    return obj
'''
For simulator-base optimization with self-defined objective function.
'''python
def objective_function(x):
    set.var_input(x, aspen)
    obj = set.Cal_obj(aspen)
    return obj
'''
Subsequently, customized your algorith with sepecific information, such as upper and lower bondary, decimal places for all the input parameters, number of iteration, csv file name, collecting variables name.
'''python
xMax, xMin = [10.0, 10.0], [-10.0, -10.0]
decimal = [2, 2]
n_iterations = 50
csv_filename = 'try'
wbpath = os.path.join(os.path.abspath('.'),csv_filename)
data_label = ['num of runs', 'input 1', 'input 2', 'score1']
'''
It should be noted that each algorithm needs to be customized with specific parameters as well.
PSO requires: d (Dimension of matrix), size (population size), c1 and c2 (Exploring and Exploiting robustness)
Bayesian requires: kernel (Currently only rbf_kernel can choose)
Simulated Annealing requires: T0 (Initiating temperature), Tf (Termination temperature), k (Cooling gradient), step (Parameter moving speed), index (0 for contiunous, 1 for discrete random variable generating), X_init (Initial points)
'''python
pso = PSO(d=2, size=40, c1=0.5, c2=0.5)
gp = GaussianProcess(kernel=rbf_kernel)
sa = SA(T0=100, Tf=0.1, k=0.85, step=[3, 3], index=[0, 0], X_init=[0, 0])
'''
Run the optimization via optimization function.
'''python
optimize(n_iterations,
         xMax,
         xMin,
         decimal,
         objective_function,
         gp, # Make sure the desired algorithm is added at here.
         csv_filename,
         wbpath, 
         data_label)
'''