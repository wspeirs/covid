import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from math import pi, sin
from compute_us import compute_us
from dateutil.parser import parse
from collections import defaultdict


# ensure we can print all rows
pd.set_option('display.max_rows', None)


def fit_sin(df, country, lockdown_date):
    prev_first_death_date = None
    prev_diff = None
    first_death_date = df[country].ne(0).idxmax() - datetime.timedelta(days=1)

    # have to keep these out of the loop because we change the length of the index
    i = -1
    latest_date = df.index[-1]
    latest_deaths = df[country][-1]

    while latest_deaths == 0.0:
        i -= 1
        latest_date = df.index[i]
        latest_deaths = df[country][i]

    while True:
        peak_date = lockdown_date + datetime.timedelta(days=24)  # we assume a peak 24 days after the lock-down
        last_death_date = peak_date + datetime.timedelta(days=(peak_date-first_death_date).days)
        duration = (last_death_date-first_death_date).days

        if latest_date < peak_date:
            peak_deaths = latest_deaths / sin((latest_date-first_death_date).days * (pi/duration))
        else:
            peak_deaths = df.loc[peak_date][country]

        df['computed'] = 0  # fill with zeros

        for day in range((last_death_date - first_death_date).days + 1):
            df.at[first_death_date+datetime.timedelta(days=day), 'computed'] = peak_deaths * sin(day * (pi/duration))

        # only compute for the dates we have
        actual = df[country][:latest_date].sum()
        computed = df['computed'][:latest_date].sum()
        diff = abs(actual - computed)

        print("{}: Actual: {} vs Computed: {} = {}".format(first_death_date, actual, computed, diff))

        if prev_diff is None or prev_diff > diff:
            prev_diff = diff
            prev_first_death_date = first_death_date
            first_death_date += datetime.timedelta(days=1)
        else:
            df['computed'] = 0  # fill with zeros

            for day in range((last_death_date - prev_first_death_date).days):
                df.at[prev_first_death_date + datetime.timedelta(days=day), 'computed'] = peak_deaths * sin(day * (pi / duration))

            print("LAST DEATH: {}".format(last_death_date))

            return last_death_date


countries = [
    # "Belgium",
     # "Brazil",
    "China",
    # "France",
    # "Germany",
     # "Indonesia",
    # "Iran",
    # "Italy",
    # "Korea, South",
     # "Netherlands",
     # "Portugal",
    # "Spain",
     # "Sweden",
     # "Switzerland",
     # "Turkey",
    # "United Kingdom",
]

global_deaths_df = pd.read_csv('data/global_deaths.csv', header=0)

# us_df = compute_us()

data = defaultdict(lambda: dict())

for date in global_deaths_df.columns[4:]:
    date_dt = parse(date).date()

    for country, df in global_deaths_df.groupby('Country/Region'):
        if country not in countries:
            continue

        data[country][date_dt] = df[date].sum()

    # if date_dt in us_df.index:
    #     data['US'][date_dt] = us_df.loc[date_dt]['deaths']

df = pd.DataFrame(data)
df = df.sort_index()

print(df)

df_diff = df.copy()

# convert from raw counts to percent change with a 3-day moving average
for country in list(countries): # + ['US']:
    df_diff[country] = df[country].diff().rolling(window=3).mean()

df_diff = df_diff.fillna(value=0)
print(df_diff)

# fit the sin curve
lockdown_date = datetime.date(year=2020, month=1, day=23)
clear_date = fit_sin(df_diff, 'China', lockdown_date)

print("Clear by: {} with {} deaths".format(clear_date, df_diff['computed'].sum()))

# plot the results
# ax = df_diff.plot(figsize=(10,5), title='Deaths by Day')
ax = df_diff.plot(figsize=(10,5))
(start, end) = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start, end, 6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m/%-d'))
plt.ylabel('Deaths by Day')
# plt.ylim(-1, 6)
plt.grid(which='both', axis='x')

# plt.show()
plt.savefig('site/img/china.png')

print()
