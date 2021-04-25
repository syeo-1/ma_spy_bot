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

# test_data = open('GME_quote_data.txt', 'r')
processed_test_data = [data['data']['p'] for data in processing.jsonify_recorded_data('GME_quote_data.txt')]
# print(processed_test_data)


def test_params(winlength, polyorder, maxmin_range, deque_length):
    trade_data = deque(maxlen=deque_length)
    data_point = 0
    profit = 0

    current_buy_price = None
    buy = True
    sell = False

    for price in processed_test_data:
        data_point += 1
        if data_point == 2050:
            break
        trade_data.append(price)
        # # once hit maxlen, start attempting trades
        if len(trade_data) == deque_length:
            # print('test')
            # sg_bids = ss.savgol_filter(trade_data, win_length, poly_order)
            # sg_og.append(sg_bids[len(sg_bids)-1])
            sg_bids_deriv1 = ss.savgol_filter(trade_data, winlength, polyorder, deriv=1)
            # sg_values.append(sg_bids_deriv1[len(sg_bids_deriv1)-1])
            sg_bids_deriv2 = ss.savgol_filter(trade_data, winlength, polyorder, deriv=2)

        #     # check most recently processed elements
            if -maxmin_range < sg_bids_deriv1[len(sg_bids_deriv1)-1] < maxmin_range:
                if sg_bids_deriv2[len(sg_bids_deriv2)-1] > 0 and buy:
                    # buy
                    # print(sg_bids_deriv2[199])
                    # actions.market_buy(buys, processed_msg['data']['p'])
                    # buy_x.append(ind)
                    buy = False
                    sell = True
                    current_buy_price = price

                elif sg_bids_deriv2[len(sg_bids_deriv2)-1] < 0 and sell:
                    # print(sg_bids_deriv2[199])
                    # actions.market_sell(sells, processed_msg['data']['p'])
                    # sell_x.append(ind)
                    buy = True
                    sell = False
                    current_sell_price = price
                    profit += current_sell_price - current_buy_price
    return profit



def find_max_profit_pattern():
    # vary between winlength, polyorder, deque_length, and maxmin_range
    # polyorder only really needs to go up to 5
    # winlength can range from 300 to 400
    # maxmin_range can go from 0.0005 to 0.0100 (20 values), use np linspace
    # deque length can go from 100 to 200
    # only do up to the first 1250 data points
    
    # initialize maxmin_ranges
    maxmin_ranges = np.linspace(0.005, 0.1, 20, endpoint=True)
    max_profit = -math.inf

    best_polyorder = None
    best_winlength = None
    best_maxminrange = None
    best_dequeLength = None

    i = 0
    for polyorder in range(2, 6):
        for winlength in range(101, 200, 2):
            for maxmin_range in maxmin_ranges:
                for deque_length in range(200, 250):
                    profit = test_params(winlength, polyorder, maxmin_range, deque_length)
                    if profit > max_profit:
                        max_profit = profit
                        best_polyorder = polyorder
                        best_winlength = winlength
                        best_maxminrange = maxmin_range
                        best_dequeLength = deque_length
                    i+=1
                    print(i)
                break
            break
        break
    print("======")
    print(best_winlength)
    print(best_polyorder)
    print(best_maxminrange)
    print(best_dequeLength)
    print(max_profit)





@profiler
def run_backtest_bot():
    test_data = open('GME_quote_data.txt', 'r')
    # trade_data = deque(maxlen=1000)
    trade_data = deque(maxlen=400)

    buys = []
    sells = []
    buy_x = []
    sell_x = []

    buy = True
    sell = False

    win_length = 199
    poly_order = 5

    ind = 0
    profit = 0
    current_buy_price = None

    sg_values = []
    sg_og = []

    ''' delete block directly below later'''
    data_p = 0
    to_plot = []
    for msg in test_data:
        data_p += 1
        if data_p == 1_250:
            break
        processed_msg = processing.jsonify_stream_data(msg)
        trade_data.append(processed_msg['data']['p'])
        # # once hit maxlen, start attempting trades
        if len(trade_data) == 400:
            # winlength = 199
            # poly_order = 5
            sg_bids = ss.savgol_filter(trade_data, win_length, 3)
            to_plot.append(sg_bids[len(sg_bids)-1])

    processed_data = processing.jsonify_recorded_data('GME_quote_data.txt')
    non_processed_prices = [data['data']['p'] for ind, data in enumerate(processed_data) if 400 <= ind < 1_250]
    savgol_prices = ss.savgol_filter(non_processed_prices, win_length, poly_order)

    # fig, axs = plt.subplots(3)
    # # fig.set_figheight(8)
    # # fig.set_figwidth(8)
    # fig.suptitle('trends for smoothing')
    # # plot first 50_000 price points as they are
    # axs[0].plot(non_processed_prices)
    # # plot first 50_000 price points using savgol filter on entire data
    # axs[1].plot(savgol_prices)
    # # plot first 50_000 price points using savgol filter on stream
    # axs[2].plot(to_plot)
    # # print(to_plot)

    # # maxout plot window size
    # # figManager = plt.get_current_fig_manager()
    # # figManager.window.showMaximized()

    # plt.show()
     
    # exit(0)
    return

    data_point = 0
    for msg in test_data:
        data_point += 1
        if data_point == 51_000:
            break
        processed_msg = processing.jsonify_stream_data(msg)
        trade_data.append(processed_msg['data']['p'])
        # # once hit maxlen, start attempting trades
        if len(trade_data) == 1000:
            # sg_bids = ss.savgol_filter(trade_data, win_length, poly_order)
            # sg_og.append(sg_bids[len(sg_bids)-1])
            sg_bids_deriv1 = ss.savgol_filter(trade_data, win_length, poly_order, deriv=1)
            # sg_values.append(sg_bids_deriv1[len(sg_bids_deriv1)-1])
            sg_bids_deriv2 = ss.savgol_filter(trade_data, win_length, poly_order, deriv=2)

        #     # check most recently processed elements
            if -0.009 < sg_bids_deriv1[len(sg_bids_deriv1)-1] < 0.009:
                if sg_bids_deriv2[len(sg_bids_deriv2)-1] > 0 and buy:
                    # buy
                    # print(sg_bids_deriv2[199])
                    actions.market_buy(buys, processed_msg['data']['p'])
                    buy_x.append(ind)
                    buy = False
                    sell = True
                    current_buy_price = processed_msg['data']['p']

                elif sg_bids_deriv2[len(sg_bids_deriv2)-1] < 0 and sell:
                    # print(sg_bids_deriv2[199])
                    actions.market_sell(sells, processed_msg['data']['p'])
                    sell_x.append(ind)
                    buy = True
                    sell = False
                    current_sell_price = processed_msg['data']['p']
                    profit += current_sell_price - current_buy_price
        ind+=1
        if ind == 100_000:
            break

    print(profit)
    # print(len(sg_values))
    # get prices
    trade_prices = [msg['data']['p'] for msg in processing.jsonify_recorded_data('GME_quote_data.txt')]

    
    # plot everything together
    fig, axs = plt.subplots(2)
    fig.set_figheight(8)
    fig.set_figwidth(8)

    fig.suptitle('buys and sells')

    # plot out the prices
    axs[0].plot(trade_prices)
    # plot out the buys
    axs[0].scatter(buy_x, buys, c="green", zorder=2)
    # plot out the sells
    axs[0].scatter(sell_x, sells, c="red", zorder=2)

    axs[1].plot(sg_values)
    # axs[1].plot(sg_og)


    plt.show()

            


def run_prod_bot():
    pass

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
    # fig, axs = plt.subplots(2)
    # fig.set_figheight(8)
    # fig.set_figwidth(8)
    # a = []
    # for msg in processing.jsonify_recorded_data('GME_quote_data.txt'):
    #     a.append(msg['data']['p'])
    # trade_prices = [msg['data']['p'] for msg in processing.jsonify_recorded_data('GME_quote_data.txt')]
    # sagol = ss.savgol_filter(trade_prices, 199, 20)
    # # # print(trade_prices)
    # axs[0].plot(a)
    # axs[1].plot(sagol)
    # plt.plot(a)
    # plt.show()
    # main()
    find_max_profit_pattern()