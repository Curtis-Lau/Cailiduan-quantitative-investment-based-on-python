import pandas as pd
import matplotlib.pyplot as plt

TRD_Index = pd.read_csv("./datas/014/TRD_Index.txt",sep="\t")

#获取上证综指数据，代码为“000001”
SHindex = TRD_Index[TRD_Index["Indexcd"]==1]

#获取深证综指数据，代码为“399106”
SZindex = TRD_Index[TRD_Index["Indexcd"]==399106]

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams['axes.unicode_minus']=False

#绘制上证综指和深证综指收益率的散点图
plt.scatter(SHindex["Retindex"],SZindex["Retindex"])
plt.title("上证综指与深证综指收益率的散点图")
plt.xlabel("上证综指收益率")
plt.ylabel("深证综指收益率")
plt.show()

#计算上证综指与深证综指收益率的相关系数
SZindex.index = SHindex.index
corr = SZindex["Retindex"].corr(SHindex["Retindex"])
print(corr)
