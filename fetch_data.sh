#!/bin/sh
mkdir -p data

# data from Johns Hopkins
wget 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv' -O data/global_deaths.csv
wget 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv' -O data/global_confirmed.csv

wget 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv' -O data/us_deaths_jh.csv
wget 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv' -O data/us_confirmed_jh.csv

# NYTs data
wget 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv' -O data/us_data_nyt.csv

