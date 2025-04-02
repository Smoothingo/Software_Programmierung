import sys
import json

results = {}

for line in sys.stdin:
    year, avg = line.strip().split('\t')
    results[year] = float(avg)

print(json.dumps(results, indent=2))