# Techno-economic analysis
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