import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TsingTao = pd.read_csv("./datas/030/TsingTao.csv")
TsingTao.index = TsingTao.iloc[:,1]
TsingTao.index = pd.to_datetime(TsingTao.index,format="%Y-%m-%d")
TsingTao = TsingTao.iloc[:,2:]

Close = TsingTao["Close"]

#绘制收盘价数据时序图
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# plt.subplot()
# plt.plot(Close,"k")
# plt.xlabel("date")
# plt.ylabel("Close")
# plt.title("2014年青岛啤酒股票收盘价时序图")
# # plt.show()

#求5日的简单移动平均
SMA5 = pd.Series(0.0,index=Close.index)
for i in range(4,len(Close)):
    SMA5[i] = sum(Close[(i-4):(i+1)])/5
plt.plot(Close[4:],label="Close",color="g")
plt.plot(SMA5[4:],label="SMA5",color="r",linestyle="dashed")
plt.title("青岛啤酒收盘价与简单移动平均线")
plt.ylim(35,50)
plt.legend(loc="best")
plt.show()

#简单移动平均函数
def calSMA(tsPrice,period):
    SMA = pd.Series(0.0,index=tsPrice.index)
    for i in range(period-1,len(tsPrice)):
        SMA[i] = sum(tsPrice[(i-period+1):(i+1)])/period
    return (SMA)
