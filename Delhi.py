import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import stats
import pycountry_convert as pc

new=pd.read_csv('DL001.csv')
new.index = pd.to_datetime(new['From Date'])
print(new.head())
print(new['SO2 (ug/m3)'].groupby(by=[new.index.year, new.index.month]).mean().head(30))