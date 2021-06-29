import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import movingAverage as ma

ChinaBank = pd.read_csv("./datas/030/ChinaBank.csv")
ChinaBank.index = ChinaBank.iloc[:,1]
ChinaBank.index = pd.to_datetime(ChinaBank.index,format="%Y-%m-%d")
ChinaBank = ChinaBank.iloc[:,2:]

CBClose = ChinaBank["Close"]

Close15 = CBClose["2015"]
SMA10 = ma.SMAcal(Close15,10)

weight = np.array(range(1,11))/sum(range(1,11))
WMA10 = ma.WMAcal(Close15,weight)

expo = 2/(len(Close15)+1)
EMA10 = ma.EMAcal(Close15,10,expo)

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.plot(Close15[9:],label="Close",color="k")
plt.plot(SMA10[9:],label="SMA10",color="r",linestyle="dashed")
plt.plot(WMA10[9:],label="WMA10",color="b",linestyle=":")
plt.plot(EMA10[9:],label="EMA10",color="g",linestyle="-.")
plt.title("中国银行均线")
plt.ylim(3.5,5.5)
plt.legend()
plt.show()

