import pandas as pd
from statsmodels.graphics.tsaplots import *  #用于对ACF、PACF画图
from arch.unitroot import ADF                #用于导出ADF（平稳性检验）
from statsmodels.tsa import  stattools       #用于LB检验（白噪声检验）
from statsmodels.tsa import arima_model      #用于建立ARIMA模型
import math
from matplotlib import pyplot as plt

Datang = pd.read_csv("./datas/024/Datang.csv",index_col="time")
Datang.sort_index = pd.to_datetime(Datang.index)

returns = Datang["2014-01-01":"2016-01-01"]

#1、平稳性检验——ADF
# print(ADF(returns).summary())   #结果为-18小于-3.44（1%）,序列平稳

#2、白噪声检验
LjungBox = stattools.q_stat(stattools.acf(returns)[1:12],len(returns))[1]
# print(LjungBox)    #结果均小于0.05，拒绝原假设（H0:白噪声假设）

##3、ARIMA建模
#3.1 max_ma 参数用于执行最大ma滞后阶数——用于确定p、q值
# print(stattools.arma_order_select_ic(returns,max_ar=4))   #结果显示选择ARMA(1,0)模型

#3.2 查看模型结果
model = arima_model.ARIMA(returns,order=(1,0,0)).fit()
# print(model.summary())
# print(model.conf_int())      #系数不为0

#4、残差诊断
stdresid = model.resid/math.sqrt(model.sigma2)
plt.plot(stdresid)           #满足正态性假设（高斯白噪声）

plot_acf(stdresid,lags=12)   #绝大部分在95%内
# plt.show()

LjungBox2 = stattools.q_stat(stattools.acf(stdresid)[1:12],len(stdresid))[1]
print(LjungBox2)     #结果均大于0.05，即接受原假设（白噪声假设）
# print(stattools.acf(stdresid))

