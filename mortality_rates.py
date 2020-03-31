import pandas as pd
from compute_us import compute_us

#
# Compute the morality rate of the virus by looking at countries confirmed cases and deaths
#
global_deaths_df = pd.read_csv('data/global_deaths.csv', header=0)
global_confirmed_df = pd.read_csv('data/global_confirmed.csv', header=0)

# check that the last dates match
if global_deaths_df.columns[-1] != global_confirmed_df.columns[-1]:
    raise ValueError("Last dates are not the same")

global_data = dict()
date = global_deaths_df.columns[-1]

# compute total deaths by country
for country, df in global_deaths_df.groupby('Country/Region'):
    global_data[country] = dict()
    global_data[country]['deaths'] = df[date].sum()

# compute total cases by country
for country, df in global_confirmed_df.groupby('Country/Region'):
    global_data[country]['cases'] = df[date].sum()

# construct a new DataFrame with mortality rates
global_data_df = pd.DataFrame(global_data)
global_data_df = global_data_df.T
global_data_df['mortality'] = global_data_df['deaths'] / global_data_df['cases']

# discard anything that's zero
mortality_rates = global_data_df[global_data_df['mortality'] > 0.0]['mortality']

avg_mortality = mortality_rates.mean()
med_mortality = mortality_rates.median()

print("Average global mortality: {:.02}%".format(avg_mortality * 100.0))
print("Median global mortality: {:.02}%".format(med_mortality * 100.0))

# look at the US
us_df = compute_us()

print("US mortality: {:.02}%".format(us_df.iloc[-1]['mortality'] * 100.0))

