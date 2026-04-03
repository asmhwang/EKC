import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import stats
import pycountry_convert as pc

new=pd.read_csv('3korco2.csv', header=0, index_col=0)
new = new.transpose()
new.index = pd.to_datetime(new.index.map(lambda x : x[:-2]))
new = new.apply(pd.to_numeric, errors='coerce')
gdp=pd.read_csv('1gdpkor.csv', header=[0,1],index_col=0)
gdp= gdp.transpose()
gdp = gdp[gdp.index.isin(['1인당 지역내총생산'], level=1)].reset_index(level=1, drop=True)
gdp.index = pd.to_datetime(gdp.index)
new = new.groupby(pd.Grouper(freq='Y')).mean()
gdp = gdp.apply(pd.to_numeric, errors='coerce')
gdp = gdp.groupby(pd.Grouper(freq='Y')).mean()
new = new.transpose()
new.columns = pd.MultiIndex.from_product([['CO'], new.columns])

gdp = gdp.transpose()
gdp.columns = pd.MultiIndex.from_product([['GDP'], gdp.columns])

merged = pd.merge(new, gdp, left_index=True, right_index=True)

print(merged)
X=(merged['GDP'].transpose())['제주특별자치도']
Y=(merged['CO'].transpose())['제주특별자치도']
plt.plot(X, Y, 'o', markersize=2)
plt.show()
