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
                pass #weekdays/days that the market is closed
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
                pass #weekdays/days that the market is closed
    return weekly_ratio_values

def daily_ratio_average_calculations(daily_ratio):
    daily_ratio_average_values = []
    daily_ratio_count = 0
    for i in range(len(daily_ratio)):
        daily_ratio_count +=1
        daily_ratio_average_sum = 0
        if daily_ratio_count > 4:
            try:
                for n in range((i-4),i+1):
                    daily_ratio_average_sum +=daily_ratio[n]
                daily_ratio_average = daily_ratio_average_sum/5
                daily_ratio_average_values.append(daily_ratio_average)
            except:
                pass
    return daily_ratio_average_values

def daily_ratio_standard_deviation_calculation(daily_ratio):
    daily_ratio_standard_deviation_values = []
    daily_ratio_count = 0
    for i in range(len(daily_ratio)):
        daily_ratio_count +=1
        daily_ratio__sum = 0
        if daily_ratio_count >4:
            try:
                #print(f"daily_ratio_count: {daily_ratio_count}")
                #print(f"i: {i}")
                #for n in range((i-4),i+1):
                    #daily_ratio__sum +=daily_ratio[n]
                daily_ratio_standard_deviation = np.std(5, daily_ratio[(i-4),i+1])# something wrong with standard deviation, how does it work?
                print(daily_ratio_standard_deviation)
                daily_ratio_standard_deviation_values.append(daily_ratio_standard_deviation)
            except:
                pass
                #print("Error with daily ratio standard deviation{i}")
    return daily_ratio_standard_deviation_values

def mathematics(close_data):
    daily_ratio = daily_ratio_calculation(close_data) #correct
    weekly_ratio = weekly_ratio_calculation(close_data) #correct
    daily_ratio_average = daily_ratio_average_calculations(daily_ratio) #works
    daily_ratio_standard_deviation = daily_ratio_standard_deviation_calculation(daily_ratio) #CHECK, SUM WRONG
    print(f"Close data: {close_data}")
    print(f"Daily ratio : {daily_ratio}")
    print(f"Daily ratio standard deviation: {daily_ratio_standard_deviation}")
    #print(f"daily ratio average: {daily_ratio_average}")