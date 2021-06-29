import pandas as pd
import numpy as np

def SMAcal(price,period):
    SMA = pd.Series(0.0,index=price.index)
    for i in range(period-1,len(price)):
        SMA[i] = np.mean(price[(i-period+1):(i+1)])
    return (SMA)

def WMAcal(price,weight):
    period = len(weight)
    arrWeight = np.array(weight)
    WMA = pd.Series(0.0,index=price.index)
    for i in range(period-1,len(price)):
        WMA[i] = sum(arrWeight*price[(i-period+1):(i+1)])
    return (WMA)

def EMAcal(price,period=5,exponential=0.2):
    EMA = pd.Series(0.0,index=price.index)
    EMA[period-1] = np.mean(price[:period])
    for i in range(period,len(price)):
        EMA[i] = exponential*price[i] + (1-exponential)*EMA[i-1]
    return (EMA)
