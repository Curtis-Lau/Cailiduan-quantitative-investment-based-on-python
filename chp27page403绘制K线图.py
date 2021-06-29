import pandas as pd
from matplotlib.dates import DateFormatter,WeekdayLocator,DateLocator,MONDAY,date2num
from datetime import datetime
import mpl_finance    #——有问题？？
from matplotlib import pyplot as plt

ssec2015 = pd.read_csv("./datas/027/ssec2015.csv")
ssec2015 = ssec2015.iloc[:,1:]
ssec2015["Date"] = [date2num(datetime.strptime(date,"%Y-%m-%d")) for date in ssec2015["Date"]]

#candlestick_ohlc()传入的数据对象为序列类型，需要将ssec2015（DataFrame）转换为列表
ssec2015list = []
for i in range(len(ssec2015)):
    ssec2015list.append(ssec2015.iloc[i,:])
ax = plt.subplot()
mondays = WeekdayLocator(MONDAY)
weekFormatter = DateFormatter("%y %b %d")      #设定格式
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(DateLocator())
ax.xaxis.set_major_formatter(weekFormatter)
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
ax.set_title("上证综指2015年3月份K线图")
mpl_finance.candlestick_ohlc(ax,ssec2015list,colorup="r",colordown="g")
plt.setp(plt.gca().get_xticklabels,rotation=50,horizontalalignment="center")
plt.show()
