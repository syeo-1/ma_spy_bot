import processing
import sys
from collections import deque
import numpy as np
import json
import scipy.signal as ss
import actions
import matplotlib.pyplot as plt

def run_backtest_bot():
    test_data = open('GME_quote_data.txt', 'r')
    trade_data = deque(maxlen=200)

    buys = []
    sells = []
    buy_x = []
    sell_x = []

    buy = True
    sell = False

    win_length = 99
    poly_order = 3

    ind = 0
    profit = 0
    current_buy_price = None

    sg_values = []

    for msg in test_data:
        processed_msg = processing.jsonify_stream_data(msg)
        trade_data.append(processed_msg['data']['p'])
        # # once hit maxlen, start attempting trades
        if len(trade_data) == 200:
            sg_bids_deriv1 = ss.savgol_filter(trade_data, win_length, poly_order, deriv=1)
            sg_values.append(sg_bids_deriv1[len(sg_bids_deriv1)-1])
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

    print(profit)
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

    axs[1].plot(sg_bids_deriv1)

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
    # # trade_prices = [msg['data']['p'] for msg in processing.jsonify_recorded_data('GME_quote_data.txt')]
    # # print(trade_prices)
    # axs[0].plot(a)
    # # plt.plot(a)
    # plt.show()
    main()
