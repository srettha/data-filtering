from datetime import datetime, timedelta

def calculate_no_of_period(starting_time, ending_time, period):
    counted_period = 0
    tmp_starting_time = starting_time
    while ending_time > tmp_starting_time:
        tmp_starting_time = tmp_starting_time + timedelta(minutes=period)
        counted_period += 1
        # print(tmp_starting_time, counted_period)
    return counted_period

def calculate_no_of_total_volume_and_total_product(starting_time, ending_time, period, data, arr_of_period):
    current_period = 0
    current_time = data[5]
    volumn = float(data[11])
    price = float(data[12])
    tmp_starting_time = starting_time
    while ending_time > tmp_starting_time:
        tmp_starting_time_plus_period = tmp_starting_time + timedelta(minutes=period)
        if tmp_starting_time_plus_period >= current_time and current_time >= tmp_starting_time:
            arr_of_period[current_period][0] += volumn * price
            arr_of_period[current_period][1] += volumn
            break
        else:
            tmp_starting_time = tmp_starting_time + timedelta(minutes=period)
            current_period += 1