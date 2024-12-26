import numpy as np

def getvar_reactor(bname, r_time, liq_hold, aspen):
    """
    Args:
        bname (String): Block name
        r_time (Float): Resident time, Batch only (sec)
        liq_hold (Float): Liquid holdup (cubic meter/sec == m3/s)
        aspen (String): Your Aspen Plus file direction

    Returns:
        List: [Volume, Diameter, Inlet temperature, Outlet temperature, Pressure, Duty, Number of tubes]
    """
    type = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\BLKTYPE\\"+ bname).value
    
    if type == "RBATCH":
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        FV = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname + '\\Output\\VOLFLMX\\MIXED').value
        Ti = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ iname + '\\Output\\TEMP_OUT\\MIXED').value
        To = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname + '\\Output\\TEMP_OUT\\MIXED').value
        Q = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').value
        P = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES').value
        V = FV*3600*r_time/liq_hold 
        n = 1 
        M = V
        while M > 75:
          n = n+1
          M = V/n
        V = M
        D = (V*2/3.1415926)**(1/3)
       
    if type == "RPLUG":
        
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        L = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\LENGTH').value
        D = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\DIAM').value
        NTUBE = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\NTUBE').value
         
        P = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES\\MIXED\\1').value
        Ti = aspen.Application.Tree.FindNode('\Data\Streams\\' + iname + '\\Output\\TEMP_OUT\\MIXED').value
        To = aspen.Application.Tree.FindNode('\Data\\Streams\\' + oname + '\\Output\\TEMP_OUT\\MIXED').value
        Q = round(aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').value,0)  
        
        if aspen.Application.Tree.FindNode('\\Data\\Blocks\\' + bname + '\\Input\\CHK_NTUBE').value == "NO":
            V = 3.14159/4*D*D*L
            n = 1
        else:
            n = NTUBE
            V = 3.14159/4*D*D*L*n*2   
            
    if type == "RCSTR":
        iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
        oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
        V = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\TOT_VOL').value
        Ti = aspen.Application.Tree.FindNode('\Data\\Streams\\' + iname + '\\Output\\TEMP_OUT\\MIXED').value
        To = aspen.Application.Tree.FindNode('\Data\\Streams\\' + oname + '\\Output\\TEMP_OUT\\MIXED').value
        Q = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').value
        P = aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname + '\\Output\\B_PRES').value
        n = 1 
        M = V
        while M > 35:
            n = n+1
            M = V/n
        V = M
        D = (V*2/3.1415926)**(1/3)         
    return [V, D, Ti, To, P, Q, n]


def getvar_column(D, name, aspen):
    """
    Args:
        D (Float): Column diameter (meter)
        name (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Volume, Number of Trays, Top temperature, Bot temperature, Condenser duty, Reboiler duty, Pressure] 
    """
    NT = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Input\\NSTAGE').value
    Tt = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\TOP_TEMP').value
    Tb = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\BOTTOM_TEMP').value
    Qc = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\COND_DUTY').ValueForUnit(13, 14)
    Qr = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\REB_DUTY').ValueForUnit(13, 14)
    P = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + name + '\\Output\\B_PRES\\1').ValueForUnit(20, 15)
    V = np.pi/4*float(NT)*0.6*1.2*1.2
    return [V, NT, Tt, Tb, Qc, Qr, P]


def getvar_flash(bname, r_time, aspen):
    """
    Args:
        bname (String): Block name
        r_time (Float): Resident time (Sec). Default: 5 sec
        aspen (Sring): Your Aspen Plus file

    Returns:
        List: [Volume, Diameter, Pessure, Number of vessel]
    """
    oname_V = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    oname_L = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    
    FV1 = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname_V +'\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
    FV2 = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname_L +'\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
    FV = min(FV1,FV2)
    P = aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname +'\Output\B_PRES').ValueForUnit(20, 15)
    V = FV*60*r_time*2
    n = 1
    M = V
    while M > 520:
        n = n+1
        M = V/n
    V = M
    D = (V*2/3.1415926)**(1/3)
    return [V, D, P, n]

def getvar_decanter(bname, r_time, aspen):
    """
    Args:
        bname (String): Block name
        r_time (Float): Resident time (Sec)
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Volume, Diameter, Pessure, Number of vessel]
    """
    FV1 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    FV2 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    P = aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname + '\\Output\\B_PRES').value
    V = (FV1+FV2)*60*r_time
    n = 1 
    M = V
    while M > 628:
        n = n+1
        M = V/n
    V = M
    D = (V*2/3.1415926)**(1/3)
    return [V,D,P,n]

def getvar_exchanger(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Inlet temperature, Outlet temperature, Duty, Pressure] 
    """
    iname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\" + bname + "\\#0").value
    oname = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    Ti = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ iname +'\\Output\\TEMP_OUT\\MIXED').value
    To = aspen.Application.Tree.FindNode('\Data\\Streams\\'+ oname +'\\Output\\TEMP_OUT\\MIXED').value
    Q = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\QCALC').ValueForUnit(13, 14)
    P = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname+'\\Output\\B_PRES').ValueForUnit(20, 15)
    return [Ti, To, Q, P]

def getvar_heatx(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Heat exchanger area, Pressure, Minimum temperature difference] 
    """
    A = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HX_AREAP').value
    P1 = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HOTINP').ValueForUnit(20, 15)
    P2 = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\COLDINP').value
    P3 = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\HOT_PRES').value
    P4 = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\COLD_PRES').value
    P = max([P1,P2,P3,P4])
    
    N = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Input\\NPOINT").Value
    TH_inP = np.empty(shape=N+2)
    TC_inP = np.empty(shape=N+2)
    TH_outP = np.empty(shape=N+2)
    TC_outP = np.empty(shape=N+2)
    Td_inP = np.empty(shape=N+2)
    Td_outP = np.empty(shape=N+2)
    Td_e = np.empty(shape=N+2)
    
    for i in range(N+2):
        TH_inP[i]  = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_HOT\\INLET\\" + str(i+1)).value
        TC_inP[i]  = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_CLD\\INLET\\" + str(i+1)).value
        TH_outP[i] = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_HOT\\OUTLET\\" + str(i+1)).value
        TC_outP[i] = aspen.Application.Tree.FindNode("\\Data\\Blocks\\" + bname + "\\Output\\TEMP_CLD\\OUTLET\\" + str(i+1)).value
        Td_inP[i]  = TH_inP[i] - TC_inP[i]
        Td_outP[i] = TH_outP[i] - TC_outP[i]
        Td_e[i]    = round(Td_inP[i]*(1-i/(N+1)) + Td_outP[i]*(i/(N+1)), 2)
     
    Tmin = min(Td_e)        
    
    return [A, P, Tmin]

def getvar_extractor(bname, oname1, oname2, time, aspen):
    """
    Args:
        bname (String): Block name 
        oname1 (): 
        oname2 (): 
        time (): 
        aspen (String): Your Aspen Plus file 

    Returns:
        List: [Volume, Diameter, Pressure, Number of vessel] 
    """
    FV1 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#0").value
    FV2 = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\" + bname + "\\#1").value
    P = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Output\\B_PRES').value
    NT = aspen.Application.Tree.FindNode('\Data\\Blocks\\' + bname + '\\Input\\NSTAGE').value
    FV_T = (FV1+FV2)*60/(0.3048)^3 

    D = ((FV_T/120*4/3.1415926)**(0.5))*0.3048
    L = (NT*4+3+3)*0.3048 
    V = 3.14159*D*D*L
    n = 1 
    M = V
    while M > 628:
        n = n+1
        M = V/n
    V = M
    D = (V*2/3.1415926)**(1/3)
    return [V, D, P, n]

def getvar_compressor(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        Float: Works (kW) 
    """
    W = aspen.Application.Tree.FindNode('\Data\\Blocks\\'+ bname+ '\\Output\\WNET').value
    return W