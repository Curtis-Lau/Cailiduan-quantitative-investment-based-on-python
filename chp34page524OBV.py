import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import movingAverage as mv

TsingTao = pd.read_csv("./datas/034/TsingTao.csv",index_col = 'Date')
TsingTao = TsingTao.iloc[:,1:]
TsingTao.index = pd.to_datetime(TsingTao.index)
TsingTao['Volume'] = TsingTao['Volume'].replace(0,np.nan)
TsingTao = TsingTao.dropna()
close = TsingTao['Close']
volume = TsingTao['Volume']

## 计算累积OBV
difClose = close.diff()
difClose[0] = 0
OBV = (((difClose>=0)*2-1)*volume).cumsum()
#difClose>=0的结果是True(1)和False(0),乘2减1,使得价格上涨的为1，下跌的为-1

## 计算移动型OBV
smOBV = mv.SMAcal(OBV,9)

## 计算修正型OBV
AdjOBV = ((close-TsingTao['Low'])-(TsingTao['High']-close))/(TsingTao['High']-TsingTao['Low'])*volume
AdjOBV.name = 'AdjOBV'
AdjOBVd = AdjOBV.cumsum()
AdjOBVd.name = 'AdjOBVd'

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10,8))
ax1 = plt.subplot(311)
close.plot(title="青岛啤酒收盘价")
plt.xticks(close.index[1:3],(''))
plt.xlabel('')
ax2 = plt.subplot(312)
OBV.plot(label='OBV',title="青岛啤酒累积能量潮与移动能量潮")
smOBV.plot(label='smOBV',linestyle=":",color='r')
plt.legend(loc='best')
plt.xticks(close.index[1:3],(''))
plt.xlabel('')
ax3 = plt.subplot(313)
AdjOBVd.plot(title="青岛啤酒多空比率净额")
for ax in ax1,ax2,ax3:
    ax.grid(True)
plt.show()

