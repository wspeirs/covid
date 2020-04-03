import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from math import pi, sin
from dateutil.parser import parse
from collections import defaultdict
from jinja2 import Template


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
    # "China",
    # "France",
    # "Germany",
     # "Indonesia",
    # "Iran",
    ("Italy", datetime.date(year=2020, month=3, day=8) ),
    # "Korea, South",
     # "Netherlands",
     # "Portugal",
    ("Spain", datetime.date(year=2020, month=3, day=15) ),
     # "Sweden",
     # "Switzerland",
     # "Turkey",
    ("United Kingdom", datetime.date(year=2020, month=3, day=24) )
]

global_deaths_df = pd.read_csv('data/global_deaths.csv', header=0)

data = defaultdict(lambda: dict())

for date in global_deaths_df.columns[4:]:
    date_dt = parse(date).date()

    for country, df in global_deaths_df.groupby('Country/Region'):
        if country not in set(map(lambda t: t[0], countries)):
            continue

        data[country][date_dt] = df[date].sum()

df = pd.DataFrame(data)
df = df.sort_index()

predictions = defaultdict(lambda : dict())

# go through dates to generate predictions through time
for data_date in global_deaths_df.columns[73:]:
    data_date = parse(data_date).date()  # convert to datetime

    # go through each country and lockdown date
    for country, lockdown_date in list(countries):
        df_diff = pd.DataFrame(df[country])
        df_diff = df_diff[df_diff.index <= data_date]

        # convert from raw counts to difference with a 3-day moving average
        df_diff[country] = df[country].diff().rolling(window=3).mean()

        df_diff = df_diff.fillna(value=0)
        # print(df_diff)

        # fit the sin curve
        clear_date = fit_sin(df_diff, country, lockdown_date)
        deaths = df_diff['computed'].sum()

        print("Clear by: {} with {} deaths".format(clear_date, deaths))

        # record the prediction
        predictions[data_date][country] = '{} - {:,}'.format(clear_date.strftime('%B %-d'), deaths)

        # plot the results if it's the last date
        if data_date == parse(global_deaths_df.columns[-1]).date():
            ax = df_diff.plot(figsize=(10,5))
            (start, end) = ax.get_xlim()
            ax.xaxis.set_ticks(np.arange(start, end, 6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m/%-d'))
            plt.ylabel('Deaths by Day')
            plt.grid(which='both', axis='x')

            # plt.show()
            plt.savefig('site/img/{}.png'.format(country.lower().replace(' ', '_')))

# convert from dictionary to sorted tuple list
predictions = [(d, predictions[d]) for d in sorted(predictions.keys(), reverse=True)]
print(predictions)

with open('site/index.template', 'r') as f:
    t = Template(f.read())
    out = t.render(predictions=predictions)

    with open('site/index.html', 'w') as f_out:
        f_out.write(out)
