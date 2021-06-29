import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

TsingTao = pd.read_csv("./datas/030/TsingTao.csv")
TsingTao.index = TsingTao.iloc[:,1]
TsingTao.index = pd.to_datetime(TsingTao.index,format="%Y-%m-%d")
TsingTao = TsingTao.iloc[:,2:]

Close = TsingTao["Close"]

#定义权重
b = np.array([1,2,3,4,5])
w = b/sum(b)

WMA5 = pd.Series(0.0,index=Close.index)
for i in range(4,len(Close)):
    WMA5[i] = sum(w*Close[(i-4):(i+1)])

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.plot(Close[4:],label="Close",color="g")
plt.plot(WMA5[4:],label="WMA5",color="r",linestyle=":")
plt.title("青岛啤酒收盘价加权移动平均线")
plt.ylim(35,50)
plt.legend()
# plt.show()

#加权移动平均线函数
def WMAcal(tsprice,weight):
    period = len(weight)
    arrWeight = np.array(weight)
    WMA = pd.Series(0.0,index=tsprice.index)
    for i in range(period-1,len(tsprice)):
        WMA[i] = sum(arrWeight*tsprice[(i-period+1):(i+1)])
    return (WMA)
print(WMAcal(Close,w))
