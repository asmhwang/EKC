url1 = 'https://raw.githubusercontent.com/QuantEcon/lecture-python/master/source/_static/lecture_specific/pandas_panel/realwage.csv'
url2 = 'https://raw.githubusercontent.com/QuantEcon/lecture-python/master/source/_static/lecture_specific/pandas_panel/countries.csv'
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
# Display 6 columns for viewing purposes
pd.set_option('display.max_columns', 6)

# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

realwage = pd.read_csv(url1)

print(realwage.head())
realwage = realwage.pivot_table(values='value',
                                index='Time',
                                columns=['Country', 'Series', 'Pay period'])
print(realwage.head())
realwage.index = pd.to_datetime(realwage.index)
print(type(realwage.index))
print (type(realwage.columns))
print(realwage.columns.names)
print(realwage['United States'].head())
print(realwage.stack().head())
print(realwage.stack(level='Country').head())
print(realwage.loc['2015'].stack(level=(1, 2)).transpose().head())
realwage_f = realwage.xs(('Hourly', 'In 2015 constant prices at 2015 USD exchange rates'),
                         level=('Pay period', 'Series'), axis=1)
print(realwage_f.head())

worlddata = pd.read_csv(url2, sep=';')
print(worlddata.head())
worlddata = worlddata[['Country (en)', 'Continent']]
worlddata = worlddata.rename(columns={'Country (en)': 'Country'})
print(worlddata.head())
print(realwage_f.transpose().head())
merged = pd.merge(realwage_f.transpose(), worlddata,
                  how='left', left_index=True, right_on='Country')
print(merged.head())
print(merged[merged['Continent'].isnull()])
missing_continents = {'Korea': 'Asia',
                      'Russian Federation': 'Europe',
                      'Slovak Republic': 'Europe'}

print(merged['Country'].map(missing_continents))
merged['Continent'] = merged['Continent'].fillna(merged['Country'].map(missing_continents))

# Check for whether continents were correctly mapped

print(merged[merged['Country'] == 'Korea'])
replace = ['Central America', 'North America', 'South America']

for country in replace:
    merged['Continent'].replace(to_replace=country,
                                value='America',
                                inplace=True)

merged = merged.set_index(['Continent', 'Country']).sort_index()
print(merged.head())
print(merged.columns)
merged.columns = pd.to_datetime(merged.columns)
merged.columns = merged.columns.rename('Time')
print(merged.columns)
merged = merged.transpose()
print(merged.head())
print(merged.mean().head(10))

print(merged.mean(axis=1).head())
print(merged.groupby(level='Continent', axis=1).mean().head())
print(merged.stack().describe())
grouped = merged.groupby(level='Continent', axis=1)
print(grouped)
print(grouped.size())
continents = grouped.groups.keys()

for continent in continents:
    sns.kdeplot(grouped.get_group(continent).loc['2015'].unstack(), label=continent, fill=True)

plt.title('Real minimum wages in 2015')
plt.xlabel('US dollars')
plt.legend()
plt.show()
