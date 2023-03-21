import statistics
import scipy.stats as scp
from scipy.stats import norm
import random 
from statistics import NormalDist
import numpy as np

def daily_ratio_calculation(close_data: list) ->list:
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

def weekly_ratio_calculation(close_data: list, day: int) ->list:
    weekly_ratio_values = []
    adj_close_count = 0
    for i in range(len(close_data)):
        adj_close_count+=1
        if adj_close_count >day:
            try:
                denominator_daily = close_data[i-day]
                numerator_daily = close_data[i]
                weekly_ratio = numerator_daily/denominator_daily
                weekly_ratio_values.append(weekly_ratio)
            except:
                pass #weekdays/days that the market is closed
    return weekly_ratio_values

def daily_ratio_average_calculations(daily_ratio: list, day:int) ->list:
    daily_ratio_average_values = []
    daily_ratio_count = 0
    for i in range(len(daily_ratio)):
        daily_ratio_count +=1
        daily_ratio_average_sum = 0
        if daily_ratio_count > (day-1):
            try:
                for n in range((i-(day-1)),i+(day-1)):
                    daily_ratio_average_sum +=daily_ratio[n]
                daily_ratio_average = daily_ratio_average_sum/day
                daily_ratio_average_values.append(daily_ratio_average)
            except:
                pass
    return daily_ratio_average_values

def daily_ratio_standard_deviation_calculation(daily_ratio:list ,day:int) ->list:
    daily_ratio_standard_deviation_values = []
    for i in range(len(daily_ratio)):
        if i >(day-1):
            try:
                daily_ratio_standard_deviation = statistics.stdev(daily_ratio[(i-day):i])
                daily_ratio_standard_deviation_values.append(daily_ratio_standard_deviation)
            except:
                pass
    return daily_ratio_standard_deviation_values

def weekly_ratio_average_calculations(weekly_ratio:list) ->list: #10 day average
    weekly_ratio_average_values = []
    for i in range(len(weekly_ratio)):
        if i >9:
            try:
                weekly_ratio_average = statistics.mean(weekly_ratio[(i-10):i])
                weekly_ratio_average_values.append(weekly_ratio_average)
            except:
                print(f"Error with {weekly_ratio[i]}")
                pass 
    return weekly_ratio_average_values

def weekly_ratio_standard_deviation_calculation(weekly_ratio:list) ->list:
    weekly_ratio_standard_deviation_values = []
    for i in range(len(weekly_ratio)):
        if i >9:
            try:
                weekly_ratio_standard_deviation = statistics.stdev(weekly_ratio[(i-10):i])
                weekly_ratio_standard_deviation_values.append(weekly_ratio_standard_deviation)
            except:
                pass
    return weekly_ratio_standard_deviation_values

def simulation_based_on_5day_average_and_Std_Dev_average_calculation(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation: list) ->list:
    simulation_average_values = []
    score_of_actual_values =[]
    probability_values = []
    normal_distribution_values = []
    #all_simulation_std_dev_values = []
    for n in range(len(close_data)):
        simulation_values = []
        try:
            current_simulation = close_data[n]
            current_weekly_average = weekly_ratio_average[n] 
            current_weekly_standard_deviation = weekly_ratio_standard_deviation[n]
            for i in range(193): #runs simulation 193 times
                simulation = (NormalDist( current_weekly_average, current_weekly_standard_deviation).inv_cdf(random.uniform(0,1))) *current_simulation
                simulation_values.append(simulation)
            simulation_average = sum(simulation_values)/len(simulation_values)
            simulation_average_values.append(simulation_average)

            #Std Dev:
            std_dev = statistics.stdev(simulation_values)
            std_dev_plus_3 = simulation_average + (std_dev*3)
            std_dev_plus_2 = simulation_average + (std_dev*2)
            std_dev_plus_1 = simulation_average + std_dev
            std_dev_minus_1 = simulation_average - std_dev
            std_dev_minus_2 = simulation_average - (std_dev*2)
            std_dev_minus_3 = simulation_average - (std_dev*3)

            #Score of Actual:
            score_of_actual = (close_data[n+10]-simulation_average)/std_dev
            score_of_actual_values.append(score_of_actual)
        
            #Probabilities
            x = close_data[n+10]
            if score_of_actual > 0 :
                    #normal_distribution = (1-NormalDist(mu=, sigma = ).inv_cdf())*100   
                percentage = (1 - NormalDist(simulation_average, std_dev).cdf(x)) *100                                                 
                normal_distribution_values.append(percentage)
            else:
                percentage =  NormalDist(simulation_average, std_dev).cdf(x) *100                                                
                normal_distribution_values.append(percentage)
        except:
            pass

        #STEPS 12
        deviation_count=0

        if close_data[n+10] > std_dev_plus_3:
            deviation_count+=1
        elif close_data[n+10] <= std_dev_plus_3 and close_data[n+10] > std_dev_plus_2:
            deviation_count+=1
        elif close_data[n+10] <= std_dev_plus_2 and close_data[n+10] > std_dev_plus_1:
            deviation_count+=1
        elif close_data[n+10] <= std_dev_plus_1 and close_data[n+10] > simulation_average:
            deviation_count+=1
        elif close_data[n+10] <= simulation_average and close_data[n+10] > std_dev_minus_1:
            deviation_count+=1
        elif close_data[n+10] <= std_dev_minus_1 and close_data[n+10] > std_dev_minus_2:
            deviation_count+=1
        elif close_data[n+10] <= std_dev_minus_2 and close_data[n+10] > std_dev_minus_3:
            deviation_count+=1
        elif close_data[n+10] < std_dev_minus_3:
            deviation_count+=1
        "mismatch..........."

    return normal_distribution_values

def mathematics(close_data):
    for i in range(5,31):
        day = i
        daily_ratio = daily_ratio_calculation(close_data) 
        weekly_ratio = weekly_ratio_calculation(close_data,day) 
        daily_ratio_average = daily_ratio_average_calculations(daily_ratio,day) 
        daily_ratio_standard_deviation = daily_ratio_standard_deviation_calculation(daily_ratio,day) 
        weekly_ratio_average = weekly_ratio_average_calculations(weekly_ratio) 
        weekly_ratio_standard_deviation = weekly_ratio_standard_deviation_calculation(weekly_ratio) 
        normal_distribution = simulation_based_on_5day_average_and_Std_Dev_average_calculation(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation)   
