import datetime

from math import pi, sin, exp


def fit_sin(df, country, lockdown_date):
    prev_first_death_date = None
    prev_diff = None
    first_death_date = df[country].ne(0).idxmax() - datetime.timedelta(days=1)

    if country == 'Delaware':
        print()

    # have to keep these out of the loop because we change the length of the index
    i = -1
    latest_date = df.index[-1]
    latest_deaths = df[country][-1]

    while latest_deaths == 0.0:
        i -= 1
        latest_date = df.index[i]
        latest_deaths = df[country][i]

    # use lockdown_date + 24 days, or the actual peak whichever is further in the future
    computed_peak_date = lockdown_date + datetime.timedelta(days=24)  # we assume a peak 24 days after the lock-down
    max_deaths_date = df[country].idxmax()

    peak_date = computed_peak_date if computed_peak_date > max_deaths_date else max_deaths_date

    while True:
        last_death_date = peak_date + datetime.timedelta(days=(peak_date-first_death_date).days)
        duration = (last_death_date-first_death_date).days

        if latest_date < peak_date:
            peak_deaths = latest_deaths / sin((latest_date-first_death_date).days * (pi/duration))
        else:
            peak_deaths = df.loc[peak_date][country]

        df['computed'] = float(0.0)  # fill with zeros

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
            last_death_date = peak_date + datetime.timedelta(days=(peak_date - prev_first_death_date).days)
            duration = (last_death_date - prev_first_death_date).days

            df['computed'] = float(0.0)  # fill with zeros

            for day in range((last_death_date - prev_first_death_date).days):
                df.at[prev_first_death_date + datetime.timedelta(days=day), 'computed'] = peak_deaths * sin(day * (pi / duration))

            print("FIRST DEATH: {}\tLAST DEATH: {}".format(prev_first_death_date, last_death_date))

            return last_death_date


def fit_sigmoid(df, country):
    first_death_date = df[country].ne(0).idxmax()
    last_death_date = df.index[-1]
    peak_deaths_date = df[country].idxmax()
    peak_deaths_value = df.at[peak_deaths_date, country]

    df['computed'] = float(0.0)  # fill with zeros
    L = float(peak_deaths_value) + 50.0
    k = -0.25
    # x_0 = float((peak_deaths_date - first_death_date).days) / 2.0
    x_0 = (datetime.date(year=2020, month=3, day=18) - first_death_date).days
    print("x_0: {} - {} - {}".format(first_death_date, first_death_date + datetime.timedelta(days=x_0), peak_deaths_date))

    max_day = (peak_deaths_date - first_death_date).days
    for day in range(max_day):
        df.at[first_death_date + datetime.timedelta(days=day), 'computed'] = L / (1.0 + exp(k * (day - x_0)))

        predict_day = day + max_day
        x_0_predict = x_0 + max_day
        df.at[first_death_date + datetime.timedelta(days=predict_day), 'computed'] = L / (1.0 + exp(k * (-1.0 * (predict_day - x_0_predict))))

        print("{}:{} vs {}:{}".format(day, k * (day - x_0), predict_day, k * (-1.0 * (predict_day - x_0_predict))))

    return last_death_date

