import numpy as np
from sklearn.linear_model import LinearRegression
import csv
import matplotlib.pyplot as plt
import math

col_csv = open('cost-of-living_v2.csv')
aqi_csv = open('air_pollution_new.csv')
col_reader = csv.reader(col_csv, delimiter=',')
aqi_reader = csv.reader(aqi_csv, delimiter=',')
col_list = list(col_reader)
aqi_list = list(aqi_reader)
col_cities = [row[0] for row in col_list[1:]]
aqi_cities = [row[0] for row in aqi_list[1:]]
common_cities = set(col_cities) & set(aqi_cities)
x = []
y = []
for city in common_cities:
	x.append([float(row[4]) for row in col_list if row[0] == city][0])
	y.append([float('.'.join(row[8].split('.')[:2])) for row in aqi_list if row[0] == city][0])

nan_index = []
for i in range(0, len(common_cities)):
	if math.isnan(x[i]) or math.isnan(y[i]):
		nan_index.append(i)

for i in sorted(nan_index, reverse=True):
	del x[i]
	del y[i]
x= np.array(x).reshape((-1, 1))
y = np.array(y)
x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(x)
model = LinearRegression().fit(x_, y)
r_sq = model.score(x_, y)
print(f"coefficient of determination: {r_sq}")
print(f"intercept: {model.intercept_}")
print(f"slope: {model.coef_}")
intercept = model.intercept_
coefficient = model.coef_[0]
plt.plot(x, y, "o")
plt.plot(np.array([0, 18]), np.array([intercept, 18*coefficient]))
plt.show()