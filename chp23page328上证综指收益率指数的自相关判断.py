from statsmodels.tsa import stattools
import pandas as pd
from statsmodels.graphics.tsaplots import *
from matplotlib import pyplot as plt

data = pd.read_table("./datas/023/TRD_Index.txt",sep="\t",index_col="Trddt")

#提取上证综指数据
SHindex = data[data["Indexcd"]==1]
SHindex.index = pd.to_datetime(SHindex.index)

SHRet = SHindex["Retindex"]

acf = stattools.acf(SHRet)

pacf = stattools.pacf(SHRet)

# plot_acf(SHRet,use_vlines=True,lags=30)
# plot_pacf(SHRet,use_vlines=True,lags=30)

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

#平稳性检验
#1、观察时间序列图
plt.subplot(211)
SHclose = SHindex["Clsindex"]
SHclose.plot()
plt.title("2014-2015年上证综指收盘指数时序图")
plt.subplot(212)
SHRet.plot()
plt.title("2014-2015年上证综指收益率指数时序图")

#2、自相关图
# plot_acf(SHRet,use_vlines=True,lags=30)
# plot_pacf(SHRet,use_vlines=True,lags=30)
plot_acf(SHclose,use_vlines=True,lags=30)

# plt.show()

#3、单位根检验(ADF)
from arch.unitroot import ADF
adfSHRet = ADF(SHRet)   #——输出的是一个ADF对象，不能直接输出，要借助summary()方法
print(adfSHRet.summary())


