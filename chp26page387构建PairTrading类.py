import numpy as np
import re
from arch.unitroot import ADF
import statsmodels.api as sm

class PairTrading:
    def SSD(self,priceX,priceY):
        if priceX is None or priceY is None:
            print("缺少价格序列。")
        returnX = (priceX-priceX.shift(1))/priceX.shift(1)[1:]
        returnY = (priceY-priceY.shift(1))/priceY.shift(1)[1:]
        standardX = (1+returnX).cumprod()
        standardY = (1+returnY).cumprod()
        SSD = np.sum((standardX-standardY)**2)
        return (SSD)
    def SSDSpread(self,priceX,priceY):
        if priceX is None or priceY is None:
            print("缺少价格序列。")
        retX = (priceX-priceX.shift(1))/priceX.shift(1)[1:]
        retY = (priceY-priceY.shift(1))/priceY.shift(1)[1:]
        standardX = (1+retX).cumprod()
        standardY = (1+retY).cumprod()
        spread = standardY-standardX
        return (spread)
    def Cointegration(self,priceX,priceY):
        if priceX is None or priceY is None:
            print("缺少价格序列。")
        priceX = np.log(priceX)
        priceY = np.log(priceY)
        results = sm.OLS(priceY,sm.add_constant(priceX)).fit()
        resid = results.resid
        adfSpread = ADF(resid)
        if adfSpread.pvalue>=0.05:
            print("""交易价格不具有协整关系。
            P-value of ADF test:%f
            Coefficients of regression:
            Intercept:%f
            Beta:%f
            """%(adfSpread.pvalue,results.params[0],results.params[1]))
            return(None)
        else:
            print("""交易价格具有协整关系。
            P-value of ADF test:%f
            Coefficients of regression:
            Intercept:%f
            Beta:%f
            """%(adfSpread.pvalue,results.params[0],results.params[1]))
            return (results.params[0],results.params[1])
    def CointegrationSpread(self,priceX,priceY,Period):
        if priceX is None or priceY is None:
            print("缺少价格序列。")
        if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',Period)):
            print("形成期或交易期格式错误。")
        formX = priceX[Period.split(":")[0]:Period.split(":")[1]]
        formY = priceY[Period.split(":")[0]:Period.split(":")[1]]
        coefficients = self.Cointegration(formX,formY)
        if coefficients is None:
            print("未形成协整关系，无法配对。")
        else:
            spread = (np.log(priceY[Period.split(":")[0]:Period.split(":")[1]])
                      - coefficients[0] - coefficients[1]*np.log(priceX[Period.split(":")[0]:
                        Period.split(":")[1]]))
            return (spread)
    def calculateBound(self,priceX,priceY,method,formPeriod,width=1.5):
        if not (re.fullmatch('\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}',formPeriod)):
            print("形成期格式错误。")
        if method == "SSD":
            spread = self.SSDSpread(priceX[formPeriod.split(":")[0]:formPeriod.split(":")[1]],
                                    priceY[formPeriod.split(":")[0]:formPeriod.split(":")[1]])
            miu = np.mean(spread)
            std = np.std(spread)
            UpperBound = miu + width*std
            LowerBound = miu - width*std
            return (UpperBound,LowerBound)
        elif method == "Cointegration":
            spread = self.CointegrationSpread(priceX,priceY,formPeriod)
            miu = np.mean(spread)
            std = np.std(spread)
            UpperBound = miu + width*std
            LowerBound = miu - width*std
            return (UpperBound,LowerBound)
        else:
            print("不存在该方法。请选择“SSD”或者“Cointegration”方法。")



#测试
import pandas as pd
sh = pd.read_csv("./datas/026/sh50p.csv",index_col="Trddt")
sh.index = pd.to_datetime(sh.index)
formPeriod = '2014-01-01:2015-01-01'
tradePeriod = '2015-01-01:2015-06-30'
priceA = sh["601988"]
priceB = sh["600000"]
priceAform = priceA[formPeriod.split(":")[0]:formPeriod.split(":")[1]]
priceBform = priceB[formPeriod.split(":")[0]:formPeriod.split(":")[1]]
priceAtrade = priceA[tradePeriod.split(":")[0]:tradePeriod.split(":")[1]]
priceBtrade = priceB[tradePeriod.split(":")[0]:tradePeriod.split(":")[1]]
pt = PairTrading()

bound = pt.calculateBound(priceA,priceB,"Cointegration",formPeriod,width=1.2)
print(bound)


