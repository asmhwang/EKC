import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import stats
import pycountry_convert as pc

new=pd.read_csv('gdpKor.csv', header=0, index_col=0)