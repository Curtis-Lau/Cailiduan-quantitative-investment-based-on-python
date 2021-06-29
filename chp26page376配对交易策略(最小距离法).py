import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

sh = pd.read_csv("./datas/026/sh50p.csv",index_col="Trddt")
sh.index = pd.to_datetime(sh.index)

#定义配对形成（formation period）
formStrat = "2014-01-01"
formEnd = "2015-01-01"

#形成数据
shfrom = sh[formStrat:formEnd]

#提取中国银行股票数据（601988）
PAF = shfrom["601988"]
#提取浦发银行股票数据（600000）
PBF = shfrom["600000"]

#将两只股票数据合在一起
parif = pd.merge(PAF,PBF,right_index=True,left_index=True)

#求形成期长度
# print(len(parif))       #结果是245

#最小距离法
#构造标准化价格之差平方累积SSD函数
def SSD(priceX,priceY):
    if priceX is None or priceY is None:
        print("缺少价格序列。")
    returnX = (priceX-priceX.shift(1))/priceX.shift(1)[1:]
    returnY = (priceY-priceY.shift(1))/priceY.shift(1)[1:]
    standardX = (returnX+1).cumpord()
    standardY = (returnY+1).cumprod()
    SSD = np.sum((standardX-standardY)**2)
    return (SSD)

#求中国银行与浦发银行价格的距离——理论上应对上证50股票两两配对，计算SSD，选取最小的。这里默认为选中国银行和浦发银行
distance = SSD(PAF,PBF)
# print(distance)

#配对交易策略
retA = (PAF-PAF.shift(1))/PAF.shift(1)[1:]
retB = (PBF-PBF.shift(1))/PBF.shift(1)[1:]

#标准化价格
standardA = (1+retA).cumprod()
standardB = (1+retB).cumprod()
#价差
SSD_pair = standardB-standardA

meanSSD_pair = np.mean(SSD_pair)
sdSSD_pair = np.std(SSD_pair)

#交易信号  ——  定为μ±1.2σ
thresholdUp = meanSSD_pair+1.2*sdSSD_pair
thresholdDown = meanSSD_pair-1.2*sdSSD_pair

#交易期
tradStart = "2015-01-01"
tradEnd = "2015-06-30"
PAt = sh.loc[tradStart:tradEnd,"601988"]
PBt = sh.loc[tradStart:tradEnd,"600000"]

def spreadCal(x,y):
    retx = (x-x.shift(1))/x.shift(1)[1:]
    rety = (y-y.shift(1))/y.shift(1)[1:]
    standardX = (1+retx).cumprod()
    standardY = (1+rety).cumprod()
    spread = standardX-standardY
    return (spread)

TradSpread = spreadCal(PBt,PAt)

TradSpread.plot()
plt.axhline(y=meanSSD_pair,color="black")
plt.axhline(y=thresholdUp,color="green")
plt.axhline(y=thresholdDown,color="green")
plt.show()