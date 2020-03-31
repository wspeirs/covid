import pandas as pd
from dateutil.parser import parse

#
# Compute the cases and deaths from 2 sources of US data, using the max
#
def compute_us():
    deaths_df = pd.read_csv('data/us_deaths_jh.csv', header=0)
    cases_df = pd.read_csv('data/us_confirmed_jh.csv', header=0)

    combined_df = pd.read_csv('data/us_data_nyt.csv', header=0)
    combined_df['date'] = pd.to_datetime(combined_df['date'])

    data = dict()

    for date in deaths_df.columns[11:]:
        data[date] = dict()

        data[date]['jh_deaths'] = deaths_df[date].sum()
        data[date]['jh_cases'] = cases_df[date].sum()

        data[date]['nyt_deaths'] = combined_df[combined_df['date'] == parse(date)]['deaths'].sum()
        data[date]['nyt_cases'] = combined_df[combined_df['date'] == parse(date)]['cases'].sum()

    data_df = pd.DataFrame(data)
    data_df = data_df.T

    data_df['deaths'] = data_df[['jh_deaths', 'nyt_deaths']].max(axis=1)
    data_df['cases'] = data_df[['jh_cases', 'nyt_cases']].max(axis=1)
    data_df['mortality'] = data_df['deaths'] / data_df['cases']

    return data_df[['cases', 'deaths', 'mortality']]


if __name__ == '__main__':
    print(compute_us().head())
