"""Libraries"""
import calculations # importing the calculations module to use its functions
import data # importing the data module to use its functions


def main()->None: # creating the main() functions
    """Main Function"""
    while True: # infinite loop
        try: # ensuring that the user enters a valid number
            user_input = input("Enter a stock: ") # asking the user to enter a stock
            days = int(input("Enter preferred days: ")) # asking the user for the number of days
            if days >0: # break if the number of days is greater than 0
                break
        except ValueError: # asking the user to enter a valid number of days
            print("Enter a valid amount of days")
    open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low = data.getOCHLData(user_input, days) #Not close data, rather, open; we need Adj Close
    with open("close-data.txt", "w") as f:
        for val in daily_adj_close:
            f.write(str(val)+"\n")
        f.close()

    calculations.mathematics(daily_adj_close)

"""Main Program"""
if __name__ == "__main__":
    main() # calling the main function
