# Validation functions

# Import modules
import tkinter as tk

# Import globals
import shared

# Numeric keypress only
def validate_numeric(event):
    char = event.char
    if char.isdigit() or char == '\b':
        return
    else:
        return 'break'
    
# Population - If two fields filled in, calculate the third
def validate_population():
    fw = int(shared.fieldWorkersvalue.get())
    dw = int(shared.dykeWorkersvalue.get())
    mi = int(shared.militiavalue.get())

    if((mi == 0 or mi =="") and fw > 0 and dw > 0):
        otherval = shared.turns[-1].Population - fw - dw
        if otherval < 0:
            otherval = 0
        shared.militiavalue.delete(0,tk.END)
        shared.militiavalue.insert(0,otherval)
    elif((fw == 0 or fw =="") and mi > 0 and dw > 0):
        otherval = shared.turns[-1].Population - mi - dw
        if otherval < 0:
            otherval = 0
        shared.fieldWorkersvalue.delete(0,tk.END)
        shared.fieldWorkersvalue.insert(0,otherval)
    elif((dw == 0 or dw =="") and mi > 0 and fw > 0):
        otherval = shared.turns[-1].Population - mi - fw
        if otherval < 0:
            otherval = 0
        shared.dykeWorkersvalue.delete(0,tk.END)
        shared.dykeWorkersvalue.insert(0,otherval)

# Food - validate max allowed at 1000 or however much is left if less than 1000
def validate_planted():
    pl = int(shared.growingvalue.get())
    if(pl > shared.turns[-1].Food and shared.turns[-1].Food <= 1000):
        shared.growingvalue.delete(0,tk.END)
        shared.growingvalue.insert(0,shared.turns[-1].Food)
    elif(pl > 1000):
        shared.growingvalue.delete(0,tk.END)
        shared.growingvalue.insert(0,1000) 

# Submitted Population - validate submitted population not > actual population
def validate_submitted_population(fw,dw,mi):
    return ((fw + dw + mi) <= shared.turns[-1].Population)