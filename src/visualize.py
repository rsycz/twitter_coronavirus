#!/usr/bin/env python3
# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()
# imports
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter,defaultdict
# open the input path
with open(args.input_path) as f:
    counts = json.load(f)
# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]
# get top 10 items sorted low to high
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
items = items[:10]
items = sorted(items, key=lambda item: item[1])

# print the count values
for k,v in items:
    print(k,v)

# generate bar chart
keys = [item[0] for item in items]
values = [item[1] for item in items]

plt.figure(figsize=(12,6))
plt.bar(keys, values)
plt.xlabel('Key')
plt.ylabel('Count')
plt.title(f'{args.key} by {args.input_path}')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# save the figure
input_name = os.path.basename(args.input_path)
output_path = f'{args.key}_{input_name}.png'.replace('#','')
plt.savefig(output_path)
print(f'Saved plot to {output_path}')
