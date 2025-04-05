import sys

current_year = None
sum_temp = 0
count = 0

for line in sys.stdin:
    year, mean = line.strip().split('\t')
    mean = float(mean)
    
    if year != current_year:
        if current_year is not None:
            # Print average for previous year
            avg = sum_temp / count
            print(f"{current_year}\t{avg:.2f}")
        current_year = year
        sum_temp = 0
        count = 0
    
    sum_temp += mean
    count += 1

# Print the last year
if current_year is not None:
    avg = sum_temp / count
    print(f"{current_year}\t{avg:.2f}")