import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import WeekdayLocator,DateLocator,DateFormatter,MONDAY,date2num
import mpl_finance as mplf

plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False

Vanke = pd.read_csv("./datas/028/Vanke.csv")
Vanke.index = Vanke.iloc[:,1]
Vanke.index = pd.to_datetime(Vanke.index)
Vanke = Vanke.iloc[:,2:]
Close = Vanke["Close"]

def momentum(price,period):
    lagprice = price.shift(period)
    momen = price - lagprice
    momen = momen.dropna()
    return (momen)

momen35 = momentum(Close,35)

#定义candleLinePlots()函数
def candleLinePlots(candleData,candleTitle='a',**kwargs):
    Data = [date2num(date) for date in candleData.index]
    candleData.loc[:,"Data"] = Data
    listData = []
    for i in range(len(candleData)):
        a = [candleData["Data"][i],candleData["Open"][i],
             candleData["High"][i],candleData["Low"][i],
             candleData["Close"][i]]
        listData.append(a)
    #如果不定长参数无取值，只蜡烛图
    ax = plt.subplot()
    flag = 0
    #如果不定长参数有值，则分成两个子图
    if kwargs:
        if kwargs["splitFigures"]:                #有问题？
            ax = plt.subplot(211)
            ax2 = plt.subplot(212)
            flag = 1
    #如果无参数splitFigures，则只画一个图形框
    #如果有参数splitFigures，则画出两个图形框
        for key in kwargs:
            if key=="title":
                ax2.set_title(kwargs[key])
            if key=="ylabel":
                ax2.set_ylabel(kwargs[key])
            if key=="grid":
                ax2.grid(kwargs[key])
            if key=="Data":
                plt.sca(ax)
                if flag:
                    plt.sca(ax2)

                #一维数组
                if kwargs[key].ndim==1:
                    plt.plot(kwargs[key],color="k",label=kwargs[key].name)
                    plt.legend(loc="best")
                #二维数组有两个columns
                elif all([kwargs[key].ndim==2,len(kwargs[key].columns)==2]):
                    plt.plot(kwargs[key].iloc[:,0],color="k",label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],linstyle="dashed",label=kwargs[key].iloc[:,1].name)
                    plt.legend(loc="best")
                elif all([kwargs[key].ndim==2,len(kwargs[key].columns)==3]):
                    plt.plot(kwargs[key].iloc[:,0],color="k",label=kwargs[key].iloc[:,0].name)
                    plt.plot(kwargs[key].iloc[:,1],linestyle="dashed",label=kwargs[key].iloc[:,1].name)
                    plt.bar(left=kwargs[key].iloc[:,2].index,height=kwargs[key].iloc[:,2],color="r",label=kwargs[key].iloc[:,2].name)
                    plt.legend(loc="best")

    mondays = WeekdayLocator(MONDAY)
    weekFormatter = DateFormatter("%y %b %d")
    ax.axis.set_major_locator(mondays)
    ax.axis.set_minor_locator(DateLocator())
    ax.axis.set_major_formatter(weekFormatter)
    plt.sca(ax)
    mplf.candlestick_ohlc(ax,listData,width=0.7,colorup="r",colordown="g")
    ax.set_title(candleTitle)
    plt.setp(ax.get_xticklabels(),rotation=20,horizontalalignment="center")
    ax.autoscale_view()
    return(plt.show())

candleLinePlots(Vanke["2015"],candleTitle="万科股票2015年日K线图",
                Data=momen35["2015"],title="35日动量",ylabel="35日动量")

