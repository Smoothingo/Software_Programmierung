import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True, choices=['gcag', 'gistemp'], help='Data source (gcag or gistemp)')
args = parser.parse_args()

# Skip the header line
sys.stdin.readline()

def parse_line(line):
    parts = line.strip().split(',')
    year = parts[0]
    months = parts[1:13]  # Only Jan–Dec (12 months)
    return year, months

if args.source.lower() == 'gistemp':
    for line in sys.stdin:
        if line.strip() and not line.startswith('Year'):
            try:
                year, months = parse_line(line)
                valid_values = [float(value) for value in months if value != '***' and value != '']
                if valid_values:
                    avg_temp = sum(valid_values) / len(valid_values)
                    print(f"{year}\t{avg_temp:.2f}")
            except Exception:
                continue
elif args.source.lower() == 'gcag':
    for line in sys.stdin:
        try:
            source, year_month, mean = line.strip().split(',')
            if source.lower() == args.source.lower():
                year = year_month.split('-')[0]
                try:
                    mean = float(mean)
                    print(f"{year}\t{mean:.2f}")
                except ValueError:
                    continue
        except Exception:
            continue