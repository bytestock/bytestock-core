import numpy as np


def daily_ratio_calculation(close_data):
    daily_ratio_values = []
    adj_close_count = 0
    prev_adj_close= close_data[0]
    for i in range(len(close_data)):
        current_adj_close = float(close_data[i])
        adj_close_count +=1
        if adj_close_count >1:
            try: 
                daily_ratio = (current_adj_close/prev_adj_close)
                daily_ratio_values.append(daily_ratio)
            except:
                print("Error with daily ratio {i}")
            prev_adj_close = current_adj_close
    return daily_ratio_values

def weekly_ratio_calculation(close_data):
    weekly_ratio_values = []
    adj_close_count = 0
    for i in range(len(close_data)):
        adj_close_count+=1
        if adj_close_count >5:
            try:
                denominator_daily = close_data[i-5]
                numerator_daily = close_data[i]
                weekly_ratio = numerator_daily/denominator_daily
                weekly_ratio_values.append(weekly_ratio)
            except:
                print(f"Error with weekly ratio {i}")
    return weekly_ratio_values

def daily_ratio_average_calculations(daily_ratio):
    daily_ratio_average_values = []
    daily_ratio_count = 0
    for i in range(len(daily_ratio)):
        daily_ratio_count +=1
        daily_ratio_average_sum = 0
        if daily_ratio_count > 4:
            try:
                daily_ratio_average_sum +=daily_ratio[i:i-4]
                daily_ratio_average = daily_ratio_average_sum/5
                daily_ratio_average_values.append(daily_ratio_average)
            except:
                print(f"Error with daily ratio average {i}")
    return daily_ratio_average_values

def daily_ratio_standard_deviation_calculation(daily_ratio):
    daily_ratio_standard_deviation_values = []
    daily_ratio_count = 0
    for i in range(len(daily_ratio)):
        daily_ratio_count +=1
        if daily_ratio_count > 4:
            try:
                #daily_ratio_standard_deviation = daily_ratio[i-4]
                daily_ratio_standard_deviation = np.std(daily_ratio[i:1-4])
                daily_ratio_standard_deviation_values.append(daily_ratio_standard_deviation)
            except:
                print("Error with daily ratio standard deviation{i}")
    return daily_ratio_standard_deviation_values

def mathematics(close_data):
    daily_ratio = daily_ratio_calculation(close_data) #correct
    weekly_ratio = weekly_ratio_calculation(close_data) #correct
    daily_ratio_average = daily_ratio_average_calculations(daily_ratio) #CHECK, SUM WRONG
    daily_ratio_standard_deviation = daily_ratio_standard_deviation_calculation(daily_ratio) #CHECK, SUM WRONG
    print(f"daily ratio: {daily_ratio}")
    print(f"daily ratio average: {daily_ratio_average}")