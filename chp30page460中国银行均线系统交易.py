import pandas as pd
import numpy as np
import movingAverage as ma
import matplotlib.pyplot as plt

ChinaBank = pd.read_csv("./datas/030/ChinaBank.csv")
ChinaBank.index = ChinaBank.iloc[:,1]
ChinaBank.index = pd.to_datetime(ChinaBank.index,format="%Y-%m-%d")
ChinaBank = ChinaBank.iloc[:,2:]

CBClose = ChinaBank["Close"]

CBSMA10 = ma.SMAcal(CBClose,10)
SMASignal = pd.Series(0,index=CBClose.index)
for i in range(10,len(CBClose)):
    if all([CBClose[i]>CBSMA10[i],CBSMA10[i-1]>CBClose[i-1]]):
        SMASignal[i] = 1
    elif all([CBClose[i]<CBSMA10[i],CBSMA10[i-1]<CBClose[i-1]]):
        SMASignal[i] = -1

SMAtrade = SMASignal.shift(1).dropna()
SMAbuy = SMAtrade[SMAtrade==1]
SMAsell = SMAtrade[SMAtrade==-1]

#计算单期日收益率
CBRet = CBClose/CBClose.shift(1)-1
SMARet = (CBRet*SMAtrade).dropna()

#累计收益率表现
cumStock = np.cumprod(1+CBRet)-1
cumTrade = np.cumprod(1+SMARet)-1

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
plt.plot(cumStock,label="cumStock",color="k")
plt.plot(cumTrade,label="cumTrade",color="r",linestyle=":")
plt.title("股票本身与均线交易的累计收益率")
plt.legend()
# plt.show()

#求买卖点预测准确率
SMARet[SMARet==-0] = 0
SMAWinrate = len(SMARet[SMARet>0])/len(SMARet[SMARet!=0])
print(SMAWinrate)   #结果显示正确率很低








