import pandas as pd
from matplotlib import pyplot as plt

CPI = pd.read_csv("./datas/024/CPI.csv",index_col="time")
CPI.index = pd.to_datetime(CPI.index)

#剔除最后3期（2014年3,4,5月）的数据，对它进行预测，与真实值比较

#第一步：序列平稳性检验
#1、看图
CPItrain = CPI[3:]
CPI.sort_index(ascending=False).plot(title="CPI 2001-2015")
# plt.show()   #序列看上去还算平稳，下面进行ADF检验

#2、ADF检验
from arch.unitroot import ADF
CPItrain = CPItrain.dropna()["CPI"]
print(ADF(CPItrain,max_lags=10).summary())   #结果显示在5%水平下拒绝原假设，即认为序列是平稳的

#第二步：CPI序列是否为白噪声序列——LB检验
from statsmodels.tsa import stattools
LjungBox = stattools.q_stat(stattools.acf(CPItrain)[1:12],len(CPItrain))
# print(LjungBox[1][-1])     #小于0.05，拒绝原假设（白噪声），即认为该序列不是白噪声

#第三步：需要识别ARMA模型的p和q——用ACF和PACF来判断
from statsmodels.graphics.tsaplots import *
#将画面一分为二，第一个画ACF图，第二个画PACF图
axe1 = plt.subplot(211)
axe2 = plt.subplot(212)
plot1 = plot_acf(CPItrain,use_vlines=True,lags=30,ax=axe1)
plot2 = plot_pacf(CPItrain,use_vlines=True,lags=30,ax=axe2)
# plt.show()   #ACF和PACF都呈现拖尾现象，不能确定p和q的值
#运用AIC准则进行比较
from statsmodels.tsa import arima_model
model1 = arima_model.ARIMA(CPItrain,order=(1,0,1)).fit()
model2 = arima_model.ARIMA(CPItrain,order=(1,0,2)).fit()
model6 = arima_model.ARIMA(CPItrain,order=(3,0,2)).fit()
#   .......
print(model6.summary())    #通过建立6个模型，比较AIC值，最终确定p=3，q=2

#第四步：模型诊断——系数显著性检验和残差序列是否为白噪声，如果不是，则需要调整
#1、计算系数的置信区间，不为0，则表示在5%的置信水平下，所有系数都显著
# print(model6.conf_int())    #结果显示显著
#2、检验残差序列——可以用ACF检验resid（残差）是否存在相关
import math
stdresid = model6.resid/math.sqrt(model6.sigma2)
plot_acf(stdresid)
# plt.show()
LjungBox2 = stattools.q_stat(stattools.acf(stdresid)[1:13],len(stdresid))
# print(LjungBox2[1][-1])     #不管是ACF值还是LjungBox值，都显示该残差序列不是一个白噪声

#第五步：预测
print(model6.forecast(3)[0])   #一共三个array，第一个是预测值，第二个是标准误，第三个是置信区间


