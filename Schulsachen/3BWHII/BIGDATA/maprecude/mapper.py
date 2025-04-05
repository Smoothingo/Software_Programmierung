import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True, choices=['gcag', 'gistemp'], help='Data source (gcag or gistemp)')
args = parser.parse_args()

# Skip the header line
sys.stdin.readline()

for line in sys.stdin:
    try:
        source, year_month, mean = line.strip().split(',')
        if source.lower() == args.source.lower():
            # Extract year from "YYYY-MM" format
            year = year_month.split('-')[0]
            print(f"{year}\t{mean}")
    except:
        continue