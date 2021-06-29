import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BOCM = pd.read_csv("./datas/029/BOCM.csv")
BOCM.index = BOCM.iloc[:,1]
BOCM.index = pd.to_datetime(BOCM.index,format="%Y-%m-%d")
BOCM = BOCM.iloc[:,2:]

BOCMclp = BOCM["Close"]
clprChange = BOCMclp - BOCMclp.shift(1)
clprChange = clprChange.dropna()

#upPrc表示价格上涨
#downPrc表示价格下跌

indexprc = clprChange.index
upPrc = pd.Series(0,index=indexprc)
upPrc[clprChange>0] = clprChange[clprChange>0]
downPrc = pd.Series(0,index=indexprc)
downPrc[clprChange<0] = -clprChange[clprChange<0]

RSIdata = pd.concat([BOCMclp,clprChange,upPrc,downPrc],axis=1)
RSIdata.columns = ["Close","PrcChange","upPrc","downPrc"]
RSIdata.dropna(inplace=True)

SMUP = []
SMDOWN = []
for i in range(6,len(upPrc)+1):
    SMUP.append(np.mean(upPrc.values[(i-6):i],dtype=np.float32))       #如果i=6，values[0:6]，实际上是取0,1,2,3,4,5
    SMDOWN.append(np.mean(downPrc.values[(i-6):i],dtype=np.float32))

RSI6 = [100*SMUP[i]/(SMUP[i]+SMDOWN[i]) for i in range(0,len(SMUP))]
indexRSI = indexprc[5:]
RSI6 = pd.Series(RSI6,index=indexRSI)

UP = pd.Series(SMUP,index=indexRSI)
DOWM = pd.Series(SMDOWN,index=indexRSI)

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.figure(figsize=(20,15),dpi=80)

plt.subplot(411)
BOCMclp.plot(color="k")
plt.ylabel("Close")
plt.title("RSI相关指标")

plt.subplot(412)
UP.plot(color="b")
plt.ylabel("UP")

plt.subplot(413)
DOWM.plot(color="y")
plt.ylabel("DOWN")

plt.subplot(414)
RSI6.plot(color="g")
plt.ylabel("RSI6")
plt.xlabel("data")

plt.show()

