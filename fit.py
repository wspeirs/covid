import datetime

from math import pi, sin


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
