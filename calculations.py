#Libraries

import statistics
import random
from statistics import NormalDist

#Functions
def daily_ratio_calculation(close_data: list)->list:
    """Calculates daily ratio"""
    daily_ratio_values = []
    prev_adj_close = close_data[0]
    for index, current_close_data in enumerate(close_data):
        if index >=1:
            try:
                daily_ratio = current_close_data/prev_adj_close
                daily_ratio_values.append(daily_ratio)
            except ValueError:
                pass
            prev_adj_close = current_close_data
    return daily_ratio_values

def weekly_ratio_calculation(close_data: list, day: int) ->list:
    """Calculates weekly ratio"""
    weekly_ratio_values = []
    for index,element in enumerate(close_data):
        if index >=day:
            try:
                denominator_daily = close_data[index-day]
                numerator_daily = element
                weekly_ratio = numerator_daily/denominator_daily
                weekly_ratio_values.append(weekly_ratio)
            except ValueError:
                pass
    return weekly_ratio_values

def daily_ratio_average_calculations(daily_ratio: list, day:int) ->list:
    """Calculates daily ratio average"""
    daily_ratio_average_values = []
    for index,_ in enumerate(daily_ratio):
        if index >=day:
            try:
                daily_ratio_average_sum = statistics.mean(daily_ratio[(index-5):index])
                daily_ratio_average_values.append(daily_ratio_average_sum)
            except IndexError:
                pass
    return daily_ratio_average_values

def daily_ratio_standard_deviation_calculation(daily_ratio:list ,day:int) ->list:
    """Calculates daily ratio standard deviation"""
    daily_ratio_standard_deviation_values = []
    for i in range(len(daily_ratio)):
        if i >(day-1):
            try:
                daily_ratio_standard_deviation = statistics.stdev(daily_ratio[(i-day):i])
                daily_ratio_standard_deviation_values.append(daily_ratio_standard_deviation)
            except ValueError:
                pass
    return daily_ratio_standard_deviation_values

def weekly_ratio_average_calculations(weekly_ratio:list) ->list: #10 day average
    """Calculates weekly ratio average"""
    weekly_ratio_average_values = []
    for i in range(len(weekly_ratio)):
        if i >9:
            weekly_ratio_average = statistics.mean(weekly_ratio[(i-10):i])
            weekly_ratio_average_values.append(weekly_ratio_average)
    return weekly_ratio_average_values

def weekly_ratio_standard_deviation_calculation(weekly_ratio:list) ->list:
    """Calculates weekly ratio standard deviation"""
    weekly_ratio_standard_deviation_values = []
    for i in range(len(weekly_ratio)):
        if i >9:
            try:
                weekly_ratio_standard_deviation = statistics.stdev(weekly_ratio[(i-10):i])
                weekly_ratio_standard_deviation_values.append(weekly_ratio_standard_deviation)
            except ValueError:
                pass
    return weekly_ratio_standard_deviation_values

def simulation_and_probability_calculations(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation: list) ->list:
    """Simulations and miscellaneous calculations"""
    simulation_average_values = []
    score_of_actual_values =[]
    normal_distribution_values = []
    total_true_count = 0 #total counter for trues in step 12
    total_false_count = 0 #total counter for false in step 12
    for index, current_simulation in enumerate(close_data):
        simulation_values = []
        try:
            current_weekly_average = weekly_ratio_average[index]
            current_weekly_standard_deviation = weekly_ratio_standard_deviation[index]
            for _ in range(193): #runs simulation 193 times
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
            score_of_actual = (close_data[index+10]-simulation_average)/std_dev
            score_of_actual_values.append(score_of_actual)

            #Percentage
            close_data_in_10_days = close_data[index+10]
            if score_of_actual > 0 :
                percentage = (1 - NormalDist(simulation_average, std_dev).cdf(close_data_in_10_days)) *100                                              
                normal_distribution_values.append(percentage)
            else:
                percentage =  NormalDist(simulation_average, std_dev).cdf(close_data_in_10_days) *100                                           
                normal_distribution_values.append(percentage)

            
            #STEPS 12
            try:
            
                #It has to check if each statement is false (Reason for 8 different if/else statements)

                if close_data[index+10] > std_dev_plus_3: #>+3STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= std_dev_plus_3 and close_data[index+10] > std_dev_plus_2: #>+2STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= std_dev_plus_2 and close_data[index+10] > std_dev_plus_1: #>+1STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= std_dev_plus_1 and close_data[index+10] > simulation_average: #<+1STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= simulation_average and close_data[index+10] > std_dev_minus_1: #>-1 STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= std_dev_minus_1 and close_data[index+10] > std_dev_minus_2: #<-1 STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] <= std_dev_minus_2 and close_data[index+10] > std_dev_minus_3:#<-2 STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
                if close_data[index+10] < std_dev_minus_3: #<-3 STD
                    total_true_count+=1
                else:
                    total_false_count+=1 #as previous statement was false
            except ValueError:
                pass #The close_data[n+10] has gone past available close data
        except IndexError:
            pass

    return total_true_count, total_false_count

def probability_calculation(total_true_count,total_false_count:int) ->str: #Final step of Part 1:
    """Calculates probabilities"""
    try:
        return f"{(total_true_count/(total_true_count+total_false_count) ) *100} %"
    except ZeroDivisionError:
        pass
#main function of calculations.py
def mathematics(close_data:list) ->None:
    """Calculations for bitestock website"""
    for i in range(5,31): #days considered for comparisons
        day = i #current day being compared to
        daily_ratio = daily_ratio_calculation(close_data)
        weekly_ratio = weekly_ratio_calculation(close_data,day)
        daily_ratio_average = daily_ratio_average_calculations(daily_ratio,day) 
        daily_ratio_standard_deviation = daily_ratio_standard_deviation_calculation(daily_ratio,day)
        weekly_ratio_average = weekly_ratio_average_calculations(weekly_ratio)
        weekly_ratio_standard_deviation = weekly_ratio_standard_deviation_calculation(weekly_ratio)
        total_true_count, total_false_count = simulation_and_probability_calculations(close_data, weekly_ratio_average,  weekly_ratio_standard_deviation)
        probability =  probability_calculation(total_true_count,total_false_count)
        print(f"{probability} {i} days from now")
        #print(daily_ratio_average)