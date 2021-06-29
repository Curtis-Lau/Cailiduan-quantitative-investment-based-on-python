import pandas as pd
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols

#单因素方差分析——不同行业的股票收益率是否一样
year_return = pd.read_csv("./datas/016/TRD_Year.csv",encoding="gbk")

model1 = ols("Return ~C(Industry)",data=year_return.dropna()).fit()
table1 = anova.anova_lm(model1)
print(table1)
print("*"*100)

PSID = pd.read_csv("./datas/016/PSID.csv")
#多因素方差分析
model2 = ols("earnings~C(married)+C(educatn)",data=PSID.dropna()).fit()
table2 = anova.anova_lm(model2)
print(table2)
print("*"*100)

#析因方差分析——多因素加上交叉项
model3 = ols("earnings~C(married)*C(educatn)",data=PSID.dropna()).fit()
table3 = anova.anova_lm(model3)
print(table3)

 