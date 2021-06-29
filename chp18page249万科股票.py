import pandas as pd
# import ffn
import numpy as np
import matplotlib.pylab as plt

stock = pd.read_csv("./datas/018/stockszA.csv",index_col="Trddt")

#万科股票代码是“000002”，在stockzA中存储为2
vanke = stock[stock["Stkcd"]==2]
close = vanke["Clsprc"]

close.index = pd.to_datetime(close.index)
close.index.name = "Date"

#收盘价滞后一期
lagclose = close.shift(1)
calret = pd.DataFrame({"close":close,"lagclose":lagclose})

#计算简单收益率
simpleret = (close-lagclose)/lagclose
calret["simpleret"] = simpleret

#计算2期简单收益率
simpleret2 = (close-close.shift(2))/close.shift(2)
calret["simpleret2"]=simpleret2

#查看1月9号的数据
# print(calret.iloc[5,:])

#用ffn计算简单收益率
# ffnSampleret = ffn.to_returns(close)
# ffnSampleret.name="ffnSampleret"
# print(ffnSampleret.head())

#计算年化收益率
annualize = (1+simpleret).cumprod()[-1]**(245/311)-1
# print(annualize)

#单期连续复利
comporet = np.log(close/lagclose)
comporet.name = "comporet"
#也可以调用ffn函数
# ffnComporet = ffn.to_log_returns(close)

#多期连续复利
comporet2 = np.log(close/close.shift(2))
comporet2.name = "comporet2"

#绘制收益图
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

#简单收益率曲线图
# plt.subplot(211)
plt.plot()
plt.title("万科股票简单收益率曲线图")


plt.show()
