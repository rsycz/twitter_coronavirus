#!/usr/bin/env python3
# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

# scan through all .lang files and extract tweet counts per day per hashtag
data = defaultdict(dict)  # data[hashtag][date] = count

for path in sorted(glob.glob('src/outputs/geoTwitter20-*.lang')):
    # extract date from filename e.g. geoTwitter20-01-01
    basename = os.path.basename(path)
    date = basename[10:18]  # gets MM-DD-YY portion... adjust as needed
    # parse as month-day
    parts = basename.replace('geoTwitter20-','').replace('.zip.lang','')
    # parts is now MM-DD
    with open(path) as f:
        counts = json.load(f)
    for hashtag in args.hashtags:
        if hashtag in counts:
            total = sum(counts[hashtag].values())
        else:
            total = 0
        data[hashtag][parts] = data[hashtag].get(parts, 0) + total

# plot
plt.figure(figsize=(14,6))
for hashtag in args.hashtags:
    days = sorted(data[hashtag].keys())
    values = [data[hashtag][d] for d in days]
    plt.plot(days, values, label=hashtag)

plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.title('Hashtag usage over 2020')
plt.legend()
plt.xticks(rotation=45, ha='right')
# only show every 30th tick so x-axis isn't crowded
ax = plt.gca()
ticks = ax.get_xticks()
ax.set_xticks(ticks[::30])
plt.tight_layout()
plt.savefig('alternative_reduce.png')
print('Saved plot to alternative_reduce.png')
