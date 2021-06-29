import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

TsingTao = pd.read_csv("./datas/030/TsingTao.csv")
TsingTao.index = TsingTao.iloc[:,1]
TsingTao.index = pd.to_datetime(TsingTao.index,format="%Y-%m-%d")
TsingTao = TsingTao.iloc[:,2:]

Close = TsingTao["Close"]

EMA5_number1 = np.mean(Close[0:5])
#计算第六天的指数移动平均数
EMA5_number2 = 0.2*Close[5]+0.8*EMA5_number1
EMA5 = pd.Series(0.0,index=Close.index)
EMA5[4] = EMA5_number1  #第五天数据录入EMA5
EMA5[5] = EMA5_number2  #第六天数据录入EMA5

#计算第七天及以后的指数加权平均是
for i in range(6,len(Close)):
    expo = np.array(sorted(range(i-4),reverse=True))
    w = (1-0.2)**expo
    EMA5[i] = sum(0.2*w*Close[5:(i+1)])+EMA5_number1*0.8**(i-4)

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.plot(Close[4:],label="Close",color="k")
plt.plot(EMA5[4:],label="EMA5",color="g",linestyle="-.")
plt.title("青岛啤酒收盘价指数移动平均线")
plt.ylim(35,50)
plt.legend()
# plt.show()

#指数加权移动平均函数
def EMAcal(tsprice,period=5,exponential=0.2):
    EMA = pd.Series(0.0,index = tsprice.index)
    EMA[period-1] = np.mean(tsprice[:period])
    for i in range(period,len(tsprice)):
        EMA[i] = exponential*tsprice[i]+(1-exponential)*EMA[i-1]
    return (EMA)

Ema = EMAcal(Close,5,0.2)
print(Ema)




