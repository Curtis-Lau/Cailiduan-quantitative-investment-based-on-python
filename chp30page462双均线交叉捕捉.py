import pandas as pd
import numpy as np
import movingAverage as ma
import matplotlib.pyplot as plt

ChinaBank = pd.read_csv("./datas/030/ChinaBank.csv")
ChinaBank.index = ChinaBank.iloc[:,1]
ChinaBank.index = pd.to_datetime(ChinaBank.index,format="%Y-%m-%d")
ChinaBank = ChinaBank.iloc[:,2:]

CBClose = ChinaBank["Close"]

#计算5日、30日SMA
SSMA5 = ma.SMAcal(CBClose,5)
LSMA30 = ma.SMAcal(CBClose,30)
SLSignal = pd.Series(0,index=LSMA30.index)   #index要挑时期短的index
for i in range(1,len(LSMA30)):
    if all([SSMA5[i]>LSMA30[i],SSMA5[i-1]<LSMA30[i-1]]):
        SLSignal[i] = 1
    elif all([SSMA5[i]<LSMA30[i],SSMA5[i-1]>LSMA30[i-1]]):
        SLSignal[i] = -1

SLtrade = SLSignal.shift(1)
CBRet = CBClose/CBClose.shift(1)-1

#Long表示buy
Long = pd.Series(0,index=LSMA30.index)
Long[SLtrade==1] = 1
LongRet = (Long*CBRet).dropna()
winLrate = len(LongRet[LongRet>0])/len(LongRet[LongRet!=0])

#Short表示Sell
Short = pd.Series(0,index=LSMA30.index)
Short[SLtrade==-1] = -1
ShortRet = (Short*CBRet).dropna()
winSrate = len(ShortRet[ShortRet>0])/len(ShortRet[ShortRet!=0])

#计算所有买卖点的预测获胜率
SLtradeRet = (SLtrade*CBRet).dropna()
winRate = len(SLtradeRet[SLtradeRet>0])/len(SLtradeRet[SLtradeRet!=0])
# print(winRate)

cumLong = np.cumprod(1+LongRet)-1
cumShort = np.cumprod(1+ShortRet)-1
cumSLtrade = np.cumprod(1+SLtradeRet)-1

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.plot(cumSLtrade,label="cumSLtrade",color="k")
plt.plot(cumLong,label="cumShort",color="b",linestyle="dashed")
plt.plot(cumShort,label="cumLong",color="r",linestyle=":")
plt.title("长短期均线交易累计收益率")
plt.legend(loc="best")
plt.show()

