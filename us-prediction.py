import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from fit import fit_sin
from compute_us import compute_us
from collections import defaultdict
from jinja2 import Template
from math import floor

# ensure we can print all rows
pd.set_option('display.max_rows', None)


states = [
    ("Alabama", datetime.date(year=2020, month=3, day=24)),
    ("Alaska", datetime.date(year=2020, month=3, day=28)),
    ("Arizona", datetime.date(year=2020, month=3, day=31)),
    # ("Arkansas", datetime.date(year=2020, month=3, day=)),
    ("California", datetime.date(year=2020, month=3, day=19)),
    ("Colorado", datetime.date(year=2020, month=3, day=26)),
    ("Connecticut", datetime.date(year=2020, month=3, day=23)),
    ("Delaware", datetime.date(year=2020, month=3, day=24)),
    ("District of Columbia", datetime.date(year=2020, month=4, day=1)),
    ("Florida", datetime.date(year=2020, month=4, day=3)),
    ("Georgia", datetime.date(year=2020, month=4, day=3)),
    ("Hawaii", datetime.date(year=2020, month=3, day=25)),
    ("Idaho", datetime.date(year=2020, month=3, day=25)),
    ("Illinois", datetime.date(year=2020, month=3, day=21)),
    ("Indiana", datetime.date(year=2020, month=3, day=24)),
    # ("Iowa", datetime.date(year=2020, month=3, day=)),
    ("Kansas", datetime.date(year=2020, month=3, day=30)),
    ("Kentucky", datetime.date(year=2020, month=3, day=26)),
    ("Louisiana", datetime.date(year=2020, month=3, day=23)),
    ("Maine", datetime.date(year=2020, month=4, day=2)),
    ("Maryland", datetime.date(year=2020, month=3, day=30)),
    ("Massachusetts", datetime.date(year=2020, month=3, day=24)),
    ("Michigan", datetime.date(year=2020, month=3, day=24)),
    ("Minnesota", datetime.date(year=2020, month=3, day=27)),
    ("Mississippi", datetime.date(year=2020, month=4, day=3)),
    ("Missouri", datetime.date(year=2020, month=3, day=24)),
    ("Montana", datetime.date(year=2020, month=3, day=28)),
    # ("Nebraska", datetime.date(year=2020, month=3, day=)),
    ("Nevada", datetime.date(year=2020, month=4, day=1)),
    ("New Hampshire", datetime.date(year=2020, month=3, day=27)),
    ("New Jersey", datetime.date(year=2020, month=3, day=21)),
    ("New Mexico", datetime.date(year=2020, month=3, day=24)),
    ("New York", datetime.date(year=2020, month=3, day=22)),
    ("North Carolina", datetime.date(year=2020, month=3, day=30)),
    # ("North Dakota", datetime.date(year=2020, month=3, day=)),
    ("Ohio", datetime.date(year=2020, month=3, day=23)),
    ("Oklahoma", datetime.date(year=2020, month=3, day=28)),
    ("Oregon", datetime.date(year=2020, month=3, day=23)),
    ("Pennsylvania", datetime.date(year=2020, month=4, day=1)),
    ("Puerto Rico", datetime.date(year=2020, month=3, day=15)),
    ("Rhode Island", datetime.date(year=2020, month=3, day=28)),
    ("South Carolina", datetime.date(year=2020, month=3, day=29)),
    # ("South Dakota", datetime.date(year=2020, month=3, day=)),
    ("Tennessee", datetime.date(year=2020, month=3, day=31)),
    ("Texas", datetime.date(year=2020, month=3, day=24)),
    ("Utah", datetime.date(year=2020, month=3, day=30)),
    ("Vermont", datetime.date(year=2020, month=3, day=25)),
    ("Virginia", datetime.date(year=2020, month=3, day=30)),
    ("Washington", datetime.date(year=2020, month=3, day=23)),
    ("West Virginia", datetime.date(year=2020, month=3, day=24)),
    ("Wisconsin", datetime.date(year=2020, month=3, day=25)),
    ("Wyoming", datetime.date(year=2020, month=3, day=28)),
]

df = compute_us()

# ensure we have enough data
for state, _ in list(states):
    if df[state].max() < 10:
        df = df.drop(columns=[state])

predictions = defaultdict(lambda: dict())
state2chart = dict()

# go through dates to generate predictions through time
for data_date in df.index[-4:]:
    # go through each state and lockdown date
    for state, lockdown_date in list(states):
        if state not in df.columns:
            continue

        df_diff = pd.DataFrame(df[state])
        df_diff = df_diff[df_diff.index <= data_date]

        if df_diff.iloc[-1][state] == 0.0:
            continue

        # convert from raw counts to difference with a 3-day moving average
        df_diff[state] = df[state].diff().rolling(window=3).mean()

        df_diff = df_diff.fillna(value=0)
        # print(df_diff)

        # fit the sin curve
        clear_date = fit_sin(df_diff, state, lockdown_date)
        deaths = df_diff['computed'].sum()

        print("{} clear by: {} with {} deaths".format(state, clear_date, deaths))

        # record the prediction
        predictions[state][data_date] = '{} - {:,}'.format(clear_date.strftime('%B %-d'), floor(deaths))

        # plot the results if it's the last date
        if data_date == df.index[-1]:
            ax = df_diff.plot(figsize=(10,5))
            (start, end) = ax.get_xlim()
            ax.xaxis.set_ticks(np.arange(start, end, 6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%-m/%-d'))
            plt.ylabel('Deaths by Day')
            plt.grid(which='both', axis='x')

            # plt.show()
            img_name = state.lower().replace(' ', '_')
            fig = plt.savefig('site/img/us/{}.png'.format(img_name))
            state2chart[state] = 'img/us/{}.png'.format(img_name)
            plt.close()


# convert from dictionary to sorted tuple list
predictions = [(s, predictions[s]) for s in sorted(predictions.keys())]
print(predictions)

with open('site/us.template', 'r') as f:
    t = Template(f.read())
    out = t.render(dates=sorted(df.index[-4:], reverse=True), predictions=predictions, state_img=state2chart)

    with open('site/us.html', 'w') as f_out:
        f_out.write(out)
