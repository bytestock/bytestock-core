from datetime import datetime
import time

def getDateTimefromTicks(ticks):
    date = datetime.fromtimestamp(ticks).strftime('%Y-%m-%d %H:%M:%S')

    return date

def getDayFromDate(date):
    day = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

    return day

def getMarketCloseDates():
    with open('market-closed-dates.txt') as file:
        lines = file.readlines()

    return lines

def isMarketClosed(ticks):
    date = getDateTimefromTicks(ticks).split(' ')[0]
    
    market_closed_dates = getMarketCloseDates()
    day = getDayFromDate(date)

    if date in market_closed_dates:
        return True
    elif day == 'Saturday' or day == 'Sunday':
        return True
    else:
        return False

def wasMarketClosedFrom(start, end):
    diff = end - start
    days = diff // 86400

    market_open_days = []
    market_closed_days = []

    for i in range(days):
        current = start + i * 86400
        current_date = getDateTimefromTicks(current)

        market_closed = isMarketClosed(current)

        if market_closed:
            market_closed_days.append(current_date)
        else:
            market_open_days.append(current_date)

    return market_open_days, market_closed_days

def telemetry(ticker, days):
    ticks = int(time.time())

    with open('telemetry.txt') as f:
        lines = f.readlines()

        timestamp = lines[-1].rstrip().split(' ')[2]

    if timestamp == str(ticks):
        print('RATELIMITED')
        time.sleep(1.25)
        ticks = int(time.time())

    with open('telemetry.txt', 'w') as file:
        lines.append(f'{ticker} {days} {ticks}\n')
        file.write(''.join(lines))

        return True



