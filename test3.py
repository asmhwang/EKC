import numpy as np
from sklearn.linear_model import LinearRegression
import csv
import matplotlib.pyplot as plt

solids = np.array([])
hardness = np.array([])

with open('water_potability.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data_list = list(csv_reader)
    solids = np.array([float(row[2]) for row in data_list[1:]]).reshape((-1, 1))
    hardness = np.array([float(row[1]) for row in data_list[1:]])
    


model = LinearRegression().fit(solids, hardness)
r_sq = model.score(solids, hardness)
print(f"coefficient of determination: {r_sq}")
print(f"intercept: {model.intercept_}")
print(f"slope: {model.coef_}")
intercept = model.intercept_
coefficient = model.coef_[0]
plt.plot(solids, hardness, "o")
plt.plot(np.array([0, 60000]), np.array([intercept, 60000*coefficient]))
plt.show()