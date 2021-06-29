import pandas as pd
import numpy as np
from arch.unitroot import ADF
from matplotlib import pyplot as plt
import statsmodels.api as sm

sh = pd.read_csv("./datas/026/sh50p.csv",index_col="Trddt")
sh.index = pd.to_datetime(sh.index)

#定义配对形成（formation period）
formStrat = "2014-01-01"
formEnd = "2015-01-01"

#形成数据
shform = sh[formStrat:formEnd]

#提取中国银行股票数据（601988）
PAF = shform["601988"]
#提取浦发银行股票数据（600000）
PBF = shform["600000"]

#将两只股票数据合在一起
parif = pd.merge(PAF,PBF,right_index=True,left_index=True)

#求形成期长度
# print(len(parif))       #结果是245

#协整模型
#检验中国银行对数价格的一阶单整性
PAFlog = np.log(PAF)
#单位根检验
adfA = ADF(PAFlog)
# print(adfA.summary())        #结果显示对数价格不是平稳序列
#将中国银行对数价格差分
retA = PAFlog.diff()[1:]
adfretA = ADF(retA)
# print(adfretA.summary())     #结果显示拒绝原假设，即接收备择假设：序列平稳。说明中国银行的对数价格是一阶单整序列

#对浦发银行价格取对数
PBFlog = np.log(PBF)
adfB = ADF(PAFlog)
# print(adfB.summary())       #结果显示对数价格不是平稳序列
retB = PBFlog.diff()[1:]
adfretB = ADF(retB)
# print(adfretB.summary())     #结果显示浦发银行对数价格的一阶差分序列平稳，即对数价格序列是一阶单整的

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
# #通过图形观测是否具有协整关系
# plt.subplot(211)
# PAFlog.plot(label="601988ZGYH",style=":")
# PBFlog.plot(label="600000PFYH",style="--")
# plt.legend(loc="best")
# plt.title("中国银行与浦发银行的对数价格时序图")

# #绘制对数价格差分的时序图
# plt.subplot(212)
# retA.plot(label="601988ZGYH")
# retB.plot(label="600000PFYH")
# plt.legend(loc="best")
# plt.title("中国银行与浦发银行对数价格差分图（收益率）")
# plt.show()

#协整检验——回归分析
#因变量是浦发银行的对数价格，自变量是中国银行的对数价格
model = sm.OLS(PBFlog,sm.add_constant(PAFlog))
results = model.fit()
# print(results.summary())    #结果显示截距项和参数显著

#对回归残差进行平稳性检验
alpha = results.params[0]
beita = results.params[1]
#求残差
spread = PBFlog - alpha - beita*PAFlog
# print(spread.head())
#绘制残差序列图
# spread.plot()
# plt.title("残差序列图")
# plt.show()

#残差序列单位根检验
adfspread = ADF(spread,trend="nc")
# print(adfspread.summary())             #结果显示残差序列平稳

#交易信号——定为μ±1.2σ
spreadf = PBFlog - alpha - beita*PAFlog
miu = np.mean(spreadf)
std = np.std(spreadf)

#交易期
tradStart = "2015-01-01"
tradEnd = "2015-06-30"
PAt = sh.loc[tradStart:tradEnd,"601988"]
PBt = sh.loc[tradStart:tradEnd,"600000"]
CoSpreadT = np.log(PBt) - alpha - beita*np.log(PAt)
CoSpreadT.plot()
plt.title("交易期价差序列（协整配对）")
plt.axhline(y=miu,color="black")
plt.axhline(y=miu+1.2*std,color="green")
plt.axhline(y=miu-1.2*std,color="green")

# plt.show()

level = (float('-inf'),miu-2.5*std,miu-1.5*std,miu-0.2*std,miu+0.2*std,miu+1.5*std,miu+2.5*std,float('inf'))
prclevel = pd.cut(CoSpreadT,level,labels=False)-3
print(prclevel)

