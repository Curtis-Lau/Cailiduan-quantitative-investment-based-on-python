from scipy import linalg
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import ffn
import pandas as pd

class MeanVariance():
    def __init__(self,returns):
        self.returns = returns

    #定义最小化方差的函数，即求解二次规划,算出每个资产的比重w
    def minVar(self,goalRet):
        covariances = np.array(self.returns.cov())
        means = np.array(self.returns.mean())
        L1 = np.append(np.append(covariances.swapaxes(0,1),[means],0),[np.ones(len(means))],0).swapaxes(0,1)
        L2 = list(np.ones(len(means)))
        L2.extend([0,0])
        L3 = list(means)
        L3.extend([0,0])
        L4 = np.array([L2,L3])
        L = np.append(L1,L4,0)
        results = linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
        return (np.array([list(self.returns.columns),results[:-2]]))  #————结果是权重w

    #定义绘制最小方差前沿曲线函数
    def frontierCurve(self):
        goals = [x/500000 for x in range(-100,4000)]
        variances = list(map(lambda x:self.calVar(self.minVar(x)[1,:].astype(float)),goals))
        plt.plot(variances,goals)
        plt.show()

    #给定各资产的比例，计算收益率
    def meanRet(self,fracs):
        meanRisky = ffn.to_returns(self.returns).mean()
        assert len(meanRisky) ==len(fracs),'length of fractions must be equal to number of asserts'
        return (np.sum(np.multiply(meanRisky,np.array(fracs))))

    #给定各资产的比例，计算收益率方差
    def calVar(self,fracs):
        return (np.dot(np.dot(fracs,self.returns.cov()),fracs))

def stocks():
    stock = pd.read_table("./datas/019/stock.txt",sep="\t",index_col="Trddt")
    fjgs = stock[stock["Stkcd"]==2599]["Dretwd"]
    fjgs.name="fjgs"
    zndl = stock[stock["Stkcd"]==2600]["Dretwd"]
    zndl.name="zndl"
    sykj = stock[stock["Stkcd"]==2601]["Dretwd"]
    sykj.name="sykj"
    hxyh = stock[stock["Stkcd"]==2602]["Dretwd"]
    hxyh.name="hxyh"
    byjc = stock[stock["Stkcd"]==2603]["Dretwd"]
    byjc.name="byjc"

    sh_return = pd.concat([byjc,fjgs,hxyh,sykj,zndl],axis=1).dropna()
    sh_return.index = pd.to_datetime(sh_return.index)

    Class = MeanVariance(sh_return)
    minVar = Class.minVar(0.3/245)
    print(minVar)
    Class.frontierCurve()       #——————存在问题，不能打印图片

stocks()

