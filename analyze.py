import pandas as pd
import matplotlib.pyplot as plt

data = dict()
countries = {
    "Belgium",
    # "Brazil",
    "China",
    "France",
    "Germany",
    # "Indonesia",
    "Iran",
    "Italy",
    "Korea, South",
    # "Netherlands",
    # "Portugal",
    "Spain",
    # "Sweden",
    # "Switzerland",
    # "Turkey",
    "United Kingdom",
    "US",
}

world_df = pd.read_csv('data/global_deaths.csv', header=0)

# group by countries
country_groups = world_df.groupby('Country/Region')

for country, df in country_groups:
    if country not in countries:
        continue
    data[country] = dict()

    for date in world_df.columns[4:]:
        total = df[date].sum()  # total up the deaths for that date
        # print("{} - {}: {}".format(date, country, total))
        data[country][date] = total

df = pd.DataFrame(data)
print(df.head())

# compute the difference of deaths between days
# apply a 3-day moving average to smooth out the lines
df_diff = df.diff().rolling(window=3).mean()

# plot the results
# df_diff.plot(figsize=(15,10), logy=True)
df_diff.plot(figsize=(15,10))
plt.show()
