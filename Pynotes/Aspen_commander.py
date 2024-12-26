import win32com.client as win32 
import os

def link2aspen(Aspen_file, Visible=0, SuppressDialogs=1, Dispatch=37):
    filepath = os.path.join(os.path.abspath('.'), Aspen_file)
    aspen = win32.Dispatch('Apwn.Document.37.0') # 40.0 for Aspen V14
    aspen.InitFromFile2(filepath)
    aspen.Visible = 0
    aspen.SuppressDialogs = 1
    return aspen, filepath

