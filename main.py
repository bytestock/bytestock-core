import calculations
import data


def main():
    user_input = input("Enter a stock: ")
    days = int(input("Enter prefered days: "))
    close_data = data.getOCHLData(user_input, days)[1]
    print(close_data)
    calculations.potential_chance(close_data, (days))


if __name__ == "__main__":
    main()