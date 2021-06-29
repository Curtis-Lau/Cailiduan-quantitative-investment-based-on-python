import pandas as pd
import numpy as np

def rsi(price,period=6):
    closepriceChange = price - price.shift(1)
    closepriceChange.dropna(inplace=True)
    indexprc = closepriceChange.index

    upPrc = pd.Series(0,index=indexprc)
    upPrc[closepriceChange>0] = closepriceChange[closepriceChange>0]
    downPrc = pd.Series(0,index=indexprc)
    downPrc[closepriceChange<0] = -closepriceChange[closepriceChange<0]

    rsidata = pd.concat([price,closepriceChange,upPrc,downPrc],axis=1)
    rsidata.columns = ["Close","PrcChange","upPrc","downPrc"]
    rsidata.dropna(inplace=True)

    SMUP = []
    SMDOWN = []
    for i in range(period,len(upPrc)+1):
        SMUP.append(np.mean(upPrc.values[(i-period):i],dtype=np.float32))
        SMDOWN.append(np.mean(downPrc.values[(i-period):i],dtype=np.float32))

    rsi = [100*SMUP[i]/(SMUP[i]+SMDOWN[i]) for i in range(0,len(SMUP))]
    indexRsi = indexprc[(period-1):]
    rsi = pd.Series(rsi,index=indexRsi)
    return (rsi)

#测试12日相对强弱指标
BOCM = pd.read_csv("./datas/029/BOCM.csv")
BOCM.index = BOCM.iloc[:,1]
BOCM.index = pd.to_datetime(BOCM.index,format="%Y-%m-%d")
BOCM = BOCM.iloc[:,2:]

BOCMclp = BOCM["Close"]
rsi12 = rsi(BOCMclp,12)
print(rsi12)


