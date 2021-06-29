import pandas as pd
import matplotlib.pyplot as plt
import movingAverage as ma

ChinaBank = pd.read_csv("./datas/030/ChinaBank.csv")
ChinaBank.index = ChinaBank.iloc[:,1]
ChinaBank.index = pd.to_datetime(ChinaBank.index,format="%Y-%m-%d")
ChinaBank = ChinaBank.iloc[:,2:]
CBClose = ChinaBank["Close"]

#SMASignal
CBSMA10 = ma.SMAcal(CBClose,10)
SMASignal = pd.Series(0,index=CBClose.index)
for i in range(10,len(CBClose)):
    if all([CBClose[i]>CBSMA10[i],CBSMA10[i-1]>CBClose[i-1]]):
        SMASignal[i] = 1
    elif all([CBClose[i]<CBSMA10[i],CBSMA10[i-1]<CBClose[i-1]]):
        SMASignal[i] = -1

#SLSignal
SSMA5 = ma.SMAcal(CBClose,5)
LSMA30 = ma.SMAcal(CBClose,30)
SLSignal = pd.Series(0,index=LSMA30.index)   #index要挑时期短的index
for i in range(1,len(LSMA30)):
    if all([SSMA5[i]>LSMA30[i],SSMA5[i-1]<LSMA30[i-1]]):
        SLSignal[i] = 1
    elif all([SSMA5[i]<LSMA30[i],SSMA5[i-1]>LSMA30[i-1]]):
        SLSignal[i] = -1

#MACDSignal
DIF = ma.EMAcal(CBClose,12,exponential=2/(1+12))-ma.EMAcal(CBClose,26,exponential=2/(1+26))
DEA = ma.EMAcal(DIF,9,2/(1+9))
MACD = DIF-DEA
MACDSignal = pd.Series(0,index=DIF.index[1:])
for i in range(1,len(DIF)):
    if all([DIF[i]>DEA[i]>0.0,DIF[i-1]<DEA[i-1]]):
        MACDSignal[i]=1
    elif all([DIF[i]<DEA[i]<0.0,DIF[i-1]>DEA[i-1]]):
        MACDSignal[i]=-1

#合并交易信号
ALLSignal = SMASignal+SLSignal+MACDSignal
tradeSig = ALLSignal.shift(1).dropna()

for i in ALLSignal.index:
    if ALLSignal[i]>1:
        ALLSignal[i]=1
    elif ALLSignal[i]<-1:
        ALLSignal[i]=-1
    else:
        ALLSignal[i]=0
Close = CBClose[-1:]
asset = pd.Series(0.0,index=CBClose.index)
cash = pd.Series(0.0,index=CBClose.index)
share = pd.Series(0,index=CBClose.index)

#当价格连续两天上升且交易信号没有显示卖出时，
#第一次开账户持有股票（开户循环）
entry = 3          #从第三天开始
cash[:entry]=20000    #默认现金有20000
while entry<len(CBClose):
    cash[entry]=cash[entry-1]
    if all([CBClose[entry-1]>=CBClose[entry-2],
           CBClose[entry-2]>=CBClose[entry-3],
            ALLSignal[entry-1]!=-1]):
        share[entry]=1000        #每次购买1000股
        cash[entry]=cash[entry]-1000*CBClose[entry]
        break       #当搜索到符合条件的那一天，结束开户循环
    entry+=1

#正式交易循环
i = entry+1
while i<len(CBClose):
    cash[i]=cash[i-1]
    share[i]=share[i-1]
    if ALLSignal[i-1]==1:
        share[i]=share[i]+3000
        cash[i]=cash[i]-3000*CBClose[i]
    if all([ALLSignal[i-1]==-1,share[i]>=1000]):
        share[i]=share[i]-1000
        cash[i]=cash[i]+1000*CBClose[i]
    i+=1

asset=cash+share*CBClose

#绘制交易账户曲线图
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
plt.figure(figsize=(8,8),dpi=80)

plt.subplot(411)
plt.title("2014-2015年上：中国银行均线交易账户")
plt.plot(CBClose,color="b")
plt.ylabel("Price")
plt.subplot(412)
plt.plot(share,color="b")
plt.ylabel("Share")
plt.ylim(0,max(share)+1000)
plt.subplot(413)
plt.plot(asset,color="r")
plt.ylabel("Asset")
plt.ylim(min(asset)-5000,max(asset)+5000)
plt.subplot(414)
plt.plot(cash,color="g")
plt.ylabel("Cash")
plt.ylim(0,max(cash)+5000)
plt.show()

#计算资产收益率
AssetReturn = (asset[-1]-20000)/20000
print(AssetReturn)