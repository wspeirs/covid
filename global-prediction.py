import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from fit import fit_sin
from dateutil.parser import parse
from collections import defaultdict
from jinja2 import Template
from math import floor

# ensure we can print all rows
pd.set_option('display.max_rows', None)

global_deaths_df = pd.read_csv('data/global_deaths.csv', header=0)

countries = [
    # "Belgium",
     # "Brazil",
    # "China",
    # "France",
    # "Germany",
     # "Indonesia",
    # "Iran",
    ("Italy", datetime.date(year=2020, month=3, day=8)),
    # "Korea, South",
     # "Netherlands",
     # "Portugal",
    ("Spain", datetime.date(year=2020, month=3, day=15)),
    ("Sweden", parse(global_deaths_df.columns[-1]).date()),
     # "Switzerland",
     # "Turkey",
    ("United Kingdom", datetime.date(year=2020, month=3, day=24))
]

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
for data_date in global_deaths_df.columns[-5:]:
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
        predictions[data_date][country] = '{} - {:,}'.format(clear_date.strftime('%B %-d'), floor(deaths))

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
            plt.close()

# convert from dictionary to sorted tuple list
predictions = [(d, predictions[d]) for d in sorted(predictions.keys(), reverse=True)]
print(predictions)

with open('site/index.template', 'r') as f:
    t = Template(f.read())
    out = t.render(predictions=predictions)

    with open('site/index.html', 'w') as f_out:
        f_out.write(out)
