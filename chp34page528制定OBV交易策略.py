import ffn
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import movingAverage as mv

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def trade(obv,price):
    signal = (2*(obv.diff()>0)-1)[1:]    #能量潮增大时，信号为1；减小时，信号为-1
    ret = ffn.to_returns(price)[1:]
    ret.name = 'ret'
    tradeRet = ret*signal.shift(1)
    tradeRet.name = 'tradeRet'
    Returns = pd.merge(pd.DataFrame(ret),
                       pd.DataFrame(tradeRet),
                       left_index=True,right_index=True).dropna()
    return (Returns)

TsingTao = pd.read_csv("./datas/034/TsingTao.csv",index_col = 'Date')
TsingTao = TsingTao.iloc[:,1:]
TsingTao.index = pd.to_datetime(TsingTao.index)
TsingTao['Volume'] = TsingTao['Volume'].replace(0,np.nan)
TsingTao = TsingTao.dropna()
close = TsingTao['Close']
volume = TsingTao['Volume']

## 评价累积OBV指标
difClose = close.diff()
difClose[0] = 0
OBV = (((difClose>=0)*2-1)*volume).cumsum()
OBVtrade = trade(OBV,close)

#评价策略表现
ret = OBVtrade.ret
tradeRet = OBVtrade.tradeRet
ret.name = 'BuyAndHold'
tradeRet.name = 'OBVtrade'
(1+ret).cumprod().plot(label='ret',linestyle='dashed')
(1+tradeRet).cumprod().plot(label='tradeRet')
plt.title("累积OBV交易策略绩效表现")
plt.legend()
# plt.show()

#定义表现函数
def backtest(ret,tradeRet):
    def performance(x):
        winpect = len(x[x>0])/len(x[x!=0])
        annRet = (1+x).cumprod()[-1]**(245/len(x))-1
        sharpe = ffn.calc_risk_return_ratio(x)
        maxDD = ffn.calc_max_drawdown((1+x).cumprod())
        perfolio = pd.Series([winpect,annRet,sharpe,maxDD],
                          index=['win rate','annualized return','sharpe ratio','maximum drawdown'])
        return (perfolio)
    BuyAndHold = performance(ret)
    OBVtrade = performance(tradeRet)
    return (pd.DataFrame({ret.name:BuyAndHold,tradeRet.name:OBVtrade}))
OBVtest = backtest(ret,tradeRet)
# print(OBVtest)

## 评价smOBV指标
smOBV = mv.SMAcal(OBV,9)
smOBVtrade = trade(smOBV,close)
ret = smOBVtrade.ret
ret.name = 'BuyAndHold'
smtradeRet = smOBVtrade.tradeRet
smtradeRet.name = 'smOBVtrade'
(1+ret).cumprod().plot(label='ret',linestyle='dashed')
(1+smtradeRet).cumprod().plot(label='tradeRet')
plt.title("简单移动OBV交易策略绩效表现")
plt.legend()
plt.show()

smOBVtest = backtest(ret,smtradeRet)
print(smOBVtest)

