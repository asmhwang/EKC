import numpy as np
import pandas as pd
from linearmodels import PanelOLS
from linearmodels import RandomEffects
import statsmodels.api as sm

from linearmodels.datasets import jobtraining
data = jobtraining.load()
year = pd.Categorical(data.year)
data = data.set_index(['fcode', 'year'])
data['year'] = year

exog_vars = ['grant', 'employ']
exog = sm.add_constant(data[exog_vars])
mod = RandomEffects(data.clscrap, exog)
re_res = mod.fit()
print(data)