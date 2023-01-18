from tkinter import *

"""Code for the Calculator, supports basic operation, square root and power as well as an history for operations (may have some hidden bugs tho)"""

#Creates the main window
mainWindow = Tk()
mainWindow.geometry("375x620")
mainWindow.title("Calculator9000")

#Two frames, one for the expression the results and another one for the buttons (the button works as a grid)
exprFrame = Frame(mainWindow, height=200)
exprFrame.pack(expand=True, fill="both")
buttonFrame = Frame(mainWindow)
buttonFrame.pack(expand=True, fill="both")
buttonFrame.rowconfigure(0, weight=1)
for i in range(1, 5):
    buttonFrame.rowconfigure(i, weight=1)
    buttonFrame.columnconfigure(i, weight=1)

#The actual data of both the result and the expression
totalExpr = ""
currentExpr = ""

#History is managed with a list, it gets reset when you re-open the program
history = []
back = 1

#Digits and their coordinates in the buttonFrame
digits = {
    7: (1, 1), 8: (1, 2), 9: (1, 3),
    4: (2, 1), 5: (2, 2), 6: (2, 3),    
    1: (3, 1), 2: (3, 2), 3: (3, 3),
    0: (4, 2), '.': (4, 1)
}
#Operators dictionnary
operators = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

#Creates the label for the result and the expression ('total' and 'current')
def ExprLabels():
    totalLab = Label(exprFrame, text=totalExpr, anchor=E, padx=24)
    totalLab.pack(expand=True, fill="both")
    currentLab = Label(exprFrame, text=currentExpr, anchor=E, font=("Arial", 20, "bold"), padx=24)
    currentLab.pack(expand=True, fill="both")
    return totalLab, currentLab

total, current = ExprLabels()

#Function that adds the digit pressed to the expression
def AddToExpression(value):
    global currentExpr
    currentExpr += str(value)
    LabelUpdate()

#Adds the operator, it clears the current expression (result label) for clarity
def AddOperator(operator):
    global currentExpr, totalExpr
    totalExpr += currentExpr + operator
    currentExpr = ""
    print(totalExpr)
    TotalUpdate()
    LabelUpdate()

#Define the sign of the current operation
def DefSign():
    global currentExpr
    if currentExpr.isalnum():
        currentExpr = "(-" + currentExpr + ")"
    else:
        currentExpr = currentExpr[2:len(currentExpr)-1]
    LabelUpdate()

#Handles square root
def SqrtSign():
    global currentExpr
    currentExpr = str(eval(f"{currentExpr}**0.5"))
    LabelUpdate()

#Handles pow, works the same as the operators function but somehow bugged when trying to configure it with the same function, it now works anyways with this function :D
def PowSign():
    global currentExpr, totalExpr
    totalExpr = currentExpr + "**"
    currentExpr = ""
    TotalUpdate()
    LabelUpdate()

#Handles the action of the history button, basically goes back in the list to print it on the expression
def DisplayHistory():
    global totalExpr, back
    if back <= len(history):
        totalExpr = history[len(history)-back]
        back += 1
        TotalUpdate()

#Updates the current expression label
def LabelUpdate():
    global current
    current.config(text=currentExpr)

# "    " total expression label
def TotalUpdate():
    global total, totalExpr, currentExpr
    total.config(text=totalExpr)

#Functions that prints the result of the expression, used with the equal button
def Eval():
    global totalExpr, currentExpr
    totalExpr += currentExpr
    TotalUpdate()
    try:
        currentExpr = str(eval(totalExpr))
        totalExpr = ""
    except:
        currentExpr = "Error"
    finally:
        LabelUpdate()

#Clears the expression and adds it to the history
def Clear():
    global totalExpr, currentExpr, history
    if total.cget("text") != "":
        history.append(total.cget("text"))
    totalExpr = ""
    currentExpr = ""
    LabelUpdate()
    TotalUpdate()

#Creates the buttons for the digits, goes through a loop and asign at each button its text and its coordinates in the buttonFrame
"""A Lambda function is used here, being an anonymous function it saves us from declaring another function (it's too simple to require another declared function), on top of that it is convenient to use in a loop since our command depends on just an iterable"""
def DigitButtons():
    for digit, coordinates in digits.items():
        digitButton = Button(buttonFrame, text=str(digit), font=("Arial", 20), borderwidth=0.5, command=lambda x=digit:AddToExpression(x)).grid(row=coordinates[0], column=coordinates[1], sticky=NSEW)

#Creates all the operators and utility buttons
"""Lambda function here as well"""
def OperatorButtons():
    i = 0
    for operator, symbol in operators.items():
        button = Button(buttonFrame, text=symbol, font=("Arial", 15), command=lambda x=operator:AddOperator(x)).grid(row=i, column=4, sticky=NSEW)
        i += 1
    equalButton = Button(buttonFrame, text="=", font=("Arial", 15), command=Eval).grid(row=4, column=4, sticky=NSEW)
    signButton = Button(buttonFrame, text="+/-", font=("Arial", 15), command=DefSign).grid(row=4, column=3, sticky=NSEW)
    powButton = Button(buttonFrame, text="x^", font=("Arial", 15), command=PowSign).grid(row=0, column=2, sticky=NSEW)
    sqrtButton = Button(buttonFrame, text="\u221a", font=("Arial", 15), command=SqrtSign).grid(row=0, column=3, sticky=NSEW)
    clearButton = Button(buttonFrame, text="C", font=("Arial", 20, "bold"), command=Clear).grid(row=0, column=1, sticky=NSEW)

def CalcHistoryButton():
    button = Button(exprFrame, text="Previous Operations", command=DisplayHistory, font=("Arial", 10, "bold"), anchor=CENTER, padx=24)
    button.pack(expand=True, fill="both")

def main():
    CalcHistoryButton()
    DigitButtons()
    OperatorButtons()
    mainWindow.mainloop()





if __name__ == "__main__":
    main()

