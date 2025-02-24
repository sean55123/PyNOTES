import numpy as np
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        type_node = aspen.Application.Tree.FindNode("\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\BLKTYPE\\" + bname)
        if type_node is None:
            logging.error(f"BLKTYPE node not found for block: {bname}")
            return None
        type = type_node.value

        if type == "RBATCH":
            try:
                iname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\{bname}\\#0").value
                oname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").value
                FV = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname}\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
                Ti = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{iname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                To = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                Q = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\QCALC').ValueForUnit(13, 14)
                P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
                V = FV * 3600 * r_time / liq_hold 
                n = 1 
                M = V
                while M > 75:
                    n += 1
                    M = V / n
                V = M
                D = (V * 2 / np.pi) ** (1/3)
            except AttributeError as e:
                logging.error(f"Error processing RBATCH block '{bname}': {e}")
                return None

        elif type == "RPLUG":
            try:
                iname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\{bname}\\#0").value
                oname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").value
                L = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Input\\LENGTH').ValueForUnit(17, 1)
                D = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Input\\DIAM').ValueForUnit(17, 1)
                NTUBE = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Input\\NTUBE').value

                P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES\\MIXED\\1').ValueForUnit(20, 15)
                Ti = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{iname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                To = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                Q = round(aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\QCALC').ValueForUnit(13, 14), 0)  

                chk_ntube = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Input\\CHK_NTUBE')
                if chk_ntube and chk_ntube.value == "NO":
                    V = np.pi / 4 * D * D * L
                    n = 1
                else:
                    n = NTUBE
                    V = np.pi / 4 * D * D * L * n * 2
            except AttributeError as e:
                logging.error(f"Error processing RPLUG block '{bname}': {e}")
                return None

        elif type == "RCSTR":
            try:
                iname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\{bname}\\#0").value
                oname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").value
                V = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\TOT_VOL').ValueForUnit(27, 1)
                Ti = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{iname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                To = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
                Q = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\QCALC').ValueForUnit(13, 14)
                P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
                n = 1 
                M = V
                while M > 35:
                    n += 1
                    M = V / n
                V = M
                D = (V * 2 / np.pi) ** (1/3)  
            except AttributeError as e:
                logging.error(f"Error processing RCSTR block '{bname}': {e}")
                return None

        else:
            logging.error(f"Unknown block type '{type}' for block '{bname}'")
            return None

        return [V, D, Ti, To, P, Q, n]

    except Exception as e:
        logging.error(f"Unexpected error in getvar_reactor for block '{bname}': {e}")
        return None


def getvar_column(D, name, aspen):
    """
    Args:
        D (Float): Column diameter (meter)
        name (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Volume, Number of Trays, Top temperature, Bot temperature, Condenser duty, Reboiler duty, Pressure] 
    """
    try:
        NT = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Input\\NSTAGE').value
        Tt = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Output\\TOP_TEMP').ValueForUnit(22, 4)
        Tb = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Output\\BOTTOM_TEMP').ValueForUnit(22, 4)
        Qc = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Output\\COND_DUTY').ValueForUnit(13, 14)
        Qr = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Output\\REB_DUTY').ValueForUnit(13, 14)
        P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{name}\\Output\\B_PRES\\1').ValueForUnit(20, 15)
        V = np.pi / 4 * float(NT) * 0.6 * 1.2 * 1.2
        return [V, NT, Tt, Tb, Qc, Qr, P]
    except AttributeError as e:
        logging.error(f"Error processing column block '{name}': {e}")
        return None
    except ValueError as e:
        logging.error(f"Value conversion error in column block '{name}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_column for block '{name}': {e}")
        return None


def getvar_flash(bname, r_time, aspen):
    """
    Args:
        bname (String): Block name
        r_time (Float): Resident time (Sec). Default: 5 sec
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Volume, Diameter, Pressure, Number of vessel]
    """
    try:
        oname_V = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").value
        oname_L = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#1").value

        FV1 = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname_V}\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
        FV2 = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname_L}\\Output\\VOLFLMX\\MIXED').ValueForUnit(12, 1)
        FV = min(FV1, FV2)
        P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
        V = FV * 60 * r_time * 2
        n = 1
        M = V
        while M > 520:
            n += 1
            M = V / n
        V = M
        D = (V * 2 / np.pi) ** (1/3)
        return [V, D, P, n]
    except AttributeError as e:
        logging.error(f"Error processing flash block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_flash for block '{bname}': {e}")
        return None


def getvar_decanter(bname, r_time, aspen):
    """
    Args:
        bname (String): Block name
        r_time (Float): Resident time (Sec)
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Volume, Diameter, Pressure, Number of vessel]
    """
    try:
        FV1 = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").ValueForUnit(12, 1)
        FV2 = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#1").ValueForUnit(12, 1)
        P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
        V = (FV1 + FV2) * 60 * r_time
        n = 1 
        M = V
        while M > 628:
            n += 1
            M = V / n
        V = M
        D = (V * 2 / np.pi) ** (1/3)
        return [V, D, P, n]
    except AttributeError as e:
        logging.error(f"Error processing decanter block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_decanter for block '{bname}': {e}")
        return None


def getvar_exchanger(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Inlet temperature, Outlet temperature, Duty, Pressure] 
    """
    try:
        iname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\INSTRM\\{bname}\\#0").value
        oname = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").value
        Ti = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{iname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        To = aspen.Application.Tree.FindNode(f'\\Data\\Streams\\{oname}\\Output\\TEMP_OUT\\MIXED').ValueForUnit(22, 4)
        Q = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\QCALC').ValueForUnit(13, 14)
        P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
        return [Ti, To, Q, P]
    except AttributeError as e:
        logging.error(f"Error processing exchanger block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_exchanger for block '{bname}': {e}")
        return None


def getvar_heatx(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        List: [Heat exchanger area, Pressure, Minimum temperature difference] 
    """
    try:
        A = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\HX_AREAP').ValueForUnit(1, 1)
        P1 = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\HOTINP').ValueForUnit(20, 15)
        P2 = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\COLDINP').ValueForUnit(20, 15)
        P3 = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\HOT_PRES').ValueForUnit(20, 15)
        P4 = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\COLD_PRES').ValueForUnit(20, 15)
        P = max([P1, P2, P3, P4])

        N = aspen.Application.Tree.FindNode(f"\\Data\\Blocks\\{bname}\\Input\\NPOINT").Value
        TH_inP = np.empty(shape=N+2)
        TC_inP = np.empty(shape=N+2)
        TH_outP = np.empty(shape=N+2)
        TC_outP = np.empty(shape=N+2)
        Td_inP = np.empty(shape=N+2)
        Td_outP = np.empty(shape=N+2)
        Td_e = np.empty(shape=N+2)

        for i in range(N+2):
            try:
                TH_inP[i]  = aspen.Application.Tree.FindNode(f"\\Data\\Blocks\\{bname}\\Output\\TEMP_HOT\\INLET\\{i+1}").ValueForUnit(22, 4)
                TC_inP[i]  = aspen.Application.Tree.FindNode(f"\\Data\\Blocks\\{bname}\\Output\\TEMP_CLD\\INLET\\{i+1}").ValueForUnit(22, 4)
                TH_outP[i] = aspen.Application.Tree.FindNode(f"\\Data\\Blocks\\{bname}\\Output\\TEMP_HOT\\OUTLET\\{i+1}").ValueForUnit(22, 4)
                TC_outP[i] = aspen.Application.Tree.FindNode(f"\\Data\\Blocks\\{bname}\\Output\\TEMP_CLD\\OUTLET\\{i+1}").ValueForUnit(22, 4)
                Td_inP[i]  = TH_inP[i] - TC_inP[i]
                Td_outP[i] = TH_outP[i] - TC_outP[i]
                Td_e[i]    = round(Td_inP[i] * (1 - i / (N + 1)) + Td_outP[i] * (i / (N + 1)), 2)
            except AttributeError as e:
                logging.error(f"Error processing temperature points in heat exchanger '{bname}': {e}")
                Td_e[i] = np.nan  # Assign NaN or another placeholder

        Tmin = np.nanmin(Td_e)  # Use nanmin to ignore NaNs
        return [A, P, Tmin]
    except AttributeError as e:
        logging.error(f"Error processing heat exchanger block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_heatx for block '{bname}': {e}")
        return None


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
    try:
        FV1 = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#0").ValueForUnit(12, 1)
        FV2 = aspen.Application.Tree.FindNode(f"\\Data\\Flowsheet\\Section\\GLOBAL\\Input\\OUTSTRM\\{bname}\\#1").ValueForUnit(12, 1)
        P = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\B_PRES').ValueForUnit(20, 15)
        NT = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Input\\NSTAGE').value
        FV_T = (FV1 + FV2) * 60 / (0.3048 ** 3)

        D = ((FV_T / 120 * 4 / np.pi) ** 0.5) * 0.3048
        L = (NT * 4 + 3 + 3) * 0.3048 
        V = np.pi * D * D * L
        n = 1 
        M = V
        while M > 628:
            n += 1
            M = V / n
        V = M
        D = (V * 2 / np.pi) ** (1/3)
        return [V, D, P, n]
    except AttributeError as e:
        logging.error(f"Error processing extractor block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_extractor for block '{bname}': {e}")
        return None


def getvar_compressor(bname, aspen):
    """
    Args:
        bname (String): Block name
        aspen (String): Your Aspen Plus file

    Returns:
        Float: Works (kW) 
    """
    try:
        W = aspen.Application.Tree.FindNode(f'\\Data\\Blocks\\{bname}\\Output\\WNET').ValueForUnit(13, 14)
        return W
    except AttributeError as e:
        logging.error(f"Error processing compressor block '{bname}': {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in getvar_compressor for block '{bname}': {e}")
        return None
