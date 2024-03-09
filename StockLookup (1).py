#!/home/daddy/anaconda3/bini/python
import os
os.chdir('/home/daddy/Documents/Python/Stocks')
import tkinter as tk

import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import yfinance as yf

#   Add button called daily
#       1. Function
#       2. Button
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
    data= yf.download("SPSC,SNPS,FSLY,OSW,KNSL,APG,NICE,VTI,^GSPC",period="30d")
    return data

def DisplayList():
    print('Lookup All Values')
    txtMyBox.delete("1.0","end")
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

def Sp500():
    print('Look up S&P 500 for 2023')
    data= yf.download("^GSPC",start="2023-01-01",end="2023-12-31")
    dataClose=data['Close']
    myIndex= dataClose.index
    Values = dataClose.loc[str(myIndex[-1])]
    oldValues = dataClose.loc[str(myIndex[0])]
    df = pd.DataFrame( {"Symbol":Values,"Price":Values,"Previous":oldValues})
    dfChange = df["Price"]-df["Previous"]
    df["Change"] = dfChange
    df["Percent"] = 100*dfChange/oldValues
    txtMyBox.insert(tk.END,df)
    return Values

def weekly():
    print('Lookup weekly metrics.')
    data= yf.download("SPSC,SNPS,FSLY,OSW,KNSL,APG,NICE,VTI,^GSPC",period="30d")
    MyMetrics = ['AGG','VEA','^GSPC']
    tickers=yf.Tickers(MyMetrics)
    end_date = dt.datetime.now().strftime('%Y-%m-%d')
    start_date = dt.datetime.now()+dt.timedelta(days=-2)
    tickers_hist =  tickers.history(end=end_date,start=start_date)
    dataClose=tickers_hist['Close']
    myIndex= dataClose.index
    Values = dataClose.loc[str(myIndex[-1])]
    txtMyBox.insert(tk.END,'\n')
    txtMyBox.insert(tk.END,round(Values,2))
    return Values

def LookUpList():
    data= yf.download("SPSC,SNPS,FSLY,OSW,KNSL,APG,NICE,VTI,^GSPC",period="30d")
    return data

def Daily():
    print('Lookup All Values')
    TickersList = ['AGG','VEA','^GSPC']
    txtMyBox.delete("1.0","end")
    ndays = 2
    data= yf.download(TickersList,period="30d")
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


btn_Sp500 = tk.Button(master = frame1, text="S & P 500",command=Sp500)
btn_Sp500.grid(row=0,column=5,sticky="snew")

btn_Weekly= tk.Button(master = frame1, text="Weekly",command=weekly)
btn_Weekly.grid(row=0,column=6,sticky="snew")

btn_Daily= tk.Button(master = frame1, text="Daily",command=Daily)
btn_Daily.grid(row=0,column=7,sticky="snew")
#### Add the text box to frame 2.
txtMyBox = tk.Text(master=frame2)
txtMyBox.grid(row=1,column=0)

def handle_keypress(event):
    """Print the charracter associated ot the key pressed"""
    print(event.char)
    txtMyBox.insert(tk.END,event.char)

window.bind("<Key>",handle_keypress)
 

window.mainloop()
