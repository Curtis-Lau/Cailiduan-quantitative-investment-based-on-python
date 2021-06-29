import movingAverage as ma
import pandas as pd
import matplotlib.pyplot as plt

ChinaBank = pd.read_csv("./datas/030/ChinaBank.csv")
ChinaBank.index = ChinaBank.iloc[:,1]
ChinaBank.index = pd.to_datetime(ChinaBank.index,format="%Y-%m-%d")
ChinaBank = ChinaBank.iloc[:,2:]

CBClose = ChinaBank["Close"]

DIF = ma.EMAcal(CBClose,12,exponential=2/(1+12))-ma.EMAcal(CBClose,26,exponential=2/(1+26))
DEA = ma.EMAcal(DIF,9,2/(1+9))
MACD = DIF-DEA

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.figure(figsize=(10,5),dpi=80)

plt.subplot(211)
plt.plot(DIF["2015"],label="DIF",color="k")
plt.plot(DEA["2015"],label="DEA",color="b",linestyle="dashed")
plt.title("信号线DIF与DEA")
plt.legend()

plt.subplot(212)
plt.bar(MACD["2015"].index,MACD["2015"],label="MACD",color="r")
plt.legend()
# plt.show()

MACDSignal = pd.Series(0,index=DIF.index[1:])
for i in range(1,len(DIF)):
    if all([DIF[i]>DEA[i]>0.0,DIF[i-1]<DEA[i-1]]):
        MACDSignal[i]=1
    elif all([DIF[i]<DEA[i]<0.0,DIF[i-1]>DEA[i-1]]):
        MACDSignal[i]=-1
MACDTrade = MACDSignal.shift(1)
CBRet = CBClose/CBClose.shift(1)-1
MACDRet = (CBRet*MACDTrade).dropna()
MACDRet[MACDRet==-0]=0
MACDwinRet = len(MACDRet[MACDRet>0])/len(MACDRet[MACDRet!=0])
# print(MACDwinRet)



