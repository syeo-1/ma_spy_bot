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
import config
import argparse
import data_streamer

trade_prices = [msg['data']['p'] for msg in processing.jsonify_recorded_data(config.RECORDED_DATA)]

manager = multiprocessing.Manager()

shared_data = manager.list()

overall_best_filterlength = manager.Value('i', -1)
overall_best_maxmin_range = manager.Value('d', -1.0)
overall_max_profit = manager.Value('d', -1.0)

best_param_file = config.BEST_PARAM_FILE

def get_diff(first, second):
    ''' return the difference between two elements '''
    return second - first

def get_stream_data_prices(prices, filterlength, maxmin_range):
    ''' use a simulated stream of recorded data to test a single pair of parameters '''
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



def moving_avg_testing(filterlengths=None, maxmin=None, linspace_num=None):
    ''' test what parameters to use for moving averages smoothing '''
    maxmin_ranges = None
    if maxmin == None:
        maxmin_ranges = np.linspace(0.002, 0.002, 1, endpoint=True)
    else:
        maxmin_ranges = np.linspace(maxmin[0], maxmin[1], linspace_num, endpoint=True)

    if filterlengths == None:
        filterlengths = [500,501]


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
    



@profiler(run_profiler=False, output_file=config.BACKTEST_PROFILE)
def run_backtest_bot(cli_args):
    '''backtest strategy using recorded data'''
    with concurrent.futures.ProcessPoolExecutor() as executor:
        maxmin_ranges = []
        filterlengths = []
        num_processors = multiprocessing.cpu_count()

        if cli_args.test_type == 'maxmin_range':
            maxmin_upper_range = 0.1
            maxmin_div_size = maxmin_upper_range / num_processors
            maxmin_cur_lower = 0
            for i in range(1, num_processors+1):
                maxmin_ranges.append([maxmin_cur_lower, i*maxmin_div_size])
                maxmin_cur_lower = i*maxmin_div_size

            print(maxmin_ranges)
            executor.map(moving_avg_testing, [None for _ in range(4)], maxmin_ranges, [250 for _ in range(4)])
        else:
            upper_range = 1_000
            division_size = upper_range // num_processors

            current_lower = 0
            for i in range(1, num_processors+1):
                filterlengths.append([current_lower, i*division_size])
                current_lower = i*division_size
            
            print(filterlengths)

            executor.map(moving_avg_testing, filterlengths)

    best_param_data = {
        "best_profit": overall_max_profit.value,
        "best_filterlength": overall_best_filterlength.value,
        "best_maxmin_range": overall_best_maxmin_range.value
    }

    # record the single best param group
    processing.record_best_param_data(best_param_data, best_param_file)

    # record the shared data (all params and profits)
    processing.record_shared_data(shared_data, config.SHARED_DATA_FILE)

    # plot out the data and sort by a given key amongst profit, maxmin_range, or filterlength
    plotter.plot_dict_list(shared_data,'profit')


def run_prod_bot():
    ''' run bot that sends requests to alpaca markets to execute trades '''

    # get most recent optimal parameters from file
    optimal_filterlength = None
    optimal_maxmin_range = None
    with open(best_param_file, 'r') as param_file:
        best_param_data = param_file.readlines()[-1].split(',')
        optimal_filterlength = int(best_param_data[1])
        optimal_maxmin_range = float(best_param_data[2])

    data_streamer.initiliaze_stream('production', optimal_filterlength, optimal_maxmin_range)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('runtype')
    parser.add_argument('--test_type', required=False)
    args = parser.parse_args()
    if args.runtype == 'test':
        run_backtest_bot(args)
    elif args.runtype == 'production':
        run_prod_bot()
    else:
        print('invalid run_type given. Please give either test or prod')
        exit(1)

    

if __name__ == '__main__':
    main()