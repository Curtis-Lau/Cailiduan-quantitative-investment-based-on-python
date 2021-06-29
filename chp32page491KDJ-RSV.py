import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

GSPC = pd.read_csv("./datas/032/GSPC.csv",index_col="Date")
GSPC = GSPC.iloc[:,1:]
GSPC.index = pd.to_datetime(GSPC.index)

close = GSPC['Close']
high = GSPC['High']
low = GSPC['Low']

date = GSPC.index.to_series()
ndate = len(date)

periodHigh = pd.Series(np.zeros(ndate-8),index=date.index[8:])
periodLow = pd.Series(np.zeros(ndate-8),index=date.index[8:])

RSV = pd.Series(np.zeros(ndate-8),index=date.index[8:])

for j in range(8,ndate):
    period = date[j-8:j+1]
    i = date[j]
    periodHigh[i] = high[period].max()
    periodLow[i] = low[period].min()
    RSV[i] = 100*(close[i]-periodLow[i])/(periodHigh[i]-periodLow[i])
    periodHigh.name = "periodHigh"
    periodLow.name = "periodLow"
    RSV.name = "RSV"

close1 = close['2015']
RSV1 = RSV['2015']
C_RSV = pd.DataFrame([close1,RSV1]).T
C_RSV.plot(subplots=True,title="标普指数2015年未成熟随机指标RSV")
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.show()

# RSV1 = pd.Series([50,50],index=date[6:8]).append(RSV)
KValue = pd.Series(0.0,index=RSV.index)
KValue[0]=50
for i in range(1,len(RSV)):
    KValue[i] = 2/3*KValue[i-1]+RSV[i]/3
KValue.name = 'KValue'

DValue = pd.Series(0.0,index=RSV.index)
DValue[0] = 50
for i in range(1,len(RSV)):
    DValue[i] = 2/3*DValue[i-1]+KValue[i]/3
DValue.name = 'DValue'

JValue = 3*KValue-2*DValue
JValue.name = 'JValue'

plt.figure(figsize=(10,5))
plt.subplot(211)
plt.title("2015年标准普尔500的收盘价")
plt.plot(close['2015'])
plt.subplot(212)
plt.title("2015年标准普尔500的RSV与KDJ线")
plt.plot(RSV['2015'],label='RSV线')
plt.plot(KValue['2015'],linestyle='dashed',label='KValue线')
plt.plot(DValue['2015'],linestyle=':',label='DValue线')
plt.plot(JValue['2015'],linestyle='-.',label='JValue线')

plt.legend(loc='best')
# plt.show()

