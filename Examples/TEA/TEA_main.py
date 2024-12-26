import numpy as np
import Pynotes.TEA as TEA

CEPCI   = 821.1
HPA     = 28.04
TCC     = 220.55
TOC     = 2.45373105
TMC     = 0
# W1 = 10.76 + 0.031 + 0.034 + 0.618 + 0.213 + 0.0884 
# W2 = 7.3
# TWC1     = round((W1*3600)*(41/1000) *8000/1000, 2)
# TWC2     = round((W2*3600)*(56/1000) *8000/1000, 2)

FCI_fact  = 0.18
Tax_rate  = 0.35
d_ratio   = [0.2,0.32,0.192,0.1152,0.1152,0.0576]
Cons_per  = 2
Proj_life  = 12
P          = 0
Nnp        = 50
UP         = 100
IRR_Target = 0.15
TWC = 0

def cost(UP):
    """
    Four indexes should be considered
    CBM: Total bare module cost
    CUT: Total utility cost
    CRM: Total raw material cost
    CWT: Waste treatment

    It would be faster to calculate all the expenditures in advance than feed it into this model.
    Args:
        UP (Float): Unit prices

    Returns:
        List: [Revenue, TCC, TOC, TMC, TWC]
    """
    Revenue = round(HPA*UP*8000/1000,2)
    Output_Eco = [Revenue, TCC, TOC, TMC, TWC]
    
    return Output_Eco    

Output_Eco = cost(UP)
IRR        = TEA.TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp)
print('--------------------------------')
print('UP=         ', round(UP,3))
print('IRR=        ', IRR)

while np.abs(IRR-IRR_Target)>0.0001:
    print('--------------------------------')
    UP_new = UP*(1 + 0.02*(IRR_Target-IRR)/(IRR_Target))
    print('UP_new=     ', round(UP_new,3))
    
    Output_Eco = cost(UP_new)
    print('Output_Eco= ', Output_Eco)
    
    IRR=TEA.TEA(Output_Eco, FCI_fact, Tax_rate, d_ratio, Cons_per, Proj_life, P, Nnp)
    print('IRR=        ', IRR)
    
    UP=UP_new