import calculations
import data


def main():
    while True:
        try:
            user_input = input("Enter a stock: ")
            days = int(input("Enter preferred days: "))
            if days >0:
                break
        except:
            print("Enter a valid amount of days")
    open_days, daily_open, daily_close, daily_high, daily_low = data.getOCHLData(user_input, days) #Not close data, rather, open; we need Adj Close
    #print(close_data)
    calculations.mathematics(daily_close)

if __name__ == "__main__":
    main()