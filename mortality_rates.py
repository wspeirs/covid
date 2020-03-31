import pandas as pd

#
# Compute the morality rate of the virus by looking at other countries
#
global_deaths_df = pd.read_csv('data/global_deaths.csv', header=0)
global_confirmed_df = pd.read_csv('data/global_confirmed.csv', header=0)

# check date ranges
if global_deaths_df.columns[4] != global_confirmed_df.columns[4] or \
   global_deaths_df.columns[-1] != global_confirmed_df.columns[-1]:
    raise ValueError("Date mis-match")

global_data = dict()

# compute total deaths by country
for country, df in global_deaths_df.groupby('Country/Region'):
    total = 0
    global_data[country] = dict()

    for date in global_deaths_df.columns[4:]:
        total += df[date].sum()  # add to our total the deaths for that date
        # print("{} - {}: {}".format(date, country, total))

    global_data[country]['deaths'] = total

# compute total cases by country
for country, df in global_confirmed_df.groupby('Country/Region'):
    total = 0

    for date in global_confirmed_df.columns[4:]:
        total += df[date].sum()  # add to our total the deaths for that date
        # print("{} - {}: {}".format(date, country, total))

    global_data[country]['cases'] = total

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
