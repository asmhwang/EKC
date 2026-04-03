import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy import stats
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

col_df = pd.read_csv('cities_by_gdp.csv')
aqi_df = pd.read_csv('global air pollution dataset.csv')
joint_df = pd.merge(col_df, aqi_df, left_on='Metropolitian Area/City', right_on='City').dropna()

joint_df['continent'] = joint_df.apply(lambda row : country_to_continent(row['Country/Region'], row['Country']), axis=1)
joint_df['gdp per capita'] = joint_df.apply(lambda row : float(row['Official est. GDP(billion US$)'])/float(row['Metropolitian Population'].replace(',',''))*1000000000, axis=1)
joint_df['AQI Value'] = joint_df['AQI Value'].apply(lambda x : float('.'.join(x.split('.')[:2])) if type(x) is str else x)

plt.xlabel("GDP per capita")
plt.ylabel("Air Quality Index")

continents = set(joint_df['continent'])
for continent in continents:
	filtered_df = joint_df[joint_df['continent'].str.contains(continent)]
	X = filtered_df['gdp per capita']
	Y = filtered_df['AQI Value']
	plt.plot(X, Y, 'o', markersize=2)

for continent in continents:
	filtered_df = joint_df[joint_df['continent'].str.contains(continent)]
	X = filtered_df['gdp per capita']
	Y = filtered_df['AQI Value']
	lin_result = stats.linregress(X, Y)
	pearsons_r = stats.pearsonr(X, Y)
	print(f"{continent} R-squared: {lin_result.rvalue**2}")
	print(f"{continent} Pearsons R: {pearsons_r}")
	line_domain = np.linspace(min(X), max(X), 100)
	plt.plot(line_domain, (lambda x: lin_result.slope*x+lin_result.intercept)(line_domain))

X = joint_df['gdp per capita']
Y = joint_df['AQI Value']
lin_result = stats.linregress(X, Y)
pearsons_r = stats.pearsonr(X, Y)
print(f"Global R-squared: {lin_result.rvalue**2}")
print(f"Global Pearsons R: {pearsons_r}")
line_domain = np.linspace(min(X), max(X), 100)
plt.plot(line_domain, (lambda x: lin_result.slope*x+lin_result.intercept)(line_domain))

plt.legend([*continents, *continents, 'Global'])

plt.show()