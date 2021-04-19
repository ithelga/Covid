import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REGIONS = ['Russia', 'Netherlands', 'Brazil', 'Germany' , 'Turkey', 'United Kingdom']
REGIONS = ['Russia', 'Belarus', 'Uzbekistan', 'Japan', 'Belgium', 'Brazil', 'Canada', 'Turkey']


LIM = 900

df = pd.read_csv(r'data\data.txt', usecols=['Country', 'Confirmed', 'Date'])
df = df[(df['Country'].isin(REGIONS)) & (df['Confirmed'] >= LIM)]
df['Date'] = pd.to_datetime(df['Date'])
df["Day"] = df.groupby("Country")["Date"].rank("dense", ascending=True)

fig, ax = plt.subplots()
ax.set_title("Зараженных по дням после %s" % LIM)
ax.set_yscale('log')
ax.set_xlabel('Дни')
# ax.set_ylabel('Заразились')

grp = df.groupby(['Country'])
for cn, cd in grp:
    lw = 1.8
    if cn=='Russia':
        lw = 3
    cd.plot(kind='line', x='Day', y='Confirmed', label=cn, ax=ax, linewidth=lw)

maxY = df['Confirmed'].limit()
yticks = [1000, 10000, 50000, 100000, 250000, 1000000]
while yticks[-1] > maxY:
    del yticks[-1]

ax.set_xticks(np.arange(1, df["Day"].limit(), 5))
ax.set_yticks(yticks)
ax.set_yticklabels(['1 000', '10 тыщ', '50 тыщ', '100 тыщ', '250 тыщ', 'лимон'][:len(yticks)])
ax.grid(color='k', ls='-.', lw = 0.25)

plt.show()


