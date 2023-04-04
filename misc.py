from datetime import datetime
import time


class Misc:
    def __init__(self,ticks, date, start, end) -> None:
        self.ticks = ticks
        self.date = date
        self.start = start
        self.end = end
    
    def getDateTimefromTicks(self):
        date = datetime.fromtimestamp(self.ticks).strftime('%Y-%m-%d %H:%M:%S')

        return date
    
    def getFancyDateTimefromTicks(self):
        date = datetime.fromtimestamp(self.ticks).strftime('%b %d %Y')

        return date
    
    def getDayFromDate(self):
        day = datetime.strptime(self.date, '%Y-%m-%d').strftime('%A')

        return day

    def getMarketCloseDates(self):
        with open('market-closed-dates.txt') as file:
            lines = file.readlines()

        return lines
    
    def isMarketClosed(self):
        date = self.getDateTimefromTicks().split(' ')[0]
        
        market_closed_dates = self.getMarketCloseDates()
        day = self.getDayFromDate()

        if date in market_closed_dates:
            return True
        elif day == 'Saturday' or day == 'Sunday':
            return True
        else:
            return False
        
    def wasMarketClosedFrom(self):
        market_open_days = []
        market_closed_days = []

        for i in range(self.date):
            current = self.start + i * 86400
            current_date = self.getFancyDateTimefromTicks()

            market_closed = self.isMarketClosed()

            if market_closed:
                market_closed_days.append(current_date)
            else:
                market_open_days.append(current_date)

        return market_open_days, market_closed_days
    
    def telemetry(self):
        ticks = int(time.time())

        with open('telemetry.txt') as f:
            lines = f.readlines()

            timestamp = lines[-1].rstrip().split(' ')[2]

        if timestamp == str(ticks):
            print('RATELIMITED')
            time.sleep(1.25)
            ticks = int(time.time())

        with open('telemetry.txt', 'w') as file:
            lines.append(f'{self.ticks} {self.date} {ticks}\n')
            file.write(''.join(lines))

            return True
        


