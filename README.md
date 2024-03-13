# rusher-rating
Created a new NFL statistic based on passer rating for rushers

rusher rating
modeled after passer rating
note: fumbles do not happen often enough for them to be their own category like interceptions are
2.375 * 4 =~ 3.167 * 3 -> puts it on same scale as QBR 0-158.3

range:
max(a/b/c) = 3.167
min(a/b/c) = 0

a: (td - fumble + 1.5) * .905 - considers a -2 td/fumble differential min and 2 differential to be the max
b: (yards / att - 3) * 1.056 - considers a 3 and under y/a min and a 6 max
c: (RYOE / att + 1) * .905 - considers about a -1 RYOE per attempt to be zero and a 2.5 to be max

formula ((a+b+c)/6) x 100 = passer rating formula

Rusher rating -> contracts