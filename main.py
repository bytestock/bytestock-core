"""Libraries"""
import calculations
import data


def main()->None:
    """Main Function"""
    while True:
        try:
            user_input = input("Enter a stock: ")
            days = int(input("Enter preferred days: "))
            if days >0:
                break
        except ValueError:
            print("Enter a valid amount of days")
    open_days, daily_open, daily_close, daily_adj_close, daily_high, daily_low = data.getOCHLData(user_input, days) #Not close data, rather, open; we need Adj Close
    calculations.mathematics(daily_adj_close)

"""Main Program"""
if __name__ == "__main__":
    main()