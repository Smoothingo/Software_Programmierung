import sys
import json

output = {}

for line in sys.stdin:
    word, count = line.strip().split('\t')
    output[word] = int(count)

with open('output.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)