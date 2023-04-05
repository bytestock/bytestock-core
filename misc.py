"""Libraries"""
from datetime import datetime  # importing the datetime module to get the current date and time
import time # importing the time module to get the current time


class Misc: 
    """Miscellaneous Functions Class"""
    def __init__(self,ticks, date, start, end) -> None: # initializing the class
        self.ticks = ticks
        self.date = date
        self.start = start
        self.end = end
    
    def getDateTimefromTicks(self): # getting the date from the ticks

        return datetime.fromtimestamp(self.ticks).strftime('%Y-%m-%d %H:%M:%S') # getting the date from the ticks
    
    def getFancyDateTimefromTicks(self): # getting the date from the ticks

        return datetime.fromtimestamp(self.ticks).strftime('%b %d %Y') # getting the date from the ticks

    
    def getDayFromDate(self): # getting the day from the date

        return datetime.strptime(self.date, '%Y-%m-%d').strftime('%A') # getting the day from the date

    def getMarketCloseDates(self): # getting the market closed dates
        with open('market-closed-dates.txt') as file:
            lines = file.readlines()

        return lines # returning the market closed dates
    
    def isMarketClosed(self): # checking if the market is closed
        date = self.getDateTimefromTicks().split(' ')[0]

        market_closed_dates = self.getMarketCloseDates() # getting the market closed dates
        day = self.getDayFromDate() # getting the day from the date

        if date in market_closed_dates: # checking if the date is in the market closed dates
            return True
        elif day == 'Saturday' or day == 'Sunday': # checking if the day is a weekend
            return True
        else:
            return False
        
    def wasMarketClosedFrom(self): # checking if the market was closed from a certain date
        market_open_days = []
        market_closed_days = []

        for i in range(self.date): # looping through the days
            current = self.start + i * 86400 
            current_date = self.getFancyDateTimefromTicks() # getting the date from the ticks

            market_closed = self.isMarketClosed() # checking if the market is closed

            if market_closed: # checking if the market is closed
                market_closed_days.append(current_date)
            else: # checking if the market is open
                market_open_days.append(current_date)

        return market_open_days, market_closed_days
    
    def telemetry(self):  # telemetry
        ticks = int(time.time()) # getting the current time

        with open('telemetry.txt') as f:
            lines = f.readlines()

            timestamp = lines[-1].rstrip().split(' ')[2]

        if timestamp == str(ticks): # checking if the timestamp is the same as the current time
            print('RATELIMITED')
            time.sleep(1.25)
            ticks = int(time.time())

        with open('telemetry.txt', 'w') as file:
            lines.append(f'{self.ticks} {self.date} {ticks}\n')
            file.write(''.join(lines))

            return True # returning True if the telemetry was successful
        


