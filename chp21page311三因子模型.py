import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm

stock = pd.read_table("./datas/021/stock.txt",sep="\t",index_col="Trddt")
#获取华夏银行的股票数据
#股票代码是“600015.SH”
HXBank = stock[stock["Stkcd"]==600015]
HXBank.index = pd.to_datetime(HXBank.index)

HXRet = HXBank["Dretwd"]
HXRet.name = "HXRet"
# HXRet.plot()

ThreeFactors = pd.read_table("./datas/021/ThreeFactors.txt",sep="\t",index_col="TradingDate")
#将三因子数据转化成时间序列格式
ThreeFactors.index = pd.to_datetime(ThreeFactors.index)
#截取2014年1月2日以后的数据
ThrFac = ThreeFactors["2014-01-02":]
#获取三因子变量
ThrFac = ThrFac.iloc[:,[2,4,6]]

#合并收益率数据与三因子数据
HXThrFac = pd.merge(pd.DataFrame(HXRet),
                    pd.DataFrame(ThrFac),
                    left_index=True,right_index=True)

plt.subplot(311)
plt.scatter(HXThrFac["HXRet"],HXThrFac["RiskPremium2"])
plt.subplot(312)
plt.scatter(HXThrFac["HXRet"],HXThrFac["SMB2"])
plt.subplot(313)
plt.scatter(HXThrFac["HXRet"],HXThrFac["HML2"])
plt.show()

model = sm.OLS(HXThrFac["HXRet"],sm.add_constant(HXThrFac.iloc[:,1:])).fit()
print(model.summary())
print(model.params)


