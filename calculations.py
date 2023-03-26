#Libraries

import statistics
import random
from statistics import NormalDist

#Functions
def daily_ratio_calculation(index: int, close_data: list)->float:
    """Calculates daily ratio"""
    if index >0 and index <len(close_data)-1:
        #try:
        daily_ratio = close_data[index+1]/close_data[index]
        return daily_ratio
        #except:
            #pass if condition is not met

def weekly_ratio_calculation(index,day: int, close_data: list) ->float:
    """Calculates weekly ratio"""
    weekly_ratio = close_data[index]/close_data[index-day]
    return weekly_ratio

def weekly_ratio_average_calculations(weekly_ratio_values:list) ->float: #10 day average
    """Calculates weekly ratio average"""
  
    weekly_ratio_average = statistics.mean(weekly_ratio_values[len(weekly_ratio_values)-11:len(weekly_ratio_values)-1])
    return weekly_ratio_average
   
def weekly_ratio_standard_deviation_calculation(weekly_ratio_values:list) ->float:
    """Calculates weekly ratio standard deviation"""
    weekly_ratio_average = statistics.stdev(weekly_ratio_values[len(weekly_ratio_values)-11:len(weekly_ratio_values)-1])
    return weekly_ratio_average


#def simulation_and_probability_calculations(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation: float) ->int:
    #"""Simulations and miscellaneous calculations"""
    #simulation_values = []
    #for _ in range(193):
        #simulation(NormalDist())

    #return 1,2

def mathematics(close_data:list) ->None:
    #for day in range(5,6): #Different days considered for comparison
    #total_true_count = 0
    #total_false_count = 0
    daily_ratio_values = []
    weekly_ratio_values = []
    day = 5
    for index, _ in enumerate(close_data):
        daily_ratio_values.append(daily_ratio_calculation(index, close_data))
        if index >= day:
            weekly_ratio = weekly_ratio_calculation(index, day, close_data)
            weekly_ratio_values.append(weekly_ratio)
            print(weekly_ratio_values)
        if len(weekly_ratio_values) >=11:
            weekly_ratio_average = weekly_ratio_average_calculations(weekly_ratio_values)
            weekly_ratio_standard_deviation = weekly_ratio_standard_deviation_calculation(weekly_ratio_values)
            
            #Step 5-12
            #total_true_count, total_false_count = simulation_and_probability_calculations(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation)
            #print(f"Total true and false count respectively for {day} days considered: {total_true_count}, {total_false_count}")
        