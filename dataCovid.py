import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REGIONS = ['Russia', 'Netherlands', 'US', 'Spain', 'Germany']
WIDTH = 0.95 / len(REGIONS)
COLORS = 'bgcmy'


df = pd.read_csv(r'data\data.txt')
df = df[df['Country'].isin(REGIONS)]
df['Date'] = pd.to_datetime(df['Date'])
df['Daily_Confirmed'] = df['Confirmed'] - df.sort_values(by=['Date'], ascending=True).groupby(['Country'])['Confirmed'].shift(1)
df["Daily_Confirmed"] = df["Daily_Confirmed"].fillna(df["Confirmed"])

days = pd.to_datetime(df['Date'].unique())
index = np.arange(len(days))
delta = 0

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 7))
ax1.set_yscale('log')
ax1.set_xlabel('Дни')
ax1.set_ylabel('Всего')
ax2.set_yscale('log')
ax2.set_xlabel('Дни')
ax2.set_ylabel('В день')

countries = df.groupby('Country')
for i, country in enumerate(countries.groups.keys()):
    p = countries.get_group(country).groupby('Date', as_index=False).sum()['Confirmed'].tolist()
    b = countries.get_group(country).groupby('Date', as_index=False).sum()['Daily_Confirmed'].tolist()
    while len(p) < len(index):
        p.insert(0,0)
        b.insert(0,0)
    color = COLORS[i]
    linewidth = 1
    if country == 'Russia':
        color = 'r'
        linewidth = 1.7
    # ax1.plot(index, p, color=color, label=country, linewidth = linewidth)
    ax2.bar(index + delta, b, WIDTH, label=country, color=color)
    delta += WIDTH


ticks = index[4::7]
tickNames = [x.strftime('%d/%m') for x in days[4::7]]
ax1.set_xticks(ticks)
ax1.set_xticklabels(tickNames)
ax2.set_xticks(ticks)
ax2.set_xticklabels(tickNames)
ax1.set_yticks([100, 1000, 10000, 50000, 100000, 250000, 1000000])
ax1.set_yticklabels(['100', '1 000', '10 тыщ', '50 тыщ', '100 тыщ', '250 тыщ', 'лимон'])
ax1.grid(color='k', ls = '-.', lw = 0.25)
ax2.legend()


fig.tight_layout()
plt.show()