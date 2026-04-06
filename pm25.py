import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import stats
import pycountry_convert as pc
import statsmodels.api as sm
from linearmodels import PanelOLS
from linearmodels import RandomEffects
from linearmodels.panel.results import compare
from  linearmodels import IV2SLS

new=pd.read_csv('data/pm2_5Emissions.csv',header=0, index_col=0)
popDensity=pd.read_csv('data/population.csv',header=0,index_col=0)
totalPopulation=pd.read_csv('data/totalPop.csv',header=0,index_col=0)
new = new.transpose()
new.index = pd.to_datetime(new.index)
new = new.apply(pd.to_numeric, errors='coerce')
gdp=pd.read_csv('data/1gdpkor.csv', header=0,index_col=0)
gdp= gdp.transpose()
gdp.index = pd.to_datetime(gdp.index)
new = new.groupby(pd.Grouper(freq='Y')).mean()
gdp = gdp.apply(pd.to_numeric, errors='coerce')
gdp = gdp.groupby(pd.Grouper(freq='Y')).mean()
new = new.transpose()
new.columns = pd.MultiIndex.from_product([['PM25'], new.columns])

popDensity = popDensity.transpose()
popDensity.index = pd.to_datetime(popDensity.index)
popDensity = popDensity.apply(pd.to_numeric, errors='coerce')
popDensity = popDensity.groupby(pd.Grouper(freq='Y')).mean()
popDensity = popDensity.transpose()
popDensity.columns = pd.MultiIndex.from_product([['DENSITY'], popDensity.columns])

totalPopulation = totalPopulation.transpose()
totalPopulation.index = pd.to_datetime(totalPopulation.index)
totalPopulation = totalPopulation.apply(pd.to_numeric, errors='coerce')
totalPopulation = totalPopulation.groupby(pd.Grouper(freq='Y')).mean()
totalPopulation = totalPopulation.transpose()
totalPopulation.columns = pd.MultiIndex.from_product([['POP'], totalPopulation.columns])

gdp = gdp.transpose()
gdp.columns = pd.MultiIndex.from_product([['GDP'], gdp.columns])

merged = pd.merge(new, gdp, left_index=True, right_index=True)
merged = pd.merge(merged, popDensity, left_index=True, right_index=True)
merged = pd.merge(merged, totalPopulation, left_index=True, right_index=True)
print(merged)
merged = merged.stack()
merged.index.names = ['Region', 'Year']
merged['Year'] = merged.index.get_level_values('Year')
merged['PM25'] = merged['PM25'] / merged['POP']
merged['PM25'] = merged['PM25'].apply(lambda x: np.log(x))
merged['GDP'] = merged['GDP'].apply(lambda x: np.log(x))
merged['GDP_square'] = merged['GDP'].apply(lambda x: x**2)
#merged['DENSITY'] = merged['DENSITY'].apply(lambda x: np.log(x))
print(merged)
exog_vars = ['GDP','GDP_square','DENSITY']
exog = sm.add_constant(merged[exog_vars])
mod = RandomEffects(merged['PM25'], exog)
re_res = mod.fit()
print(re_res)
mod = PanelOLS(merged['PM25'], exog)
fe_res = mod.fit()
print(fe_res)
print(compare({'Fixed': fe_res, 'Random': re_res}))
psi = fe_res.cov - re_res.cov
diff = fe_res.params - re_res.params
W = diff.dot(np.linalg.inv(psi)).dot(diff)
dof = re_res.params.size -1
pvalue = stats.chi2(dof).sf(W)
print("Hausman Test: chisq = {0}, df = {1}, p-value = {2}".format(W, dof, pvalue))
print(fe_res.cov, re_res.cov)
print(fe_res.params, re_res.params)