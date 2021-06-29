import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

Vanke = pd.read_csv("./datas/028/Vanke.csv")
Vanke.index = Vanke.iloc[:,1]
Vanke.index = pd.to_datetime(Vanke.index)
Vanke = Vanke.iloc[:,2:]
Close = Vanke["Close"]

def momentum(price, period):
    lagprice = price.shift(period)
    momen = price - lagprice
    momen = momen.dropna()
    return (momen)

momen35 = momentum(Close,35)

#当35日动量值为负值时，signal取值为-1，表示卖出；
#当35日动量值为非负值时，signal取值1，表示买入。

signal = []
for i in momen35:
    if i>0:
        signal.append(1)
    else:
        signal.append(-1)

signal = pd.Series(signal,index=momen35.index)

tradeSig = signal.shift(1)
ret = Close/Close.shift(1)-1
Mom35Ret = (ret*tradeSig).dropna()
#Mom35Ret为正说明前一天预测的买或卖正确，因为：
# 举例假设昨天预测将要下跌，则说明今天收益率小于零，两者相乘即Mom35Ret大于零，预测正确。

Mom35Ret[Mom35Ret==-0]=0
win = Mom35Ret[Mom35Ret>0]    #预测正确的次数
winrate = len(win)/len(Mom35Ret[Mom35Ret!=0])   #预测正确的概率

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

# plt.subplot(211)
# plt.plot(ret[-len(Mom35Ret):],'b')
# plt.ylabel("return")
# plt.ylim(-0.13,0.10)
# plt.title("收益率时序图")
#
# plt.subplot(212)
# plt.plot(Mom35Ret,'r')
# plt.ylabel("Mom35Ret")
# plt.ylim(-0.13,0.10)
# plt.title("动量交易收益率时序图")

loss = -Mom35Ret[Mom35Ret<0]
plt.subplot(211)
win.hist()
plt.title("盈利直方图")
plt.subplot(212)
loss.hist()
plt.title("亏损直方图")
plt.show()

performance = pd.DataFrame({"win":win.describe(),"loss":loss.describe()})
print(performance)