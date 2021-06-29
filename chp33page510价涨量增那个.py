import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter,WeekdayLocator,DateLocator,MONDAY,date2num
from mpl_finance import candlestick_ohlc

CJSecurities = pd.read_csv("./datas/033/CJSecurities.csv",index_col='Date')
CJSecurities = CJSecurities.iloc[:,1:]
CJSecurities.index = pd.to_datetime(CJSecurities.index)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 参数candletitle：表示K线图的标题
# 参数bartitle：表示成交量柱状图的标题
def candleVolume(seriesData,candletitle='a',bartitle=''):
    Date = [date2num(date) for date in seriesData.index]
    seriesData.index = list(range(len(Date)))
    seriesData['Date'] = Date
    listData = zip(seriesData.index,seriesData.Open,seriesData.High,seriesData.Low,seriesData.Close)
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    for ax in ax1,ax2:
        mondays = WeekdayLocator(MONDAY)
        weekFormatter = DateFormatter("%m/%d/%y")
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(DateLocator())
        ax.xaxis.set_major_formatter(weekFormatter)
        ax.grid(True)

    ax1.set_ylim(seriesData.Low.min()-2,seriesData.High.max()+2)
    ax1.set_ylabel("蜡烛图及收盘价线")
    candlestick_ohlc(ax1,listData,width=0.7,colorup='r',colordown='g')
    plt.setp(plt.gca().get_xticklabels(),rotation=20,horizontalalignment='center')
    ax1.autoscale_view()
    ax1.set_title(candletitle)

    ax1.plot(seriesData,seriesData.Close,color='black',label='收盘价')
    ax1.legend(loc='best')

    ax2.set_ylabel("成交量")
    ax2.set_ylim(0,seriesData.Volume.max()*3)
    ax2.bar(np.array(Date)[np.array(seriesData.Close>=seriesData.Open)],
            height=seriesData.iloc[:,4][np.array(seriesData.Close>=seriesData.Open)],
            color='r',align='center')
    ax2.bar(np.array(Date)[np.array(seriesData.Close<seriesData.Open)],
            height=seriesData.iloc[:,4][np.array(seriesData.Close<seriesData.Open)],
            coloe='g',align='center')
    ax2.set_title(bartitle)
    return (plt.show())

CJSecurities1 = CJSecurities['2015-04-01':'2015-04-30']
candleVolume(CJSecurities1,candletitle="长江证券2015年4月蜡烛图",
             bartitle="长江证券2015年4月份日成交量")
