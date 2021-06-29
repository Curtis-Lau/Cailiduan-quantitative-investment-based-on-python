import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statsmodels.tsa import stattools
from arch import arch_model

SHret = pd.read_table("./datas/025/TRD_IndexSum.txt",index_col="Trddt",sep="\t")
SHret.index = pd.to_datetime(SHret.index)
SHret = SHret.sort_index()

#绘制收益率平方序列图——是否存在ARCH效应（波动聚集）
plt.subplot(311)
plt.plot(SHret)
plt.xticks([])
plt.title("Daily Return of SH Index")

plt.subplot(312)
plt.plot(SHret**2)
plt.xticks([])
plt.title("Squared Daily Return of SH Index")

plt.subplot(313)
plt.plot(np.abs(SHret))
plt.title("Absolute Daily Return of SH Index")
# plt.show()

#用LB检验收益率平方的自相关性(不是白噪声)
LjungBox = stattools.q_stat(stattools.acf(SHret**2)[1:13],len(SHret))[1]
# print(LjungBox)     #结果小于0.05，拒绝原假设（白噪声假设），也即存在ARCH效应

#设定模型
am = arch_model(SHret)

#估计参数
#update_freq=0表示不输出中间结果，只输出最终结果
model = am.fit(update_freq=0)
print(model.summary())
