def potential_chance(close_data,days):
    adj_close_count = 0
    prev_adj_close= close_data[0]
    for i in range(0,days):
        current_adj_close = float(close_data[i])
        adj_close_count +=1
        if adj_close_count >1:
            try:
                print(current_adj_close, prev_adj_close)
                daily_ratio = current_adj_close/prev_adj_close
                print(daily_ratio)
            except:
                print("Error with adj close")
            prev_adj_close = current_adj_close