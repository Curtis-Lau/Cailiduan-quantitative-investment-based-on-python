import pandas as pd
import ffn
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import statsmodels.api as sm

#获取指数数据，作为市场收益率
indexcd = pd.read_csv("./datas/020/TRD_Index.csv",index_col="Trddt")
mktcd = indexcd[indexcd["Indexcd"]==902]
mktret = pd.Series(mktcd["Retindex"].values,index=pd.to_datetime(mktcd.index))
mktret.name = "mktret"
mktret = mktret["2014-01-02":"2014"]

#获取新安股份股票数据——个股
xin_an = pd.read_csv("./datas/020/xin_an.csv",index_col="Date")
xin_an.index = pd.to_datetime(xin_an.index)
xin_anret = ffn.to_returns(xin_an["Close"])
xin_anret.name = "returns"
xin_anret = xin_anret.dropna()

#将新安股份和市场指数收益率合并在一起，将没有交易的数据删除
Ret = pd.merge(pd.DataFrame(mktret),
               pd.DataFrame(xin_anret),
               left_index=True,right_index=True,how="inner")

#计算无风险收益率
rf = (1+0.036)**(1/360)-1

#计算市场风险溢酬和股票的超额收益率
Eret = Ret-rf
print(Eret)
#画散点图
plt.scatter(Eret.values[:,0],Eret.values[:,1])
plt.xlabel("Market Return")
plt.ylabel("XinAnGuFen Return")
plt.title("XinAnGuFen Return and Market Return")
# plt.show()

# 拟合CAPMA函数
model = sm.OLS(Eret["returns"],Eret["mktret"]).fit()
print(model.summary(),"\n",model.params)
