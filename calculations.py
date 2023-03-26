#Libraries

import statistics
import random
from statistics import NormalDist
import multiprocessing

#Functions
def daily_ratio_calculation(index: int, close_data: list)->float:
    """Calculates daily ratio"""
    if index >0 and index <len(close_data)-1:
        #try:
        daily_ratio = close_data[index-1]/close_data[index]
        return daily_ratio
        #except:
            #pass if condition is not met

def weekly_ratio_calculation(index,day: int, close_data: list) ->float:
    """Calculates weekly ratio"""
    weekly_ratio = close_data[index]/close_data[index-day]
    return weekly_ratio

def weekly_ratio_average_calculations(weekly_ratio_values:list, comparison:int) ->float: #10 day average
    """Calculates weekly ratio average"""
  
    weekly_ratio_average = statistics.mean(weekly_ratio_values[len(weekly_ratio_values)-11:len(weekly_ratio_values)-1])
    return weekly_ratio_average
   
def weekly_ratio_standard_deviation_calculation(weekly_ratio_values:list) ->float:
    """Calculates weekly ratio standard deviation"""
    weekly_ratio_average = statistics.stdev(weekly_ratio_values[len(weekly_ratio_values)-11:len(weekly_ratio_values)-1])
    return weekly_ratio_average


def simulation_and_probability_calculations(index, close_data, weekly_ratio_average, weekly_ratio_standard_deviation) ->int:
    """Simulations and miscellaneous calculations"""
    simulation_values = []
    true_count = 0
    false_count = 0
    current_simulation_value = close_data[index]
    current_weekly_average = weekly_ratio_average
    current_weekly_standard_deviation = weekly_ratio_standard_deviation
    for _ in range(193):
        simulation = (NormalDist(current_weekly_average, current_weekly_standard_deviation).inv_cdf(random.uniform(0,1))) *current_simulation_value
        simulation_values.append(simulation)
    simulation_average = statistics.mean(simulation_values)
   
    #Std Dev:
    std_dev = statistics.stdev(simulation_values)

    #abs difference
    abs_difference = abs(close_data[index] - simulation_average)
    if abs_difference <1:
        std_dev_plus_3 = simulation_average + (std_dev*3)
        std_dev_plus_2 = simulation_average + (std_dev*2)
        std_dev_plus_1 = simulation_average + std_dev
        std_dev_minus_1 = simulation_average - std_dev
        std_dev_minus_2 = simulation_average - (std_dev*2)
        std_dev_minus_3 = simulation_average - (std_dev*3)
  
        try:
            #Score of Actual:
            score_of_actual = (close_data[index+10]-simulation_average)/std_dev

            #Percentage
            close_data_in_10_days = close_data[index+10]
            if score_of_actual > 0 :
                percentage = (1 - NormalDist(simulation_average, std_dev).cdf(close_data_in_10_days)) *100                        
            else:
                percentage =  NormalDist(simulation_average, std_dev).cdf(close_data_in_10_days) *100
        
            #STEPS 12
            #It has to check if each statement is false (Reason for 8 different if/else statements)

            #print(close_data[index+10], simulation_average, std_dev_plus_2, std_dev)

            if close_data[index+10] > std_dev_plus_3: #>+3STD
                true_count+=1
               # print('TRUE OPSITIVE')
            if close_data[index+10] <= std_dev_plus_3 and close_data[index+10] > std_dev_plus_2: #>+2STD
                true_count+=1
               # print('TRUE OPSITIVE')
            if close_data[index+10] <= std_dev_plus_2 and close_data[index+10] > std_dev_plus_1: #>+1STD
                false_count += 1
            if close_data[index+10] <= std_dev_plus_1 and close_data[index+10] > simulation_average: #<+1STD
                false_count+=1
            if close_data[index+10] <= simulation_average and close_data[index+10] > std_dev_minus_1: #>-1 STD
                false_count+=1
            if close_data[index+10] <= std_dev_minus_1 and close_data[index+10] > std_dev_minus_2: #<-1 STD
                false_count+=1
            if close_data[index+10] <= std_dev_minus_2 and close_data[index+10] > std_dev_minus_3:#<-2 STD
                true_count += 1
               # print('TRUE OPSITIVE')
            if close_data[index+10] < std_dev_minus_3: #<-3 STD
                true_count+=1
                #print('TRUE OPSITIVE')

            #print(f"Total true and false count for index {close_data[index]} days considered: {true_count}, {false_count}")
            #print(true_count/(true_count+false_count))
        except IndexError: #if data 10 days from date is not available
            pass

    return true_count, false_count



def mathematics(close_data:list) ->None:
    day_prices = []
    for current_comparison, _ in enumerate (close_data):
        total_true_count = []
        total_false_count = []
        #print('\n\nNEW CLOSE DATA VALUE\n\n')
        for comparison in range(5,16): #Different days considered for comparison
           # print(f'\nNEW COMPARISON RATIO: {comparison}')
            trues = 0
            falses = 0
            daily_ratio_values = []
            weekly_ratio_values = []
            
            for index, _ in enumerate (close_data):
                daily_ratio_values.append(daily_ratio_calculation(index, close_data))

                weekly_ratio_values.append(weekly_ratio_calculation(index, comparison, close_data))
                #print(weekly_ratio_values, comparison, index, close_data[index], close_data[index-comparison])

                if len(weekly_ratio_values) >= 16:
                    weekly_ratio_average = weekly_ratio_average_calculations(weekly_ratio_values, comparison)
                    #print(weekly_ratio_average, comparison, index, close_data[index], close_data[index-comparison], len(weekly_ratio_values), weekly_ratio_values)
                    weekly_ratio_standard_deviation = weekly_ratio_standard_deviation_calculation(weekly_ratio_values)
                    #print(weekly_ratio_standard_deviation, comparison, index)

                    #Step 5-12                   
                    true_count, false_count = simulation_and_probability_calculations(index, close_data, weekly_ratio_average,  weekly_ratio_standard_deviation)
                    if true_count > 0 or false_count > 0 and close_data[index] not in day_prices:
                        day_prices.append(close_data[index])
                    trues += true_count
                    falses += false_count
        
            #print(close_data)
            #print(daily_ratio_values)

            total_true_count.append(trues)
            total_false_count.append(falses)
            print(len(total_false_count), total_true_count, total_false_count)

            #print(day_prices)
            if comparison == 15:
                try:
                    print(f"Probability: {(sum(total_true_count) / (sum(total_false_count) + sum(total_true_count))) * 100}%")
                except:
                    pass # Div by 0
            #print(weekly_ratio_values)
        

#write it so only ONE simulation average for ONE CLOSE DAY gets sent after the second enumerate 