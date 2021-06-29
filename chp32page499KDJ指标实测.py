## K、D捕捉超买、超卖信号
# K值大于85，超买，signal为-1；
# K值小于20，超卖，signal为1；
# D值大于80，超买，signal为-1；
# D值小于20，超卖，signal为1。
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TKAgg")
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

KSignal = KValue.apply(lambda x:-1 if x>85 else 1 if x<20 else 0)
DSignal = DValue.apply(lambda x:-1 if x>80 else 1 if x<20 else 0)
KDSignal = KSignal + DSignal
KDSignal.name = 'KDSignal'

KDSignal[KDSignal>=1] = 1
KDSignal[KDSignal<=-1] = -1

def trade(signal,price):
    ret = (price/price.shift(1)-1)[1:]
    ret.name = 'ret'
    signal = signal.shift(1)[1:]
    tradeRet = signal*ret + 0
    tradeRet.name = 'tradeRet'
    Returns = pd.merge(pd.DataFrame(ret),
                       pd.DataFrame(tradeRet),
                       left_index=True,
                       right_index=True).dropna()
    return (Returns)

KDtrade = trade(KDSignal,close)
KDtrade.rename(columns={"ret":"Ret",
                        "tradeRet":"KDtradeRet"},inplace=True)

import ffn
def backtest(ret,tradeRet):
    def performance(x):
        winpct = len(x[x>0])/len(x[x!=0])
        annRet = (1+x).cumprod()[-1]**(245/len(x))-1
        sharpe_ratio = ffn.calc_risk_return_ratio(x)
        maxDD = ffn.calc_max_drawdown((1+x).cumprod())
        perfo = pd.Series([winpct,annRet,sharpe_ratio,maxDD],
                          index=["win rate","annualized return","sharpe ratio","maximum drawdown"])
        return (perfo)
    BuyAndHold = performance(ret)
    Trade = performance(tradeRet)
    return (pd.DataFrame({ret.name:BuyAndHold,
                          tradeRet.name:Trade}))

cumRets1 = (1+KDtrade).cumprod()
plt.plot(cumRets1['Ret'],label='Ret')
plt.plot(cumRets1['KDtradeRet'],'--',label='KDtradeRet')
plt.title("KD指标交易策略绩效表现")
plt.legend(loc='best')
# plt.show()

## J值定义超买超卖
# J大于100，超买
# J小于0，超卖
JValue = 3*KValue-2*DValue
JValue.name = 'JValue'
JSignal = JValue.apply(lambda x:-1 if x>100 else 1 if x<0 else 0)
KDJSignal = KSignal + DSignal + JSignal
KDJSignal = KDJSignal.apply(lambda x:1 if x>=2 else -1 if x<=-1 else 0)
KDJtrade = trade(KDJSignal,close)
KDJtrade.rename(columns={"ret":"Ret",
                         "tradeRet":"KDJtradeRet"},
                inplace = True)
print(backtest(KDJtrade['Ret'],KDJtrade['KDJtradeRet']))

## K线、D线的“金叉”与“死叉”
