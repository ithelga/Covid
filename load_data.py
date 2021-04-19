import pandas as pd

REGIONS = ['Russia', 'Belarus', 'Uzbekistan', 'Japan', 'Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany',
           'Iran', 'Italy', 'Netherlands', 'Spain', 'Switzerland', 'Turkey', 'US', 'United Kingdom']

dates = pd.date_range("01/22/2020", "04/18/2020")
filename = 'data\data-%s-%s.txt' % (dates.min().strftime('%m_%d'), dates.max().strftime('%m_%d'))
print(filename)

# https://honingds.com/blog/pandas-read_csv/

datalist = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{dt}.csv'
dataframes = []

countryColumn = 'Country/Region'
for dt in dates:
    print(dt.strftime('%m-%d-%Y'))
    if dt > pd.to_datetime("03/21/2020"):
        countryColumn = 'Country_Region'
    dataset = datalist.format(dt=dt.strftime('%m-%d-%Y'))
    df = pd.read_csv(dataset, sep=",", usecols=[countryColumn, 'Confirmed', 'Deaths', 'Recovered'])
    df.columns = ['Country', 'Confirmed', 'Deaths', 'Recovered']
    df = df[df['Country'].isin(REGIONS)]
    df = df.groupby(by=['Country'], as_index=True).sum()
    df = df.assign(Date=dt.strftime('%Y-%m-%d'))
    dataframes.append(df)

result = pd.concat(dataframes)
result.to_csv(filename)
