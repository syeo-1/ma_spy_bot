import concurrent.futures
import processing
import sys
from collections import deque
import numpy as np
import json
import scipy.signal as ss
import actions
import matplotlib.pyplot as plt
from profile_decorator import profiler
import math
import multiprocessing
from sklearn import preprocessing
import plotter

trade_prices = [msg['data']['p'] for msg in processing.jsonify_recorded_data('GME_quote_data.txt')]

manager = multiprocessing.Manager()

shared_data = manager.list()

overall_best_filterlength = manager.Value('i', -1)
overall_best_maxmin_range = manager.Value('d', -1.0)
overall_max_profit = manager.Value('d', -1.0)

best_param_file = 'param_file.txt'


def run_prod_bot():
    pass


def get_diff(first, second):
    return second - first

def get_stream_data_prices(prices, filterlength, maxmin_range):
    test_deque = deque(maxlen=filterlength)
    d_calculations = deque(maxlen=3)
    d1_deque = deque(maxlen=2)
    d1 = None
    d2 = None
    buy = True
    sell = False
    profit = 0

    currentBuy = None
    for price in prices:
        test_deque.append(price)
        if len(test_deque) == filterlength:
            avg = sum(test_deque)/filterlength
            d_calculations.append(avg)
            if len(d_calculations) == 3:
                for i in range(2):
                    d1_deque.append(get_diff(d_calculations[i], d_calculations[i+1]))
                d1 = d1_deque[1]
                d2 = get_diff(d1_deque[0], d1_deque[1])

                if -maxmin_range < d1 < maxmin_range and d2 > 0 and buy:
                    currentBuy = price
                    buy = False
                    sell = True
                elif -maxmin_range < d1 < maxmin_range and d2 < 0 and sell:
                    currentSell = price
                    profit += currentSell - currentBuy
                    buy = True
                    sell = False
                
    return profit



def moving_avg_testing(filterlengths):
    maxmin_ranges = np.linspace(0.0001, 0.015, 1, endpoint=True)
    max_profit = -math.inf
    best_filterlength = None
    best_maxmin_range = None

    ind = 0
    for filterlength in range(filterlengths[0], filterlengths[1]):
        for maxmin_range in maxmin_ranges:
            profit = get_stream_data_prices(trade_prices, filterlength, maxmin_range)
            shared_data.append({
                'profit': profit,
                'filterlength': filterlength,
                'maxmin_range': maxmin_range
            })
            if profit > max_profit:
                max_profit = profit
                best_filterlength = filterlength
                best_maxmin_range = maxmin_range
            print(ind)
            ind+=1

    if max_profit > overall_max_profit.value: 
        overall_max_profit.value = max_profit
        overall_best_filterlength.value = best_filterlength
        overall_best_maxmin_range.value = best_maxmin_range
    



@profiler
def run_backtest_bot():
    '''backtest strategy using recorded data'''
    with concurrent.futures.ProcessPoolExecutor() as executor:
        filterlengths = [
            [150, 175],
            [175, 200],
            [200, 225],
            [225, 250]
        ]
        results = executor.map(moving_avg_testing, filterlengths)
    
    # print(results)
    for result in results:
        print(result)

    # get rid of oldest data in file if more than 1 weeks worth of param data
    trading_param_file = open(best_param_file, 'r')
    new_file_contents = []
    if len(trading_param_file.readlines()) == 8:

        # reset file pointer position after confirming 8 lines
        trading_param_file.seek(0, 0)

        # skip reading the oldest param data
        line_count = 1
        for line in trading_param_file:
            if line_count == 2:
                line_count += 1
                continue
            new_file_contents.append(line)
            line_count += 1
            # print(line)
        print(new_file_contents)
        
        
        # overwrite the file without the oldest date's best params
        trading_param_file = open(best_param_file, 'w')
        for line in new_file_contents:
            trading_param_file.write(line)
        print(new_file_contents)
        
        # close the file
        trading_param_file.close()
    
    # print(len(trading_param_file.readlines()))


    # append most recent day's best params to the file
    trading_param_file = open(best_param_file, 'a')
    trading_param_file.write(f'''\n{overall_max_profit.value},{overall_best_filterlength.value},{overall_best_maxmin_range.value}''')
    trading_param_file.close()

    # plotter.plot_dict_list(shared_data,'profit')


def main():
    run_type = sys.argv[1]
    if run_type == 'test':
        run_backtest_bot()
    elif run_type == 'prod':
        print('going live!!!')
    else:
        print('invalid run_type given. Please give either test or prod')
        exit(1)


if __name__ == '__main__':
    main()