import pandas as pd
import matplotlib.pyplot as plt

ChinaUnicom = pd.read_csv("./datas/031/ChinaUnicom.csv")
ChinaUnicom.index = ChinaUnicom.iloc[:,1]
ChinaUnicom.index = pd.to_datetime(ChinaUnicom.index,format="%Y-%m-%d")
ChinaUnicom = ChinaUnicom.iloc[:,2:]

High = ChinaUnicom["High"]
Close = ChinaUnicom["Close"]
Low = ChinaUnicom["Low"]

#设定上下通道线初始值
upboundDC = pd.Series(0.0,index=Close.index)
downboundDC = pd.Series(0.0,index=Close.index)
midboundDC = pd.Series(0.0,index=Close.index)

#求唐奇安上中下通道
for i in range(20,len(Close)):
    upboundDC[i] = max(High[(i-20):i])
    downboundDC[i] = min(Low[(i-20):i])
    midboundDC[i] = 0.5*(upboundDC[i]+downboundDC[i])
upboundDC = upboundDC[20:]
downboundDC = downboundDC[20:]
midboundDC = midboundDC[20:]

#绘制2013年中国联通价格唐奇安通道上中下轨道线图
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.plot(Close["2013"],label="Close",color="k")
plt.plot(upboundDC["2013"],label="upboundDC",color="b",linestyle="dashed")
plt.plot(midboundDC["2013"],label="midboundDC",color="r",linestyle="-.")
plt.plot(downboundDC["2013"],label="downboundDC",color="b",linestyle="dashed")
plt.title("2013年中国联通股价唐奇安通道")
plt.ylim(2.9,3.9)
plt.legend()
# plt.show()

##python捕捉唐奇安通道
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

#唐奇安通道突破策略
UpBreak = upbreak(Close[upboundDC.index[0]:],upboundDC)
DownBreak = downbreak(Close[downboundDC.index[0]:],downboundDC)
BreakSig = UpBreak+DownBreak

#计算获胜率
tradeSig = BreakSig.shift(1)
ret = Close/Close.shift(1)-1
tradeRet = (tradeSig*ret).dropna()
tradeRet[tradeRet==-0]=0
winRate = len(tradeRet[tradeRet>0])/len(tradeRet[tradeRet!=0])
print("20日唐奇安通道预测获胜率:",winRate)

##计算40日唐唐奇安通道策略预测获胜率
upboundDC2 = pd.Series(0.0,index=Close.index)
downboundDC2 = pd.Series(0.0,index=Close.index)
midboundDC2 = pd.Series(0.0,index=Close.index)
for i in range(40,len(Close)):
    upboundDC2[i] = max(High[(i-40):i])
    downboundDC2[i] = min(Low[(i-40):i])
    midboundDC2[i] = 0.5*(upboundDC2[i]+downboundDC2[i])
upboundDC2 = upboundDC2[40:]
downboundDC2 = downboundDC2[40:]
midboundDC2 = midboundDC2[40:]

UpBreak2 = upbreak(Close[upboundDC2.index[0]:],upboundDC2)
DownBreak2 = downbreak(Close[downboundDC2.index[0]:],downboundDC2)
BreakSig2 = UpBreak2+DownBreak2

tradeSig2 = BreakSig2.shift(1)
ret = Close/Close.shift(1)-1
tradeRet2 = (tradeSig2*ret).dropna()
tradeRet2[tradeRet2==-0]=0
winRate2 = len(tradeRet2[tradeRet2>0])/len(tradeRet2[tradeRet2!=0])
print("40日唐奇安通道预测获胜率:",winRate2)
