import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#布林带通道函数
def bbands(tsPrice,period=20,times=2):
    upBBand = pd.Series(0.0,index=tsPrice.index)
    midBBand = pd.Series(0.0,index=tsPrice.index)
    downBBand = pd.Series(0.0,index=tsPrice.index)
    sigma = pd.Series(0.0,index=tsPrice.index)
    for i in range(period-1,len(tsPrice)):
        midBBand[i] = np.nanmean(tsPrice[(i-period+1):(i+1)])
        sigma[i] = np.nanstd(tsPrice[(i-period+1):(i+1)])
        upBBand[i] = midBBand[i] + times*sigma[i]
        downBBand[i] = midBBand[i] - times*sigma[i]
    BBands = pd.DataFrame({"upBBand":upBBand[(period-1):],
                           "midBBand":midBBand[(period-1):],
                           "downBBand":downBBand[(period-1):],
                           "sigma":sigma[(period-1):]})
    return (BBands)

ChinaUnicom = pd.read_csv("./datas/031/ChinaUnicom.csv")
ChinaUnicom.index = ChinaUnicom.iloc[:,1]
ChinaUnicom.index = pd.to_datetime(ChinaUnicom.index,format="%Y-%m-%d")
ChinaUnicom = ChinaUnicom.iloc[:,2:]
Close = ChinaUnicom["Close"]

CHNUnicomBBands = bbands(Close,20,2)
UpDownBB = CHNUnicomBBands.loc[:,["downBBand","upBBand"]]
UpDownBB13 = UpDownBB["2013"]
UpDownBB13.plot()
plt.plot(Close["2013"],label="Close")
plt.legend()
# plt.show()

import candle
candle.candle(StockData=ChinaUnicom["2013-01":"2013-06"],candleTitle="蜡烛图")
plt.show()

#构造布林带风险函数CalBollRisk()
def CalBollRisk(tsPrice,multiplier):
    k = len(multiplier)
    BollRisk = []
    for i in range(k):
        BBands = bbands(tsPrice,20,multiplier[i])
        a = 0
        b = 0
        for j in range(len(BBands)):
            tsPrice = tsPrice[-(len(BBands)):]
            if tsPrice[j]>BBands["upBBand"][j]:
                a+=1
            elif tsPrice[j]<BBands["downBBand"][j]:
                b+=1
        BollRisk.append(100*(a+b)/len(BBands))
    return (BollRisk)

multiplier=[1,1.65,1.96,2,2.58]
price2010 = Close["2010-01-04":"2010-12-31"]

##一般布林带上下通道突破策略
BBands = bbands(Close,20,2)

#upbreak()函数
def upbreak(price,upbound):
    n = min(len(price),len(upbound))
    tsLine = price[-n:]
    tsRefLine = upbound[-n:]
    signal = pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]>tsRefLine[i],tsLine[i-1]<tsRefLine[i-1]]):
            signal[i]=1
    return (signal)
#downbreak()函数
def downbreak(price,downbound):
    n = min(len(price),len(downbound))
    tsLine = price[-n:]
    tsRefLine = downbound[-n:]
    signal = pd.Series(0,index=tsLine.index)
    for i in range(1,len(tsLine)):
        if all([tsLine[i]<tsRefLine[i],tsLine[i-1]>tsRefLine[i-1]]):
            signal[i]=-1
    return (signal)

upbreakBB1 = upbreak(Close,BBands["upBBand"])
downbreakBB1 = downbreak(Close,BBands["downBBand"])

#每条信号出现2天后进行交易
upBBSig1 = -upbreakBB1.shift(2)
downBBSig1 = -downbreakBB1.shift(2)

tradeSignal1 = upBBSig1+downBBSig1
tradeSignal1[tradeSignal1==-0]=0

#构造评价函数
def perform(price,signal):
    ret = price/price.shift(1)-1
    tradeRet = (ret*signal).dropna()
    ret = ret[-len(tradeRet):]
    winRate = [len(ret[ret>0])/len(ret[ret!=0]),len(tradeRet[tradeRet>0])/len(tradeRet[tradeRet!=0])]
    meanWin = [np.mean(ret[ret>0]),np.mean(tradeRet[tradeRet>0])]
    meanloss = [np.mean(ret[ret<0]),np.mean(tradeRet[tradeRet<0])]
    Performance = pd.DataFrame({"winRate":winRate,
                                "meanWin":meanWin,
                                "meanloss":meanloss})
    Performance.index = ["Stock","Trade"]
    return (Performance)

Performance1 = perform(Close,tradeSignal1)
print(Performance1)

##特殊布林带通道突破策略
upbreakBB2 = upbreak(Close,BBands["downBBand"])
downbreakBB2 = downbreak(Close,BBands["upBBand"])

upBBSig2 = upbreakBB2.shift(2)
downBBSig2 = -downbreakBB2.shift(2)
tradeSignal2 = upbreakBB2+downBBSig2
tradeSignal2[tradeSignal2==-0]=0

Performance2 = perform(Close,tradeSignal2)
print(Performance2)