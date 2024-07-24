import numpy as np

def reactor(V, D, Ti, To, P, Q, n, index, CEPCI):
    """
    Here calculates the bare module cost for reactor.
    Besides, RYield, RGibbs, RStioc are considered as batch reactor.
    Heat generated from exothermic reactor will be used to generate corresponding level of steam as credits.
    
    Args:
        V (Float): Reactor volume (cubic meter == m3)
        D (Float): Reactor diameter (meter)
        Ti (Float): Tube-side inlet temperature (oC)
        To (Float): Tube-side outlet temperature (oC)
        P (Float): Stream pressure (Bar)
        Q (Float): Reaction heat (kW)
        n (Integer): Number of tubes (if the reactor is multi-tube reactor)
        index (String): Type of reactor
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep

    Returns:
        List: [Captital cost, Operating cost]
    """
    FP_v = (P*D/(2*944*0.9-1.2*P)+0.00315)/0.0063

    if FP_v <= 1:
        FP = 1
    elif P < -0.5:
        FP = 1.25
    else:
        FP = FP_v

    if index == "BATCH":
        if V <= 0.3:
            V = 0.3
            
        CP_R = 10**(3.4974+0.4485*np.log10(V)+0.1074*(np.log10(V))**2)/1000
        CBM_R = CP_R*(2.25+1.82*1*FP)*n
        Ti = To

    if index == "PFR":
        if Q == 0:
            if V <= 0.3:
                V = 0.3
            CP_R = 10**(3.4974+0.4485*np.log10(V)+0.1074*(np.log10(V))**2)/1000
        else:
            if V < 5:
                V = 5
            CP_R = 10**(3.3496+0.7235*np.log10(V)+0.0025*(np.log10(V))**2)/1000   
        
        CBM_R = CP_R*(2.25+1.82*1*FP)*n

    if index == "CSTR":
        if Q == 0:
            if V <= 0.3:
                V = 0.3
            CP_R = 10**(3.4974+0.4485*np.log10(V)+0.1074*(np.log10(V))**2)/1000
        else:
            if V < 0.1:
                V = 0.1
            CP_R = 10**(4.1052+0.5320*np.log10(V)-0.0005*(np.log10(V))**2)/1000
        
        CBM_R = CP_R*(2.25+1.82*1*FP)*n
        Ti = To

    if Q < 0:
        if (To>40) & (To<130):
            Tlm = ((Ti-40)-(To-30))/np.log((Ti-40)/(To-30))
            OPER = -Q*3600*8000*0.378/10**9
            A = -Q/0.568/Tlm
            
        elif (To>=130) & (To<170):
            if Ti-To == 0:
                Tlm = Ti-120
            else:
                Tlm = ((Ti-120)-(To-120))/np.log((Ti-120)/(To-120))  
            OPER = Q*3600*8000*(4.11/10^9-1.523/2203.04/10**6)
            A = -Q/0.568/Tlm
        
        elif (To>=170) & (To<194): 
            if Ti-To == 0:
                 Tlm = Ti-160
            else:
                 Tlm = ((Ti-160)-(To-160))/np.log((Ti-160)/(To-160))
            OPER = Q*3600*8000*(4.54/10**9-1.523/2081.86/10**6)
            A = -Q/0.568/Tlm
        
        elif (To>=194) & (To<264): 
             if Ti-To == 0:
                Tlm = Ti-18
             else:
                Tlm = ((Ti-184)-(To-184))/np.log((Ti-184)/(To-184))
             
             OPER = Q*3600*8000*(4.77/10**9-1.523/1999.72/10**6)
             A = -Q/0.568/Tlm
        else:
            if Ti-To == 0:
                Tlm = Ti-254
            else:
                Tlm = ((Ti-254)-(To-254))/np.log((Ti-254)/(To-254))
         
            OPER = Q*3600*8000*(5.66/10**9-1.523/1694.34/10**6)
            A = -Q/0.568/Tlm
        
    elif Q > 0:
        if To > 174:
            if Ti-To == 0:
                Tlm = 254-Ti
            else:
                Tlm = ((254-Ti)-(254-To))/np.log((254-Ti)/(254-To))
            
            OPER = Q*3600*8000*5.66/10^9
            A = Q/0.568/Tlm
        elif To > 150:
            if Ti-To == 0:
                Tlm = 184-Ti
            else:
                Tlm = ((184-Ti)-(184-To))/np.log((184-Ti)/(184-To))
            
            OPER = Q*3600*8000*4.77/10**9
            A = Q/0.568/Tlm  
        
        elif To > 110:
            if Ti-To == 0:
                Tlm = 160-Ti
            else:
                Tlm = ((160-Ti)-(160-To))/np.log((160-Ti)/(160-To))
            
            OPER = Q*3600*8000*4.54/10**9
            A = Q/0.568/Tlm
        
        else:
            if Ti-To == 0:
                Tlm = 120-Ti
            else:
                Tlm = ((120-Ti)-(120-To))/np.log((120-Ti)/(120-To))
            OPER = Q*3600*8000*4.11/10**9
            A = Q/0.568/Tlm        
    else:
        OPER = 0

    if P < 5:
        FP_HX = 1     
    else:
        FP_HX = 10**(0.03881-0.11272*np.log10(P)+0.08183*(np.log10(P))**2)

    if index == "BATCH":
        if Q == 0:
            CP_HX = 0
        else:
            CP_HX = 10**(4.3247-0.3030*np.log10(A)+0.1634*(np.log10(A))**2)
    else:
        CP_HX = 0
   
    CBM_HX = CP_HX*(1.63+1.66*1*FP_HX)/1000 
    CAP = round((CBM_R+CBM_HX)*CEPCI/397, 2)
    OPER = round(OPER, 2)
    return [CAP, OPER]

def flash(V, D, P, n, CEPCI):
    """
    Operating cost in the flash is considered to be zero.
    In other word, when calculating cost from flash, it's necessary to set the duty to be 0.
    Heat adding and removing should be carried out in heat exchanger.
    
    Args:
        V (Float): Vessel volume (cubic meter == m3)
        D (Float): Vessel diameter (meter)
        P (Float): Operating pressure (Bar)
        n (Integer): Number of the column, set to 1
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep

    Returns:
        List: [Captital cost, Operating cost]
    """
    FP_v = (P*D/(2*944*0.9-1.2*P)+0.00315)/0.0063
    if FP_v <= 1:
        FP = 1
    elif P < -0.5:
        FP = 1.25
    else:
        FP = FP_v  
    CP_F = 10**(3.4974+0.4485*np.log10(V)+0.1074*(np.log10(V))**2)/1000
    CBM_F = round((CP_F*(2.25+1.82*1*FP)*n)*CEPCI/397, 2)
    return [CBM_F, 0]

def heatx(A, P, CEPCI):
    """If the heat exchanger area is lower than 10 and larger than 1 square meter (m2), double pipe exchanger will be applied.
    If the area is in the range of 10 to 1000 square meter (m2), fixed tube heat exchanger will be used.
    Args:
        A (Float): Heat exchanging area
        P (Float): Operating pressure
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep

    Returns:
        List: [Bare model cost, 0]
    """
    if P < 5:
       FP_HX = 1     
    else:
       FP_HX = 10**(0.03881-0.11272*np.log10(P)+0.08183*(np.log10(P))**2)   
    if A > 10:
        CP = 10**(4.3247-0.3030*np.log10(A)+0.1634*(np.log10(A))**2)
    elif A <= 10:
        CP = 10**(3.3444+0.2745*np.log10(A)-0.0472*np.log10(A)**2)
        
    CBM = round((CP*(1.63+1.66*1*FP_HX)/1000)*CEPCI/397, 2)
    return [CBM, 0]

def column(D, NT, Tt, Tb, Qc, Qr, P, CEPCI):
    """
    Capital cost of column is calculated in four separated parts:
    1. Tower
    2. Tray
    3. Condenser (Top)
    4. Reboiler (Bot)
    
    It should be noted that the stage height is set to be 0.6096 meter as default,
    heat recovered in the cooler is used to generate corresponding level of steam as well.

    If the heat exchanger area is lower than 10 and larger than 1 square meter (m2), double pipe exchanger will be applied.
    If the area is in the range of 10 to 1000 square meter (m2), fixed tube heat exchanger will be used.
    
    Args:
        D (Float): Tray diameter (meter)
        NT (Integer): Number of tray 
        Tt (Float): Tower top temperature (oC)
        Tb (Float): Tower bot temperature (oC)
        Qc (Float): Condenser duty (kW)
        Qr (Float): Reboiler duty (kW)
        P (Float): Operating pressure (Bar)
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep
        
    Returns:
        List: [Captital cost, Operating cost]
    """
    H = float(NT)*0.6096*1.2
    V = np.pi/4*D*D*H
    FM = 1
    FP_v = (P*D/(2*944*0.9-1.2*P)+0.00315)/0.0063

    if FP_v <= 1:
        FP_vessel = 1
    elif P < -0.5:
        FP_vessel = 1.25
    else:
        FP_vessel = FP_v
    
    Cp_Tower = 10**(3.4974 + 0.4485*np.log10(V) + 0.1074*(np.log10(V))**2)
    CBM_Tower = Cp_Tower*(2.25+1.82*FM*FP_vessel)/1000

    A = 3.14159/4*D*D
    Cp_Tray = 10**(2.9949 + 0.4465*np.log10(A) + 0.3961*(np.log10(A))**2)

    if NT < 20:
        Fq = 10**(0.4771+0.08516*np.log10(float(NT))-0.3473*(np.log10(float(NT)))**2)
    else:
        Fq = 1

    FBM_Tray = 1
    CBM_Tray = Cp_Tray*float(NT)*FBM_Tray*Fq/1000

    if Tt >= 194:
        Cond1lm = Tt-184
        Opt_C = Qc*3600*8000*(4.77/10**9-1.523/1999.72/10**6)
        Ac = -Qc/0.852/Cond1lm
    elif Tt >= 170: 
        Cond1lm = Tt-160
        Opt_C = Qc*3600*8000*(4.54/10**9-1.523/2081.86/10**6)
        Ac = -Qc/0.852/Cond1lm
    elif Tt >= 130:
        Cond1lm = (Tt-120)
        Ac = -Qc/0.852/Cond1lm
        Opt_C = Qc*3600*8000*(4.11/10**9-1.523/2203.04/10**6)
    elif Tt >= 47:
        Cond1lm = ((Tt-40)-(Tt-30))/np.log((Tt-40)/(Tt-30))
        Opt_C = -Qc*3600*8000*0.378/10**9
        Ac = -Qc/0.852/Cond1lm
    elif Tt >= 10:
        Cond1lm = ((Tt-15)-(Tt-5))/np.log((Tt-15)/(Tt-5))
        Ac = -Qc/0.852/Cond1lm
        Opt_C = -Qc*3600*8000*4.77/10**9
    elif Qc == 0:
        Ac = 0
        Opt_C = 0
    else:
        Ac = 10**4
        Opt_C = 10**8
       
    if Tb >= 264:
        Opt_R = 10**8
        Ar = 10^4
    elif Tb >= 174:
        Ar = Qr/0.568/(254-Tb)
        Opt_R = Qr*3600*8000*5.66/10**9
    elif Tb >= 150:
        Ar = Qr/0.568/(184-Tb)
        Opt_R = Qr*3600*8000*4.77/10**9
    elif Tb >= 110:
        Ar = Qr/0.568/(160-Tb)
        Opt_R = Qr*3600*8000*4.54/10**9
    elif Qr == 0:
        Ar = 0
        Opt_R = 0
    else:
        Ar = Qr/0.568/(120-Tb)
        Opt_R = Qr*3600*8000*4.11/10**9   
        
    if Qc == 0:
        CP_C = 0
    elif Qc != 0 and Ac > 10:
        CP_C = 10**(4.3247-0.3030*np.log10(Ac)+0.1634*(np.log10(Ac))**2)
    elif Qc != 0 and Ac <= 10:
        CP_C = 10**(3.3444+0.2745*np.log10(A)-0.0472*np.log10(A)**2)

    if Qr == 0:
        CP_R = 0
    elif Qr != 0 and Ar > 10:
        CP_R = 10**(4.3247-0.3030*np.log10(Ar)+0.1634*(np.log10(Ar))**2)
    elif Qr != 0 and Ar <= 10:
        CP_R = 10**(3.3444+0.2745*np.log10(A)-0.0472*np.log10(A)**2)

    if P < 5:
        FP_HX = 1
    else:
        FP_HX = 10**(0.03881-0.11272*np.log10(P)+0.08183*(np.log10(P))**2)
    
    if Qc > 0:
        CBM_C = 0
        Opt_C = 0
    if Qr < 0:
        CBM_R = 0
        Opt_R = 0
    
    CBM_C = CP_C*(1.63+1.66*1*FP_HX)/1000
    CBM_R = CP_R*(1.63+1.66*1*FP_HX)/1000
    CAP = round((CBM_Tower+CBM_Tray+CBM_C+CBM_R)*CEPCI/397, 2)
    OPER = round(Opt_C+Opt_R, 2)
    return[CAP, OPER]    

def compressor(W, CEPCI):
    """
    Work between 450 to 3000 kW will apply centrifugal comppressor, 
    in the range of 18 to 450 kW will apply rotary compressor,
    work less than 18 will set to be 18 kW.
    
    !!Beware the units of works!!
    
    Args:
        W (Float): Compressor duty (kW)
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep
        
    Returns:
        List: [Captital cost, Operating cost]
    """
    W = W/1000
    if (W>=450) & (W<3000):
        CP = 10**(2.2897+1.3604*np.log10(W)-0.1027*(np.log10(W))**2) # Centrifugal compressor
    elif (W>=18) & (W<450):
        CP = 10**(5.0355-1.8002*np.log10(W)+0.8253*(np.log10(W))**2) # Rotary Compressor
    else:
        W_limit = 18
        CP = 10**(5.0355-1.8002*np.log10(W_limit)+0.8253*(np.log10(W_limit))**2)

    FBM = 2.7
    CBM = round((CP*FBM/1000)*CEPCI/397, 2)
    OPER = round(W*3600*8000/10**9*18.72, 2)
    return [CBM, OPER]

def exchanger(Ti, To, Q, P, CEPCI):
    """If the heat exchanger area is lower than 10 and larger than 1 square meter (m2), double pipe exchanger will be applied.
    If the area is in the range of 10 to 1000 square meter (m2), fixed tube heat exchanger will be used.

    Args:
        Ti (Float): Stream inlet temperature (oC)
        To (Float): Stream outlet temperature (oC)
        Q (Float): Duty (kW)
        P (Float): Stream pressure (Bar)
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep
        
    Returns:
        List: [Captital cost, Operating cost]
    """
    if Q < 0:
        if  To >= 264:
            Tlm = To-254
            OPER = Q*3600*8000*(5.66/10**9-1.523/1999.72/10**6)
            A = -Q/0.852/Tlm
        elif To >= 194:
            Tlm = To-184
            OPER = Q*3600*8000*(4.77/10**9-1.523/1999.72/10**6)
            A = -Q/0.852/Tlm
        elif To >= 170: 
            Tlm = To-160
            OPER = Q*3600*8000*(4.54/10**9-1.523/2081.86/10**6)
            A = -Q/0.852/Tlm
        elif To >= 130:
            Tlm = (To-120)
            A = -Q/0.852/Tlm
            OPER = Q*3600*8000*(4.11/10**9-1.523/2203.04/10**6)
        elif To >= 47:
            Tlm = ((To-40)-(Ti-30))/np.log((To-40)/(Ti-30))
            OPER = -Q*3600*8000*0.378/10**9
            A = -Q/0.852/Tlm
        elif To >= 10:
            Tlm = ((To-15)-(Ti-5))/np.log((To-15)/(Ti-5))
            A = -Q/0.852/Tlm
            OPER = -Q*3600*8000*4.77/10**9
        elif To >= -17:
            Tlm = ((To-(-19))-(Ti-(-20)))/np.log((To-(-19))/(Ti-(-20)))
            A = -Q/0.852/Tlm
            OPER = -Q*3600*8000*7.89/10**9
        elif To >= -46:
            Tlm = ((To-(-48))-(Ti-(-49)))/np.log((To-(-48))/(Ti-(-49)))
            A = -Q/0.852/Tlm
            OPER = -Q*3600*8000*13.11/10**9
        else:
            A = 10^4
            OPER = 10^8
    else:
        if To > 174:
            Tlm = ((254-Ti)-(254-To))/np.log((254-Ti)/(254-To))
            OPER = Q*3600*8000*5.66/10**9
            A = Q/0.568/Tlm
        elif To > 150:
            Tlm = ((184-Ti)-(184-To))/np.log((184-Ti)/(184-To))
            OPER = Q*3600*8000*4.77/10**9
            A = Q/0.568/Tlm    
        elif To > 110:
            Tlm = ((160-Ti)-(160-To))/np.log((160-Ti)/(160-To))
            OPER = Q*3600*8000*2.78/10**9
            A = Q/0.568/Tlm
        else:
            Tlm = ((120-Ti)-(120-To))/np.log((120-Ti)/(120-To))
            OPER = Q*3600*8000*2.52/10**9
            A = Q/0.568/Tlm
            
    if P < 5:
        FP_HX = 1     
    else:
        FP_HX = 10**(0.03881-0.11272*np.log10(P)+0.08183*(np.log10(P))**2)
        
    if A > 10:
        CP = 10**(4.3247-0.3030*np.log10(A)+0.1634*(np.log10(A))**2)
    elif A <= 10:
        CP = 10**(3.3444+0.2745*np.log10(A)-0.0472*np.log10(A)**2)
        
    CBM = CP*(1.63+1.66*1*FP_HX)/1000
    
    CAP = round(CBM*CEPCI/397, 2)
    OPER = round(OPER, 2)
    return [CAP, OPER]

def extractor(V, D, P, CEPCI):
    """
    Args:
        V (Float): Vessel volume (cubic meter == m3)
        D (Float): Vessel diameter (meter)
        P (Float): Operating pressure (Bar) 
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep
        
    Returns:
        List: [Captital cost, Operating cost]
    """
    FP_v = (P*D/(2*944*0.9-1.2*P)+0.00315)/0.0063
    if FP_v <= 1:
        FP = 1
    elif P < -0.5:
        FP = 1.25
    else:
        FP = FP_v
    
    CP_D = 10**(3.5565+0.3776*np.log10(V)+0.0905*(np.log10(V))**2)/1000
    CBM_D = CP_D*(2.25+1.82*1*FP)*CEPCI/397
    return[CBM_D, 0]

def vacuum(V, P, name1, name2, bname1, bname2, CEPCI, aspen):
    """_summary_

    Args:
        V (Float): Vessel volume (cubic meter == m3)
        P (Float): Operatimg pressure (Bar)
        name1 (): 
        name2 (): 
        bname1 (): 
        bname2 (): 
        CEPCI (Float): CEPCI, 822.1 for 2022 Sep
        aspen (): 
        
    Returns:
        List: [Captital cost, Operating cost]
    """  
    W = (5+(0.0298+0.03088*np.log((P+1)*760)-0.0005733*np.log((P+1)*760)**2)*(V*35.3147)**0.66)*0.4536
 
    # print('V   =  ', round(V,2), '   W   =   ', round(W,2))    
    
    aspen.Tree.FindNode('\Data\\Streams\\' + name1 + '\\Input\\TOTFLOW\\MIXED').value = W
    
    if (aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\B_PRES\\2') != None and
        aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\VAP_FLOW_FRS\\2') != None and
        aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\COND_DUTY') != None and
        aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\B_PRES\\1') != None):
               
    
        Pin  = aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\B_PRES\\2').value
        Fin  = aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\VAP_FLOW_FRS\\2').value
        Qc = aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\COND_DUTY').value
        Ptop = aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\\B_PRES\\1').value
    
        aspen.Tree.FindNode('\Data\\Streams\\' + name2 + '\\Input\\TOTFLOW\\MIXED').value = Fin
        aspen.Tree.FindNode('\Data\\Streams\\' + name2 + '\\Input\\PRES\\MIXED' ).value = Pin
        aspen.Tree.FindNode('\Data\\Blocks\\' + bname2 + '\\Input\\DUTY').value = Qc
        aspen.Tree.FindNode('\Data\\Blocks\\' + bname2 + '\\Input\\PRES').value = Ptop
    
        Comp = ['AA','WATER','PG','T','TT','DAA']
    
        for i in Comp:
            if aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\Y\\2\\' + i) is None:
                aspen.Tree.FindNode('\Data\\Streams\\' + name2 + '\\Input\\FLOW\\MIXED\\' + i).value = 0
            else:
                In = aspen.Tree.FindNode('\Data\\Blocks\\' + bname1 + '\\Output\Y\\2\\' + i).value
                aspen.Tree.FindNode('\Data\\Streams\\' + name2 + '\\Input\\FLOW\\MIXED\\' + i).value = In

        aspen.Engine.Run2()
    
        oname_V = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname2 + "\\#0").value
        FVM     = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname_V +'\\Output\\MASSFLMX\\MIXED').value    
    
    
        if (-P+1)*760 >100:
            CAP  = round(1690*(FVM/0.4536/(-P+1)/760)**0.41*CEPCI/500/1000, 2)
        elif (-P+1)*760 >15: 
            CAP  = round(1690*(FVM/0.4536/(-P+1)/760)**0.41*CEPCI/500*1.8/1000, 2)
        elif (-P+1)*760 >2:
            CAP  = round(1690*(FVM/0.4536/(-P+1)/760)**0.41*CEPCI/500*2.6/1000, 2)
        else:
            CAP  = 10^8    
    
        OPER = round(FVM/0.4536*10*5/1000*8000/1000, 2)
        
    else: 
            CAP  = 10**6
            OPER = 10**6

    return [CAP, OPER]