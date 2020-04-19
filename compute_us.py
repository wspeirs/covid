import pandas as pd

from dateutil.parser import parse
from collections import defaultdict
from datetime import timedelta
from statistics import mean


#
# Compute deaths from 2 sources of US data, using the max
#
def compute_us():
    jh_df = pd.read_csv('data/us_deaths_jh.csv', header=0)
    nyt_df = pd.read_csv('data/us_data_nyt.csv', header=0)
    nyt_df['date'] = pd.to_datetime(nyt_df['date'])

    data = defaultdict(lambda: dict())

    # go through the NYTs data converting to a DataFrame we can use
    for state, df in nyt_df.groupby('state'):
        date_group = df.groupby('date')
        for date, df in date_group:
            date_str = date.strftime('%-m/%-d/20')
            nyt_deaths = df['deaths'].sum()

            # just use NYTs data
            data[date.date()][state] = nyt_deaths

            # if date_str in jh_df.columns:
            #     jh_deaths = jh_df[jh_df['Province_State'] == state][date_str].sum()
            #     data[date.date()][state] = mean([nyt_deaths, jh_deaths])
            #     if state == 'Connecticut':
            #         print("{} vs {}".format(nyt_deaths, jh_deaths))
            # else:
            #     data[date.date()][state] = nyt_deaths

        # date = sorted(date_group.groups.keys())[-1]
        # date += timedelta(days=1)
        # date_str = date.strftime('%-m/%-d/20')
        #
        # if date_str in jh_df.columns:
        #     jh_deaths = jh_df[jh_df['Province_State'] == state][date_str].sum()
        #     data[date.date()][state] = jh_deaths

    df = pd.DataFrame(data).T
    df = df.sort_index()
    df = df.fillna(value=0)

    return df


if __name__ == '__main__':
    print(compute_us())
