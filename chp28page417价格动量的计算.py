import pandas as pd
import matplotlib.pyplot as plt

Vanke = pd.read_csv("./datas/028/Vanke.csv")
Vanke.index = Vanke.iloc[:,1]
Vanke.index = pd.to_datetime(Vanke.index)
Vanke = Vanke.iloc[:,2:]

##作差法提取动量值
#提取收盘价
Close = Vanke["Close"]
lag5Close = Close.shift(5)
momentum5 = Close - lag5Close

#绘制收盘价和5日动量曲线图
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

plt.subplot(311)
plt.plot(Close,"b*")
plt.xlabel("date")
plt.ylabel("Close")
plt.title("万科股票收盘价序列图")

plt.subplot(312)
plt.plot(momentum5,"r-*")
plt.xlabel("date")
plt.ylabel("Momentum5")
plt.title("万科股票5日动量图")

# plt.show()

##作除法提取动量值
plt.subplot(313)
Momen5 = Close/lag5Close-1
Momen5 = Momen5.dropna()
Momen5.plot()

plt.show()

#编写成函数
def momentum(price,period):
    lagprice = price.shift(period)
    momen = price - lagprice
    momen = momen.dropna()
    return (momen)
