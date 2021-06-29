import pandas as pd

ssec2011 = pd.read_csv("./datas/027/ssec2011.csv")
ssec2011.index = ssec2011.iloc[:,1]
ssec2011.index = pd.to_datetime(ssec2011.index,format="%Y-%m-%d")
ssec2011 = ssec2011.iloc[:,2:]

close11 = ssec2011["Close"]
open11 = ssec2011["Open"]

##捕捉刻画符合“乌云盖顶”形态的连续两个蜡烛实体
lagclose11 = close11.shift(1)
lagopen11 = open11.shift(1)
cloud = pd.Series(0,index=close11.index)
for i in range(1,len(close11)):                #用数学描述“乌云盖顶”的条件
    if all([lagclose11[i]>lagopen11[i],
            open11[i]>close11[i],
            open11[i]>lagclose11[i],
            close11[i]>lagopen11[i],
            close11[i]<0.5*(lagclose11[i]+lagopen11[i])]):
        cloud[i]=1

#定义前期上升趋势
trend = pd.Series(0,index=close11.index)
for i in range(2,len(close11)):
    if close11[i-1]>close11[i-2]:
        trend[i]=1

#寻找“乌云盖顶”形态
darkcloud = cloud+trend
darkcloud = darkcloud[darkcloud==2]
print(darkcloud)
