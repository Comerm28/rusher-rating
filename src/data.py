#inspired by Tim Bryan's tutorial on nfl next gen stats

import nfl_data_py as nfl
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def a(td, fb, gp):
    if (td - fb) / gp >= 2:
        diff = 2
    elif (td - fb) / gp <= -2:
        diff = -2
    else:
        diff = (td - fb) / gp
    return (diff + 1.5) * .905

def b(ya):
    if ya > 6:
        ya = 6
    elif ya < 3:
        ya = 3
    return (ya - 3) * 1.056

def c(ryoe):
    if ryoe > 2.5:
        ryoe = 2.5
    elif ryoe < -1:
        ryoe = -1
    return (ryoe + 1) * .905

def rusher_rating(a, b, c):
    return (a+b+c)/6.0 * 100.0

years = [2023]

rusherbcstat = nfl.import_ngs_data(stat_type='rushing',years=years)
rusherastat = nfl.import_seasonal_data(years)
money = nfl.import_contracts()

rusherbcstat_aggregated = rusherbcstat.groupby(['player_gsis_id', 'player_display_name', 'season']).agg({
    'avg_rush_yards': 'mean', 
    'rush_yards_over_expected_per_att': 'mean',  
}).reset_index()

x = []
y = []
z = []
s = []

for rb in rusherbcstat_aggregated.index:
    id = rusherbcstat_aggregated['player_gsis_id'][rb]
    if id not in rusherastat['player_id'].values:
        continue
    indA = list(rusherastat['player_id']).index(id)

    name = rusherbcstat_aggregated['player_display_name'][rb]
    if name not in money['player'].values:
        continue
    indM = list(money['player']).index(name)
    if(rusherastat['carries'][indA] < 100):
        continue
    
    x.append(rusher_rating(a(rusherastat['rushing_tds'][indA], rusherastat['rushing_fumbles_lost'][indA], rusherastat['games'][indA]), b(rusherbcstat_aggregated['avg_rush_yards'][rb]), c(rusherbcstat_aggregated['rush_yards_over_expected_per_att'][rb])))
    y.append(money['apy'][indM])
    z.append(name)
    s.append(rusherbcstat_aggregated['season'][rb])

xy = pd.DataFrame({'x' : x, 'y' : y})

plot.figure(figsize=(8, 6))
plot.scatter(x, y, color='blue', alpha=0.5)
plot.title('Is Paying a Running Back Worth it?')
plot.xlabel('Average Rusher Rating')
plot.ylabel('Salary (Millions)')
plot.xlim(0, 158.3)
plot.ylim(0, 20) 
plot.grid(True)

for i in xy.index:
    plot.annotate(f"{z[i]}, {s[i]}", (xy['x'][i], xy['y'][i]), fontsize=6)

plot.show()