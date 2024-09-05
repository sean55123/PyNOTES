import numpy as np
import Get_variable as apvar
import Economics as eco
import os

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
        

def TAC_cal(aspen):
    """Auto calculation of economic. Designed by Shiau-Jeng Shen.
    Calculated result in the unit of kUSD/year

    Args:
        aspen (String): Your Aspen Plus file

    Returns:
        Float: Total annual cost with specific PBY and CEPCI
    """
    CEPCI = 821.1 # 2022 SEP
    pby = 3

    capital_cost_dict = {}
    ope_cost_dict = {}
    
    # Calculate Capital Cost of Distillation Tower
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RadFrac']:
        D = aspen.Application.Tree.FindNode(fr"\Data\Blocks\{bname}\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1").Value
        V, NT, Tt, Tb, Qc, Qr, P = apvar.getvar_column(D, bname, aspen)
        cap_c, oper_c = eco.column(D, NT, Tt, Tb, Qc, Qr, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # Calculate Capital Cost of Flash
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Flash2']:
        V, D, P, n = apvar.getvar_flash(bname, 5, aspen)
        cap_c, oper_c = eco.flash(V, D, P, n, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # Calculate Capital Cost of exchanger
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Heater']:
        Ti, To, Q, P = apvar.getvar_exchanger(bname, aspen)
        cap_c, oper_c = eco.exchanger(Ti, To, Q, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # Calculate Capital Cost of CSTR
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='RCSTR']:
        V, D, Ti, To, P, Q, n = apvar.getvar_reactor(bname, None, None, aspen)
        cap_c, oper_c = eco.reactor(V, D, Ti, To, P, Q, n, "CSTR", CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    # Calculate Capital Cost of HeatX
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='HeatX']:
        A, P, Tmin = apvar.getvar_heatx(bname, aspen)
        cap_c, oper_c = eco.heatx(A, P, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c
    
    # Calculates Capital Cost for Compressor
    for bname in [item.name for item in aspen.Tree.FindNode(r'\Data\Blocks').Elements if item.AttributeValue(6)=='Compr']:
        W = apvar.getvar_compressor(bname, aspen)
        cap_c, oper_c = eco.compressor(W, CEPCI)
        capital_cost_dict[bname] = cap_c
        ope_cost_dict[bname] = oper_c

    TCC = sum(capital_cost_dict.values())
    TOC = sum(ope_cost_dict.values())
    TAC = round(TOC + TCC/pby, 2)
    return TAC

def Aspen_saving(cost_t, aspen, best, path_folder, filename):
    """In order to save Aspen Plus file at the end or during the optimization.
    
    Args:
        cost_t (Float): Recorded calculation time.
        aspen (String): Aspen Plus execution file.
        best (List): List of variables that own the best score.
        path_folder (String): Path of the operating file.
        filename (String): Desired name for saving
    """
    path = os.path.join(path_folder, filename) + str(cost_t) + '.apw'    
    var_input(best, aspen)
    aspen.saveas(path)            