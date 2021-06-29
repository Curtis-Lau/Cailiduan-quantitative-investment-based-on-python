import pandas as pd
import statsmodels.api as sm
import numpy as np

penn = pd.read_excel("./datas/017/Penn World Table.xlsx",2)   #sheetname默认为0，这里用的是第三个表
model = sm.OLS(np.log(penn["rgdpe"]),sm.add_constant(penn.iloc[:,-6:])).fit()
print(model.summary())
#pl_c和pl_k不显著，看是否存在共线性
penn.iloc[:,-6:].corr()    #存在共线性，剔除这两个变量
print("*"*100)

model2 = sm.OLS(np.log(penn["rgdpe"]),sm.add_constant(penn.iloc[:,-5:-1])).fit()
print(model2.summary())    #结果显著