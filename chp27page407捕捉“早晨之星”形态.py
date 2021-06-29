import pandas as pd

ssec2012 = pd.read_csv("./datas/027/ssec2012.csv")
ssec2012.index = ssec2012.iloc[:,1]
ssec2012.index = pd.to_datetime(ssec2012.index,format="%Y-%m-%d")
ssec2012 = ssec2012.iloc[:,2:]

#提取收盘价数据
Close = ssec2012["Close"]

#提取开盘价数据
Open = ssec2012["Open"]

#计算每一个交易日期的收盘价与开盘价的差值CL_OP
ClOp = Close - Open

#简要总结收盘价与开盘价差值的分布情况
# print(ClOp.describe())

##捕捉绿色实体、十字形和红色实体
Shape = [0,0,0]
lag1ClOp = ClOp.shift(1)
lag2ClOp = ClOp.shift(2)

for i in range(3,len(ClOp)):
    if all([lag2ClOp[i]<-11,abs(lag1ClOp[i])<2,ClOp[i]>6,abs(ClOp[i])>abs(lag2ClOp[i]*0.5)]):
        Shape.append(1)      #给定一个标准，按照这个标准找“早晨之星”
    else:
        Shape.append(0)

#查看Shape中元素第一次取值为1所在的index
# print(Shape.index(1))

##捕捉十字形实体位置
lagOpen = Open.shift(1)
lagClose = Close.shift(1)
lag2Close = Close.shift(2)

Doji = [0,0,0]
for i in range(3,len(Open),1):
    if all([lagOpen[i]<Open[i],lagOpen[i]<lag2Close[i],lagOpen[i]<Open[i],(lagClose[i]<lag2Close[i])]):
        Doji.append(1)
    else:
        Doji.append(0)

##刻画下跌趋势
#先计算收益率
ret = Close/Close.shift(1)-1
lag1ret = ret.shift(1)
lag2ret = ret.shift(2)

#寻找下降趋势
Trend = [0,0,0]
for i in range(3,len(ret)):
    if all([lag1ret[i]<0,lag2ret[i]<0]):
        Trend.append(1)
    else:
        Trend.append(0)

##完成上述3个条件，让python自动寻找“早晨之星”
StarSig = []
for i in range(len(Trend)):
    if all([Shape[i]==1,Doji[i]==1,Trend[i]==1]):
        StarSig.append(1)
    else:
        StarSig.append(0)

#捕捉上证综指2012年出现“早晨之星”形态的日期
for i in range(len(StarSig)):
    if StarSig[i]==1:
        print(ssec2012.index[i])
