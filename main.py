"""Libraries"""
import calculations # importing the calculations module to use its functions
from data import Data # importing the data module to use its functions
import subprocess


def main(stock, days)->None: # creating the main() functions
    """Main Function"""
    get_data = Data(stock, days) # creating an instance of the Data class
    open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low = get_data.getOCHLData() #Not close data, rather, open; we need Adj Close
    with open("close-data.txt", "w") as f:
        for val in daily_adj_close:
            f.write(str(val)+"\n")
        f.close()

    #calculations.mathematics(daily_adj_close)
    args = ("./calc")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readlines()
    with open('output.txt', 'w') as f:
        for output_line in output:
            output_line = str(output_line)
            period = output_line.split(' ')[1].split(' ')[0]
            probability = output_line.split(' ')[3].split(' ')[0]

            newline = f'Period:{period}:Probability:{probability}\n'
            f.write(newline)


