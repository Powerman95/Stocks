import tkinter as tk

import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import yfinance as yf

def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"


def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"

def lookup():
    ticker = 'SATS'
    print("SATS lookup requested")
    mystart = dt.datetime(2024,1,20)
    myend = dt.datetime(2024,2,11)
    dishhistory=yf.Ticker(ticker).history(start=mystart,end=myend)
    price=dishhistory['Close'][-1]
    print("SATS download complete")
    txtMyBox.insert(tk.END,str(round(price,2)))
    return price

def LookUpList():
    data= yf.download("SPSC,SNPS,FSLY,OSW,KNSL,APG,NICE,VTI",period="30d")
    return data

def DisplayList():
    print('Lookup All Values')
    ndays = int(lbl_value.cget("text"))
    if(ndays<1):
        ndays = 1
    print(ndays," days")
    data=LookUpList()
    dataClose=data['Close']
    myIndex= dataClose.index
    Values = dataClose.loc[str(myIndex[-1])]
    oldValues = dataClose.loc[str(myIndex[-ndays-1])]
    df = pd.DataFrame( {"Symbol":Values.index,"Price":Values,"Previous":oldValues})
    dfChange = df["Price"]-df["Previous"]
    df["Change"] = dfChange
    df["Percent"] = 100*dfChange/oldValues
    txtMyBox.insert(tk.END,df)
    return Values

window = tk.Tk()

window.rowconfigure([0,1],minsize=50, weight =1)
window.columnconfigure([0,1,2,3],minsize=50,weight=1)

####  Divide the window into 2 frames.  One for buttons. One for text.
frame1=tk.Frame()
frame1.pack()

frame2=tk.Frame()
frame2.pack()

####  Add the buttons to frame 1.
btn_decrease = tk.Button(master=frame1, text = "-",command=decrease)
btn_decrease.grid(row=0,column=0, sticky = "snew")

lbl_value = tk.Label(master=frame1,text = "0")
lbl_value.grid(row=0,column=1)

btn_increase = tk.Button(master = frame1, text="+",command=increase)
btn_increase.grid(row=0,column=2,sticky="snew")

btn_Sats    =   tk.Button(master=frame2,text="SATS",command=lookup)
btn_Sats.grid(row=0,column=3,sticky="snew")

btn_All     =   tk.Button(master=frame1, text="All",command=DisplayList)
btn_All.grid(row=0,column=4,sticky="snew")

#### Add the text box to frame 2.
txtMyBox = tk.Text(master=frame2)
txtMyBox.grid(row=1,column=0)

def handle_keypress(event):
    """Print the charracter associated ot the key pressed"""
    print(event.char)
    txtMyBox.insert(tk.END,event.char)

window.bind("<Key>",handle_keypress)
 

window.mainloop()
