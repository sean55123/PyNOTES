import random as random
import numpy as np
import Get_variable as apvar
import Economics as eco
import time
import matplotlib.pyplot as plt
import os

# 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6 hr
# k1, k2, k3, k4(200)[FOL, 2-MF, POL, 2-MTHF]
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13]
conv_g = [[0, 80.15717092, 92.73084479, 97.64243615, 98.62475442, 99.70707269, 100, 100, 100, 100, 100]]
goal = [[0, 64.04715128, 71.70923379, 59.92141454, 55.00982318, 48.9194499,
         33.79174853, 28.09430255, 19.25343811, 11.98428291, 6.876227898], 
        [0, 11.198428, 17.288802, 32.0235760, 37.72102161, 44.00785855, 
         57.76031434, 62.6719057, 69.9410609, 75.44204322, 80.55009823],
        [0, 0, 0, 0, 0.33557047, 1.342281879, 2.013422819, 2.032702238, 
         2.032702238, 2.204819277, 2.721170396],
        [0, 0, 0, 0, 0, 0.196463654, 0.392927308, 0.392927308, 0.589390963, 
         0.602532, 0.624234]]

weight = [96.08556, 98.10144, 82.10204, 88.14968, 86.1338]
comp_list = ['FUL', 'FOL', '2-MF', '2-POL', '2-MTHF']

#-------------------------------------------------------------------------------------------
# Codes for setting input variables to aspen file
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
            
#-------------------------------------------------------------------------------------------------
# Codes below here are commonly used for calculating objective function
def Conversion(comp):
    # in the unit of %
    conv = [[]]
    init = comp[0]
    for i in range(len(comp)):
        conv[0].append((init - comp[i]) / init * 100)
    return conv

def Yield(comp, base):
    # in the unit of %
    # base = comp[0][0]
    for i in range(len(comp)):
        for j in range(len(comp[i])):
            comp[i][j] = (comp[i][j] / base) * 100
    return comp

def SE(goal, ans):
    sse = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            sse += (goal[i][j] - ans[i][j])**2
    return sse

def MSE(goal, ans):
    sse = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            sse += (goal[i][j] - ans[i][j])**2
    # mse = sse / (len(goal) * len(goal[0]))
    return sse

def RMSE(goal, ans):
    sse = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            sse += (goal[i][j] - ans[i][j])**2
    # rmse = (sse / (len(goal) * len(goal[0]))) ** 0.5
    rmse = sse ** 0.5
    return rmse

def MAPE(goal, ans):
    ape = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            ape += abs(goal[i][j] - ans[i][j])/goal[i][j]
    # mape = ape / (len(goal) * len(goal[0]))
    return ape

def MAE(goal, ans):
    ae = 0
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            ae += abs(goal[i][j] - ans[i][j])
    # mae = ae / (len(goal) * len(goal[0]))
    return ae

def MASE(goal, ans):
    mad = 0
    ase = 0

    mean = np.mean(ans)
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            mad += abs(ans[i][j] - mean)
    mad = mad / (len(goal) * len(goal[0]))
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            ase += abs(goal[i][j] - ans[i][j]) / mad
    # mase = ase / (len(goal) * len(goal[0]))
    return ase

def Cal(aspen):        
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
    return obj  
#--------------------------------------------------------------------------------------------
# Codes for checking convergence
def get_status(aspen):

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
    return [sta, sta2, sta3, sta4, sta5]

#--------------------------------------------------------------------------------------------
def data_write(m, Vars, sse, Sheet):
    
   
    if m == 0:        
        Sheet.write(0, 0, 'Set No')
        Sheet.write(0, 1, 'Vars')
        Sheet.write(0, 1+len(Vars), 'Obj')
                           
    
    Sheet.write(m+1, 0, m+1)    
    
    for j in range(len(Vars)):
        Sheet.write(m+1, j+1, Vars[j])              
    for k in range(1):
        Sheet.write(m+1, k+1+len(Vars), sse)

#--------------------------------------------------------------------------------------------
def TAC_cal(aspen):
    # Essential Constant
    CEPCI = 821.1
    pby = 3
    # CEPCI = 821.1 FOR 2022Sep
    capital_cost_dict = {}
    ope_cost_dict = {}
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RadFrac']:
        D = aspen.Application.Tree.FindNode(fr"\Data\Blocks\{bname}\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1").Value
        V, NT, Tt, Tb, Qc, Qr, P = apvar.getvar_column(D, bname, aspen)
        cap_c, oper_c = eco.column(D, NT, Tt, Tb, Qc, Qr, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # calculate Capital Cost of Flash
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Flash2']:
        V, D, P, n = apvar.getvar_flash(bname, 5, aspen)
        cap_c, oper_c = eco.flash(V, D, P, n, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # calculate Capital Cost of exchanger
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Heater']:
        Ti, To, Q, P = apvar.getvar_exchanger(bname, aspen)
        cap_c, oper_c = eco.exchanger(Ti, To, Q, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # calculate Capital Cost of CSTR
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RCSTR']:
        V, D, Ti, To, P, Q, n = apvar.getvar_reactor(bname, None, None, aspen)
        cap_c, oper_c = eco.reactor(V, D, Ti, To, P, Q, n, "CSTR", CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # calculate Capital Cost of HeatX
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='HeatX']:
        A, P, Tmin = apvar.getvar_heatx(bname, aspen)
        cap_c, oper_c = eco.heatx(A, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    TCC = sum(capital_cost_dict.values()) # kUSD/year
    TOC = sum(ope_cost_dict.values())
    TAC = round(TOC + TCC/pby, 2)
    return TAC
#--------------------------------------------------------------------------------------------
# Do the plot stuff
def Plot(cost_t, aspen, best):
    var_input(best, aspen)
    result_list = [] 
    for i in range(len(comp_list)):
        result_list.append([])
        for j in t:
            node = aspen.Tree.FindNode("\\Data\\Blocks\\R200\\Output\\COMP_MASS\\MIXED\\" + comp_list[i])
            if node == None:
                result_list[i].append(1e6)
            else:
                result_list[i].append(aspen.Tree.FindNode("\\Data\\Blocks\\R200\\Output\\COMP_MASS\\MIXED\\" + comp_list[i] + "\\" + str(j)).value / weight[i] * 1e3)
    
    base = result_list[0][0]        
    conv = Conversion(result_list[0])
    yi = Yield(result_list[1:], base)
    plot_list = ['Conv', 'FOL yield', '2-MF yield', '2-POL yield', '2-MTHF yield']
    for i in range(len(plot_list)):
        if i == 0:
            r = np.array(conv)
            for j in range(len(conv[0])):
                plt.plot(conv_g[0][j], conv[0][j], 'bo')
            plt.plot([r.min(), r.max()], [r.min(), r.max()], 'r-')
            plt.ylabel('Aspen Plus simulation data')
            plt.xlabel('Experimental data')
            plt.title('Conversion Plot')
            plt.savefig(plot_list[i] + ' 200 ' + str(cost_t) + '_MASE3.png')
            plt.close()
            
        else:
            for j in range(len(yi[i-1])):
                r = np.array(goal[i-1])
                plt.plot(goal[i-1][j], yi[i-1][j], 'bo')
            plt.plot([r.min(), r.max()], [r.min(), r.max()], 'r-')
            plt.ylabel('Aspen Plus simulation data')
            plt.xlabel('Experimental data')
            plt.title(plot_list[i] + ' Yield Plot')
            plt.savefig(plot_list[i] + ' 200 ' + str(cost_t) + '_MASE3.png')  
            plt.close()        

#--------------------------------------------------------------------------------------------
# Save the file
def Saving(cost_t, aspen, best, path_folder):
    path = os.path.join(path_folder, 'Two_reactor') + str(cost_t) + '.apw'    
    var_input(best, aspen)
    aspen.saveas(path)            