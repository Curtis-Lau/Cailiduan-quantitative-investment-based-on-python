import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

HSRet300 = pd.read_csv("./datas/014/return300.csv")
# print(HSRet300.head(5))

density = stats.kde.gaussian_kde(HSRet300["return"])
bins = np.arange(-5,5,0.02)

plt.rcParams["font.sans-serif"] = ["SimHei"]      #图显示中文
plt.rcParams['axes.unicode_minus']=False         #解决坐标轴不能显示负数的问题

plt.subplot(211)
plt.plot(bins,density(bins))
plt.title("沪深300收益率序列的概率密度曲线图")

plt.subplot(212)
plt.plot(bins,density(bins).cumsum())
plt.title("沪深300收益率序列的累计分布函数图")

plt.show()
