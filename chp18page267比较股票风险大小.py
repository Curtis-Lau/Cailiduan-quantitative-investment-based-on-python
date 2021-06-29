import pandas as pd
import ffn

SAPower = pd.read_csv("./datas/018/SAPower.csv",index_col="Date")
SAPower.index = pd.to_datetime(SAPower.index)

DalianRP = pd.read_csv("./datas/018/DalianRP.csv",index_col="Date")
DalianRP.index = pd.to_datetime(DalianRP.index)

returnS = ffn.to_returns(SAPower["Close"])
returnD = ffn.to_returns(DalianRP["Close"])

print(returnS.std())
print(returnD.std())
print("*"*100)

#计算下行风险——收益率均值作为MARR
def cal_half_dev(returns):
    marr = returns.mean()
    temp_returns = returns[returns<marr]
    half_deviation = (sum((marr-temp_returns)**2/len(returns)))**0.5
    return(half_deviation)

print(cal_half_dev(returnS))
print(cal_half_dev(returnD))

#风险价值VaR
#历史模拟法
print(returnS.quantile(0.05))
print(returnD.quantile(0.05))

#协方差矩阵法
from scipy.stats import norm
print(norm.ppf(0.05,returnS.mean(),returnS.var()))
print(norm.ppf(0.05,returnD.mean(),returnD.var()))


