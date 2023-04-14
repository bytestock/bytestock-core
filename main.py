"""Libraries"""
import calculations # importing the calculations module to use its functions
from data import Data # importing the data module to use its functions
import subprocess # importing the subprocess module to use its functions


def main(stock, days)->None: # creating the main() functions
    """Main Function"""
    get_data = Data(stock, days) # creating an instance of the Data class
    open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low = get_data.getOCHLData() # getting the data from the Data class
    with open("close-data.txt", "w") as f: # writing the data to a file
        for val in daily_adj_close: # looping through the data
            f.write(str(val)+"\n") # writing the data to the file
        f.close() # closing the file

<<<<<<< Updated upstream
   
    args = ("./calc") # creating the arguments for the subprocess
    popen = subprocess.Popen(args, stdout=subprocess.PIPE) # creating the subprocess
=======
    open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low = data.getOCHLData(stock, days) #Not close data, rather, open; we need Adj Close
    with open("close-data.txt", "w") as f:
        for val in daily_adj_close:
            f.write(str(val)+"\n")
        f.close()

    #calculations.mathematics(daily_adj_close)
    args = ("./bytestock-core/calc")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
>>>>>>> Stashed changes
    popen.wait()
    output = popen.stdout.readlines()
    with open('output.txt', 'w') as f: # writing the output to a file
        for output_line in output:
            output_line = str(output_line)
            period = output_line.split(' ')[1].split(' ')[0]
            probability = output_line.split(' ')[3].split(' ')[0]

            newline = f'Period:{period}:Probability:{probability}\n'
            f.write(newline) # writing the data to the file


