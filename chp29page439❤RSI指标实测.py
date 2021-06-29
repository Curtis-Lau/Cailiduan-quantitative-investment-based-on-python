import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def rsi(price,period=6):
    closepriceChange = price - price.shift(1)
    closepriceChange.dropna(inplace=True)
    indexprc = closepriceChange.index

    upPrc = pd.Series(0,index=indexprc)
    upPrc[closepriceChange>0] = closepriceChange[closepriceChange>0]
    downPrc = pd.Series(0,index=indexprc)
    downPrc[closepriceChange<0] = -closepriceChange[closepriceChange<0]

    rsidata = pd.concat([price,closepriceChange,upPrc,downPrc],axis=1)
    rsidata.columns = ["Close","PrcChange","upPrc","downPrc"]
    rsidata.dropna(inplace=True)

    SMUP = []
    SMDOWN = []
    for i in range(period,len(upPrc)+1):
        SMUP.append(np.mean(upPrc.values[(i-period):i],dtype=np.float32))
        SMDOWN.append(np.mean(downPrc.values[(i-period):i],dtype=np.float32))

    rsi = [100*SMUP[i]/(SMUP[i]+SMDOWN[i]) for i in range(0,len(SMUP))]
    indexRsi = indexprc[(period-1):]
    rsi = pd.Series(rsi,index=indexRsi)
    return (rsi)

BOCM = pd.read_csv("./datas/029/BOCM.csv")
BOCM.index = BOCM.iloc[:,1]
BOCM.index = pd.to_datetime(BOCM.index,format="%Y-%m-%d")
BOCMclp = BOCM["Close"]

rsi6 = rsi(BOCMclp,6)
rsi24 = rsi(BOCMclp,24)

##求交易信号
#交易信号一：rsi6的超卖与超卖
Sig1 = []
for i in rsi6:
    if i>80:
        Sig1.append(-1)
    elif i<20:
        Sig1.append(1)
    else:
        Sig1.append(0)
Signal1 = pd.Series(Sig1,index=rsi6.index)

#交易信号二：黄金交叉与死亡交叉
Signal2 = pd.Series(0,index=rsi24.index)
lagrsi6 = rsi6.shift(1)
lagrsi24 = rsi24.shift(1)
for i in rsi24.index:
    if (rsi6[i]>rsi24[i])&(lagrsi6[i]<lagrsi24[i]):
        Signal2[i]=1
    elif (rsi6[i]<rsi24[i])&(lagrsi6[i]>lagrsi24[i]):
        Signal2[i]=-1

#合并交易信号
signal = Signal1+Signal2
signal[signal>=1]=1
signal[signal<=-1]=-1
signal.dropna(inplace=True)

##RSI策略执行及回测
tradeSig = signal.shift(1)          #前一天买入，日期用的是今天的日期，但实际上是昨天的数据

#求买入交易收益率
ret = BOCMclp/BOCMclp.shift(1)-1    #与tradeSig不一样，一个是昨天（tradeSig），一个是今天
traderet = ret[tradeSig.index]      #查找日期一样的数据，tradeRet表示今天的价格

buy = tradeSig[tradeSig==1]         #日期虽然与tradeRet一样，但实际上是昨天买的
buyRet = traderet[tradeSig==1]*buy         #昨天买的乘以今天的收益率

#求卖出交易收益率
sell = tradeSig[tradeSig==-1]
sellRet = traderet[tradeSig==-1]*sell

#求出买卖交易合并的收益率
tradeRet = traderet*tradeSig

#绘制三中交易率的时序图
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# plt.subplot(211)
# plt.plot(buyRet,label="buyRet",color="g")
# plt.plot(sellRet,label="sellRet",color="r",linestyle="dashed")
# plt.title("RSI指标交易策略")
# plt.ylabel("strategy return")
# plt.legend(loc="best")
#
# plt.subplot(212)
# plt.plot(ret,"b")
# plt.ylabel("stock return")

# plt.show()

##计算信号点预测准确率情况
def strat(tradeSignal,traderet):
    indexData = tradeSignal.index
    ret = traderet[indexData]
    tradeRet = ret*tradeSignal      #若traSignal是buy的，则tradeSignal全部大于0，如果ret>0，说明赚钱，小于0，预测序错误
    tradeRet[tradeRet==(-0)]=0
    winRate = len(tradeRet[tradeRet>0])/len(tradeRet[tradeRet!=0])
    meanRet = sum(tradeRet[tradeRet>0])/len(tradeRet[tradeRet>0])
    meanloss = sum(tradeRet[tradeRet<0])/len(tradeRet[tradeRet<0])
    perform = {"winRate":winRate,
               "meanRet":meanRet,
               "lossRet":meanloss}
    return (perform)

BuyOnly = strat(buy,traderet)
SellOnly = strat(sell,traderet)
Trade = strat(tradeSig,traderet)
Test = pd.DataFrame({"BuyOnly":BuyOnly,
                     "SellOnly":SellOnly,
                     "Trade":Trade})
# print(Test)

##比较RSI指标交易策略的累计收益率
# cumStock = np.cumprod(1+ret)-1
# cumTrade = np.cumprod(1+tradeRet)-1
#
# plt.subplot(211)
# plt.plot(cumStock)
# plt.ylabel("cumStock")
# plt.title("股票本身收益率")
#
# plt.subplot(212)
# plt.plot(cumTrade)            #这个可以看出每个时期持有的股票持有到现在的收益率
# plt.ylabel("cumTrade")
# plt.title("RSI策略累计收益率")
#结果显示绩效不理想
# plt.show()

#调整策略——调整RSI释放出买卖信号后再隔3天进行买卖操作
tradeSig2 = signal.shift(3)
ret2 = traderet[tradeSig2.index]
buy2 = tradeSig2[tradeSig2==1]
buy2Ret = ret2[tradeSig2==1]*buy2
sell2 = tradeSig2[tradeSig2==-1]
sell2Ret = ret2[tradeSig2==-1]*sell2
tradeRet2 = ret2*tradeSig2
BuyOnly2 = strat(buy2,ret2)
SellOnly2 = strat(sell2,ret2)
Trade2 = strat(tradeSig2,ret2)
Test2 = pd.DataFrame({"BuyOnly2":BuyOnly2,
                     "SellOnly2":SellOnly2,
                     "Trade2":Trade2})
print(Test2)

cumStock2 = np.cumprod(1+ret2)-1
cumTrade2 = np.cumprod(1+tradeRet2)-1
plt.subplot(211)
plt.plot(cumStock2)
plt.ylabel("cumStock")
plt.title("股票本身收益率")

plt.subplot(212)
plt.plot(cumTrade2)
plt.ylabel("cumTrade")
plt.title("RSI策略累计收益率")

plt.show()