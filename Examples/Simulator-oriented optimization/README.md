# Example for simulator-based single objective optimization
For Simulator-based optimiation, you have to call your simulator in objective function.
In this example a process optimization taking TAC as objective is used as example.

Noted!! Setting.py can be used to input variables to Aspen Plus, checking result status, and calculate objective function.

The link2apsen() function can help you link Aspen with Python.
All you need to change is the name of the file and the dispatch number for specific Aspen dispatch.

Aspen V11 -> 37.0

Aspen V12 -> 38.0

Asepn V12.1 -> 39.0

Aspen V14 -> 40.0

```python
import Pynotes.Setting as set

def objective_function(x):
    global filepath
    aspen, filepath = link2aspen('YourAspenFile.apw')
    set.var_input(x, aspen)
    status = set.get_status()
    if status == 0:
        obj = set.TAC_cal(aspen)
        obj = [obj, status]
    else:
        obj = [10e7, status]
        aspen.close()
        aspen.quit()
        time.sleep(0.5)
        aspen, filepath = link2aspen('YourAspenFile.apw')
    return obj
```
For simulator-base optimization with self-defined objective function.
```python
def objective_function(x):
    global filepath
    aspen, filepath = link2aspen('YourAspenFile.apw')
    set.var_input(x, aspen)
    status = set.get_status()
    if status == 0:
        obj = set.Cal_obj(aspen)
    else:
        obj = 10e7
        aspen.close()
        aspen.quit()
        time.sleep(0.5)
        aspen, filepath = link2aspen('YourAspenFile.apw')
    return obj
```
Use the get_status() in setting.py to check the status of simulator.

### It is crucial to control the result of simulator
Remeber to change the description of status in setting.py!!!
```python
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
```
Finally, use the Aspen_saving() function to save the final result.
```python
aspen = link2aspen('YourAspenFile.apw')[0]
set.Aspen_saving(cost_t, aspen, params, filepath, 'Results')
```