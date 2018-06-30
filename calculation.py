import csv
import sys
from datetime import datetime, timedelta
from period import calculate_no_of_period, calculate_no_of_total_volume_and_total_product

# Constant variable
READ_PATH = './filtered_dataset/sample_filtered_data.csv'
WRITE_PATH = './calculated_dataset/sample_calculated_data.csv'

# Initialize data
PERIOD = 15
time_data = []
FMT = '%H:%M:%S'
NUM_OF_RESULT = 3
STARTING_PERIOD_MORNING = datetime.strptime("09:45:00", FMT) 
ENDIND_PERIOD_MORNING = datetime.strptime("12:30:00", FMT)
STARTING_PERIOD_AFTERNOON = datetime.strptime("14:30:00", FMT)
ENDING_PERIOD_AFTERNOON = datetime.strptime("16:45:00", FMT)
MORNING_COUNTED_PERIOD = calculate_no_of_period(STARTING_PERIOD_MORNING, ENDIND_PERIOD_MORNING, PERIOD)
AFTERNOON_COUNTED_PERIOD = calculate_no_of_period(STARTING_PERIOD_AFTERNOON, ENDING_PERIOD_AFTERNOON, PERIOD)
NO_OF_MORNING_PERIOD = [[0] * NUM_OF_RESULT for _ in range(MORNING_COUNTED_PERIOD)]
NO_OF_AFTERNOON_PERIOD = [[0] * NUM_OF_RESULT for _ in range(AFTERNOON_COUNTED_PERIOD)]

with open(READ_PATH, newline='\n') as read_csvfile:
    reader = csv.reader(read_csvfile, delimiter=',')
    # Skip header line
    next(reader, None)
    for row in reader:
        if len(row[5]) == 7:
            tmp = "0" + row[5][:-2]
            tmp = ":".join(tmp[i:i+2] for i in range(0, len(tmp), 2))
            row[5] = datetime.strptime(tmp, FMT)
        elif len(row[5]) == 8:
            tmp = row[5][:-2]
            tmp = ":".join(tmp[i:i+2] for i in range(0, len(tmp), 2))
            row[5] = datetime.strptime(tmp, FMT)
        else:
            print("VAR6 is longer than 8", len(row[5]))
            sys.exit(0)
        time_data.append(row)


if time_data:
    for data in time_data:
        current_time = data[5]
        if ENDIND_PERIOD_MORNING > current_time:
            # do sth in morningp period
            calculate_no_of_total_volume_and_total_product(STARTING_PERIOD_MORNING, ENDIND_PERIOD_MORNING, PERIOD, data, NO_OF_MORNING_PERIOD)
            # print("NO_OF_MORNING_PERIOD", NO_OF_MORNING_PERIOD)
        elif ENDING_PERIOD_AFTERNOON > current_time and current_time > ENDIND_PERIOD_MORNING:
            # do sth in afternoon period
            calculate_no_of_total_volume_and_total_product(STARTING_PERIOD_AFTERNOON, ENDING_PERIOD_AFTERNOON, PERIOD, data, NO_OF_AFTERNOON_PERIOD)
        else:
            print("current_time is not in both period.")
            sys.exit(0)

    for i, p in enumerate(NO_OF_MORNING_PERIOD):
        if p[0] == 0 or p[1] == 0:
            if i == 0:
                continue
            p[2] = NO_OF_MORNING_PERIOD[i-1][2]
            continue
        p[2] = p[0] / p[1]

    for i, p in enumerate(NO_OF_AFTERNOON_PERIOD):
        if p[0] == 0 or p[1] == 0:
            if i == 0:
                continue
            p[2] = NO_OF_AFTERNOON_PERIOD[i-1][2]
            continue
        p[2] = p[0] / p[1]
    
    with open(WRITE_PATH, 'w', newline='\n') as write_csvfile:
        writer = csv.writer(write_csvfile, delimiter=',')
        # Write default header for filtered_data file
        writer.writerow(['sum_of_product', 'sum_of_volumn', 'volumn_avg_price'])
        # Write filter_data to file
        for p in NO_OF_MORNING_PERIOD:
            writer.writerow(p)
        
        for p in NO_OF_AFTERNOON_PERIOD:
            writer.writerow(p)
