import  numpy as np
import  numpy_financial as npf

 
def CF(FCI, Cons_per, d_ratio, Revenue, COM_D, Tax_rate, Proj_life):
    """Cash flow (CF) will be calculated at heer

    Args:
        FCI_fact (Float): Fixed capital investment factor
        Cons_per (Int): Construction period
        d_ratio (Float): Depreciation ratio
        Revenue (Float): Process revenue with current unit price
        COM_D (Float): Cost of Manufactoring
        Tax_rate (Float): Tax rate of income
        Proj_life (Int): Project life of analysis

    Returns:
        Float: Cash flow
    """
    
    Land     = [0.02*FCI]
    Cap_inv  = [0]
    d        = [0]
    income   = [0]
        
    for i in range(1,Proj_life+Cons_per+1):
        Land_new = 0
        Land.append(Land_new)
            
        if i < (Cons_per+1):
            Cap_inv.append(FCI/Cons_per)
        else:
            Cap_inv.append(0)
        
        if (i > Cons_per) and i < (Cons_per + len(d_ratio) +1):
            d.append(d_ratio[i-Cons_per-1]*FCI)
        else:
            d.append(0)
            
        if i> Cons_per:
            income.append((Revenue-COM_D-d[i])*(1-Tax_rate)+d[i])
        else:
            income.append(0)
    
    Cash_Flow = np.zeros(Proj_life+Cons_per+1)
    for j in range(Proj_life+1):
        Cash_Flow[j]= -Land[j] - Cap_inv[j] + income[j]   
        
    return Cash_Flow

def TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp ):
    """Internal rate of return will be calculated at here.

    Args:
        Output_Eco (List): [Revenue, TCC, TOC, TMC, TWC]
        FCI_fact (Float): Fixed capital investment factor
        Tax_rate (Float): Tax rate of income
        d_ratio (Float): Depreciation ratio
        Cons_per (Int): Construction period
        Proj_life (Int): Project life of analysis
        P (Int): Number of units handling particulates or solids
        Nnp (Int): Number of units handling fluids

    Returns:
        Float: Internal Rate of Return
    """

 
    Revenue   = Output_Eco[0]
    TCC       = Output_Eco[1]
    TOC       = Output_Eco[2]
    TMC       = Output_Eco[3]
    TWC       = Output_Eco[4]
    NOL       = (6.29+31.7*P*P+0.23*Nnp)**0.5
    C_Labor   = round(NOL*4.5)*50000/1000
    FCI       = 1.68*TCC
     
    COM_D     = FCI*FCI_fact + 2.76*C_Labor + 1.23*(TOC+TWC+TMC)
    Tax_rate  = Tax_rate
     
    Cash_Flow =CF(FCI, Cons_per, d_ratio, Revenue, COM_D, Tax_rate, Proj_life)
    IRR = round(npf.irr(Cash_Flow),4)
 
    return IRR