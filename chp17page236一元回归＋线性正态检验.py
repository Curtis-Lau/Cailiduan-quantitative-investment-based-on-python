import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import scipy.stats as stats
import pylab

TRD_Index = pd.read_csv("./datas/017/TRD_Index.txt",sep="\t")
SHindex = TRD_Index[TRD_Index["Indexcd"]==1]
SZindex = TRD_Index[TRD_Index["Indexcd"]==399106]
SHRet = SHindex["Retindex"]
SZRet = SZindex["Retindex"]
SHRet.index = SZRet.index

model1 = sm.OLS(SHRet,sm.add_constant(SZRet)).fit()
print(model1.summary())

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

#线性性检验
plt.subplot(311)
plt.scatter(model1.fittedvalues,model1.resid)
plt.xlabel("拟合值")
plt.ylabel("残差")

#正态性检验
sm.qqplot(model1.resid_pearson,line="45")
pylab.show()

#同方差检验
plt.subplot(312)
plt.scatter(model1.fittedvalues,model1.resid_pearson)
plt.xlabel("拟合值")
plt.ylabel("标准化残差")  #要介于[-2,2]之间

# plt.show()

