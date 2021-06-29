import pandas as pd
import matplotlib.pyplot as plt

stock = pd.read_table("./datas/019/stock.txt",sep="\t",index_col="Trddt")
fjgs = stock[stock["Stkcd"]==2599]["Dretwd"]
fjgs.name="fjgs"

zndl = stock[stock["Stkcd"]==2600]["Dretwd"]
zndl.name="zndl"

sykj = stock[stock["Stkcd"]==2601]["Dretwd"]
sykj.name="sykj"

hxyh = stock[stock["Stkcd"]==2602]["Dretwd"]
hxyh.name="hxyh"

byjc = stock[stock["Stkcd"]==2603]["Dretwd"]
byjc.name="byjc"

sh_return = pd.concat([byjc,fjgs,hxyh,sykj,zndl],axis=1).dropna()
sh_return.index = pd.to_datetime(sh_return.index)
print(sh_return)
#查看各股的累计回报率
cumreturn = (1+sh_return).cumprod()

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

sh_return.plot()
plt.title("Daily Return of 5 Stocks(2014)")

cumreturn.plot()
plt.title("Cumulative Return of 5 Stocks(2014)")

plt.legend(loc="best")
# plt.show()

#股票之间的相关性
corr = sh_return.corr()
# print(corr)

