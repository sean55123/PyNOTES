import win32com.client as win32 
import os
import Get_variable as apvar
import Economics as eco
import numpy as np
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def link2aspen(Aspen_file, Visible=0, SuppressDialogs=1, Dispatch=37):
    filepath = os.path.join(os.path.abspath('.'), Aspen_file)
    aspen = win32.Dispatch('Apwn.Document.37.0') # 40.0 for Aspen V14
    aspen.InitFromFile2(filepath)
    aspen.Visible = 0
    aspen.SuppressDialogs = 1
    return aspen, filepath

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

        node = aspen.Application.Tree.FindNode(fr"\Data\Blocks\{bname}\Subobjects\Column Internals\INT-1\Subobjects\Sections\CS-1\Input\CA_DIAM\INT-1\CS-1")
        if node is None:
            logging.error(f"Default column diameter is used. '{bname}' needs to set the column internal specification")
            D = 0.68  # Assign default value or handle as needed
        else:
            D = node.Value
        
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

def Aspen_saving(cost_t, aspen, best, folder_path, filename, var_input):
    """In order to save Aspen Plus file at the end or during the optimization.
    
    Args:
        cost_t (Float): Recorded calculation time.
        aspen (String): Aspen Plus execution file.
        best (List): List of variables that own the best score.
        path_folder (String): Path of the operating file.
        filename (String): Desired name for saving
    """
    path = os.path.join(folder_path, filename) + str(cost_t) + '.apw'    
    var_input(best, aspen)
    aspen.saveas(path)
    aspen.close()
    aspen.quit()