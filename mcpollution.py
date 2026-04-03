import csv
import math
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import pycountry_convert as pc

def country_to_continent(country_name_x, country_name_y):
	try:
	    country_alpha2 = pc.country_name_to_country_alpha2(country_name_x)
	    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
	    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
	    return country_continent_name
	except:
		try:
			country_alpha2 = pc.country_name_to_country_alpha2(country_name_y)
			country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
			country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
			return country_continent_name
		except:
			return ''

col_df = pd.read_csv('cost-of-living_v2.csv')
aqi_df = pd.read_csv('air_pollution_new.csv')
joint_df = pd.merge(col_df, aqi_df, on='city').dropna()

joint_df['continent'] = joint_df.apply(lambda row : country_to_continent(row['country_x'], row['country_y']), axis=1)

joint_df['x3'] = joint_df['x3'].apply(lambda x : float('.'.join(x.split('.')[:2])) if type(x) is str else x)
joint_df['2023'] = joint_df['2023'].apply(lambda x : float('.'.join(x.split('.')[:2])) if type(x) is str else x)

X = joint_df['x3']
Y = joint_df['2023']

def sq(args):
	a, b, c = args
	curve = [a*x**2+b*x+c for x in X]
	rmse = sum((y-pt)**2 for y,pt in zip(Y,curve))**0.5
	return rmse

def exp(args):
	a, b, c, d, e = args
	curve = [a*b**(c*x-d)+e for x in X]
	rmse = sum((y-pt)**2 for y,pt in zip(Y,curve))**0.5
	return rmse

def rat(args):
	a, b = args
	curve = [a/x+b for x in X]
	rmse = sum((y-pt)**2 for y,pt in zip(Y,curve))**0.5
	return rmse

def rat_sq(args):
	a, b, c = args
	curve = [a/(x**2)+b/x+c for x in X]
	rmse = sum((y-pt)**2 for y,pt in zip(Y,curve))**0.5
	return rmse

f_sq = minimize(sq, [1,1,0]).x
f_exp = minimize(exp, [1,1,1,1,0]).x
f_rat = minimize(rat, [1,0]).x
f_rat_sq = minimize(rat_sq, [1,1,0]).x

fitted_line = np.linspace(min(X), max(X), 100)

plt.xlabel("McMeal Price")
plt.ylabel("Air Quality Index")

#continents = set(joint_df['continent'])
continents = ['Asia', 'Europe']
for continent in continents:
	filtered_df = joint_df[joint_df['continent'].str.contains(continent)]
	X = filtered_df['x3']
	Y = filtered_df['2023']
	plt.plot(X, Y, 'o', markersize=2)

for continent in continents:
	filtered_df = joint_df[joint_df['continent'].str.contains(continent)]
	X = filtered_df['x3']
	Y = filtered_df['2023']
	lin_result = stats.linregress(X, Y)
	print(f"{continent} R-squared: {lin_result.rvalue**2}")
	line_domain = np.linspace(min(X), max(X), 100)
	plt.plot(line_domain, (lambda x: lin_result.slope*x+lin_result.intercept)(line_domain))

plt.legend([*continents, *continents])

plt.show()