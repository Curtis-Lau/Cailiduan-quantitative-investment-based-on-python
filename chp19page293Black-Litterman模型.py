import numpy as np
from scipy import linalg
import pandas as pd

def blacklitterman(returns,tau,P,Q):
    miu = returns.mean()   #历史收益率均值作为先验预期收益的期望
    sigma = returns.cov()  #历史收益率的协方差作为先验预期收益的协方差
    pi1 = miu
    ts = tau*sigma
    Omega = np.dot(np.dot(P,ts),P.T)*np.eye(Q.shape[0])
    middle = linalg.inv(np.dot(np.dot(P,ts),P.T) + Omega)
    #后验分布的期望收益率
    ER = np.expand_dims(pi1,axis=0).T +np.dot(np.dot(np.dot(ts,P.T),middle),(Q-np.expand_dims(np.dot(P,pi1.T),axis=1)))
    #后验分布的协方差
    posteriorSigma = sigma + ts - np.dot(ts.dot(P.T).dot(middle).dot(P),ts)
    return [ER,posteriorSigma]

#构造投资人的分析
#构建资产选择矩阵P，假设分析师认为：
#1.前4只股票收益率为日均0.3%
#2.两只交通股日均收益比浙能电力高0.1%
pick1 = np.array([1,0,1,1,1])
q1 = np.array([0.003*4])
pick2 = np.array([0.5,0.5,0,0,-1])
q2 = np.array([0.001])
P = np.array([pick1,pick2])
Q = np.array([q1,q2])

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

#修正后验收益
res = blacklitterman(sh_return,0.1,P,Q)
# p_mean = pd.DataFrame(res[0],index=sh_return.columns,columns=["posterior_mean"])
# p_cov = res[1]

#利用马可维茨模型进行资产配置
def blminVar(blres,goalRet):
    covs = np.array(blres[1])
    means = np.array(blres[0])
    L1 = np.append(np.append((covs.swapaxes(0,1)),[means.flatten()],0),
                             [np.ones(len(means))],0).swapaxes(0,1)
    L2 = list(np.ones(len(means)))
    L2.extend([0,0])
    L3 = list(means)
    L3.extend([0,0])
    L4 = np.array([L2,L3])
    L = np.append(L1,L4,0)
    results = linalg.solve(L, np.append(np.zeros(len(means)), [1, goalRet], 0))
    return (pd.DataFrame(results[:-2],index=blres[1].columns,columns=["p_weight"]))

w = blminVar(res,0.8)
print(w)


