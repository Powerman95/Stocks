#!/home/daddy/anaconda3/bin/python
import os
os.chdir('/home/daddy/Documents/Python/Stocks')
import tkinter as tk
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

# Put a change in and find the diff.
DateTimeFormat = '%Y-%m-%d %H:%M:%S'
DateTimeFormat = '%Y-%m-%d'
#   Add button called daily
#       1. Function
#       2. Button
def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"


def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"

def RandomStock():
    #Choose a stock at random from the csv list.
    df = pd.read_csv('nasdaq.csv')
    nstocks = 10 
    if(nstocks<1):
        value = 1
    else:
        value = int(lbl_value["text"])
    MyRow = df.sample(n=value)
    txtMyBox.delete("1.0","end")
    txtMyBox.insert(tk.END,MyRow)

    df = pd.read_csv('nasdaq.csv')
    MyRow = df.sample(n=nstocks)
    print(MyRow)
    BackTestStart ='2005-01-01'
    BackTestStop ='2015-01-01'
    StockList = MyRow['Symbol'].values.tolist()

    df2 = yf.download(StockList,period='max',group_by='ticker')
    for ticker in StockList:
        OneStock = df2[ticker].dropna()
        bt = Backtest(OneStock, SmaCross,
        cash = 10000, commission=0.002,exclusive_orders=True)
        output = bt.run()
        bt.plot()
#        return(MyRow)

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
    print("Close Data Collected")
    myIndex= dataClose.index
    Values = dataClose.loc[str(myIndex[-1])]
    OldValues = dataClose.loc[str(myIndex[0])]
    df = pd.DataFrame( {"Symbol":Values,"Price":Values,"Previous":OldValues})
    dfChange = df["Price"]-df["Previous"]
    df["Change"] = dfChange
    df["Percent"] = 100*dfChange/OldValues
    txtMyBox.insert(tk.END,df)
    return Values

def weekly():   #Compare the latest close to that of last Friday.
#get today
#subtract weekday to get monday
#subract 3 to get previous Friday.
#set start date at last Friday.
#get data.  prices today [-1] and last Friday [0]
    today = dt.datetime.now()
    LastFriday = today+dt.timedelta(days=-dt.datetime.weekday(today)-3)
    EndDate = dt.datetime.strftime(today,format=DateTimeFormat)
    StartDate = dt.datetime.strftime(LastFriday,format=DateTimeFormat)
    print('Lookup weekly metrics.')
    WatchList = ["VTI","VXUS","AGG","VEA","^GSPC"]
    data= yf.download(WatchList,start=StartDate,end=EndDate)
    
    dataClose=data['Close']
    myIndex= dataClose.index
    Values = dataClose.loc[str(myIndex[-1])]    #Closing values on the last date of the dataset.
    OldValues = dataClose.loc[str(myIndex[0])]  #Closing values on the first date of the dataset.
    
    df = pd.DataFrame( {"Price":Values,"Previous":OldValues})
    dfChange = df["Price"]-df["Previous"]
    
    df["Change"] = dfChange
    df["Percent"] = 100*dfChange/OldValues

    txtMyBox.delete("1.0","end")
    txtMyBox.insert(tk.END,df.round(2))
    return Values

def LookUpList():
    data= yf.download("SPSC,SNPS,FSLY,OSW,KNSL,APG,NICE,VTI,^GSPC",period="30d")
    return data

def Daily():
    print('Lookup All Values')
    TickersList = ['AGG','VEA','^GSPC','VXUS','RCL','^DJI']
    txtMyBox.delete("1.0","end")
    ndays = 2
    tickers = yf.Tickers(TickersList)
    Bids    = []
    Asks    = []
    Close   = []
    for tick in tickers.tickers:
        Bids.append(tickers.tickers[tick].info['bid'])
        Asks.append(tickers.tickers[tick].info['ask'])
        Close.append(tickers.tickers[tick].info['previousClose'])
    df = pd.DataFrame(TickersList,columns=['Symbol'])
    df['Price']=Bids
    df['Ask']=Asks
    df['Previous']=Close
    dfChange = df["Price"]-df["Previous"]
    df["Change"] = dfChange
    df["Percent"] = 100*dfChange/df['Previous']
    txtMyBox.insert(tk.END,df)
    return  Bids 

class SmaCross(Strategy):
    n1 = 10
    n2 = 20
    
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

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
class SmaCross(Strategy):
    n1 = 10
    n2 = 20
    
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()
    n1 = 10
    n2 = 20
    
    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


btn_Sp500 = tk.Button(master = frame1, text="S & P 500",command=Sp500)
btn_Sp500.grid(row=0,column=5,sticky="snew")

btn_Weekly= tk.Button(master = frame1, text="Weekly",command=weekly)
btn_Weekly.grid(row=0,column=6,sticky="snew")

btn_Daily= tk.Button(master = frame1, text="Daily",command=Daily)
btn_Daily.grid(row=0,column=7,sticky="snew")

btn_Random = tk.Button(master = frame1, text="Random",command=RandomStock)
btn_Random.grid(row=0,column=8,sticky="snew")

#### Add the text box to frame 2.
txtMyBox = tk.Text(master=frame2)
txtMyBox.grid(row=1,column=0)

def handle_keypress(event):
    """Print the charracter associated ot the key pressed"""
    print(event.char)
    txtMyBox.insert(tk.END,event.char)

window.bind("<Key>",handle_keypress)
 

window.mainloop()
