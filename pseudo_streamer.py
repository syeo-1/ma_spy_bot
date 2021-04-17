# import candlestick_pattern_detect
import config
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

# the parameters I need to mess with
# the range that a local min/max should be detected
# the window length param of sagol
# whatever that 3rd parameter of sagol is



def param_guesser(bids):
    # initial_balance = 400_000
    # max_profit = -inf
    # maxmin_range = 0.0001
    best_polyorder = None
    best_window_length = None
    best_maxmin_range = None
    # if polyorder is one less than win_length, then its a perfect fit, which is not wanted
    # iteration = 1
    # for win_length in range(3, 200, 2):
    #     print(f"current iteration: {iteration}")
    #     for poly_order in range(1, winlength-1):
    #         while maxmin_range < 1:
    #             profit = test_params(win_length, poly_order, maxmin_range)
    #             if profit > max_profit:
    #                 max_profit = profit
    #                 best_window_length = win_length
    #                 best_polyorder = polyorder
    #                 best_maxmin_range = maxmin_range
    #             maxmin_range+=0.0001
    #     iteration += 1

    # try plotting basic stuff first
    test_win_length = 99
    test_polyorder = 3
    test_maxmin_range = 0.0001
    action_data = test_params(bids, test_win_length, test_polyorder, test_maxmin_range)
    # print(action_data)
    # print(f"best window length: {best_window_length}")
    # print(f"best polyorder: {best_polyorder}")
    # print(f"best maxmin range: {best_maxmin_range}")
    # return [test_win_length, test_polyorder, test_maxmin_range]
    return {
        "win_length": test_win_length,
        "polyorder": test_polyorder,
        "maxmin_range": test_maxmin_range,
        "action_data": action_data
    }

def plot_params_vs_profit(win_lengths, polyorders, maxmin_ranges, profits):
    '''
    takes profit and the parameters and plots 4 line graphs for each piece of data
    '''

    # sort profits, and then sort the other arrays based on the ordering of profits before plotting
    pass

def plot_best_actions(bids, bids_deriv1, bids_deriv2, buys_x, buys_y, sells_x, sells_y):
    '''
    plot the optimal buys and sells on the price and price derivative graphs
    '''
    fig, axs = plt.subplots(3)
    fig.set_figheight(8)
    fig.set_figwidth(8)
    fig.suptitle('stock info!')
    axs[0].plot(bids)

    # x and y arrays must have the same size. ie, the must have the same number of elements!!!!
    axs[0].scatter(buys_x,buys_y,c="green",zorder=2)
    axs[0].scatter(sells_x,sells_y,c="red",zorder=2)

    axs[1].plot(bids_deriv1)
    # axs[1].plot(sg_bids_deriv1)
    axs[2].plot(bids_deriv2)
    # axs[2].plot(sg_bids_deriv2)
    # for trade in trades:
    #     plt.axvline(x=trade)
    plt.ylabel('some numbers')
    plt.show()

def plot_best_actions_sagol(sg_bids, sg_bids_deriv1, sg_bids_deriv2, buys_x, buys_y, sells_x, sells_y):
    '''
    plot the optimal buys and sells on the price and price derivative graphs with sagol filters
    '''
    # plt.figure(figsize=(8,6))
    fig, axs = plt.subplots(3)
    fig.set_figheight(8)
    fig.set_figwidth(8)
    fig.suptitle('stock info!')
    # fig(num=1, figsize=(8,6), dpi=80)
    # axs[0].plot(bids)
    axs[0].plot(sg_bids)
    # x and y arrays must have the same size. ie, the must have the same number of elements!!!!
    axs[0].scatter(buys_x,buys_y,c="green",zorder=2)
    axs[0].scatter(sells_x,sells_y,c="red",zorder=2)
    # test =  list(range(1000))

    # axs[1].plot(bids_deriv1)
    axs[1].plot(sg_bids_deriv1)
    # axs[2].plot(bids_deriv2)
    axs[2].plot(sg_bids_deriv2)
    # for trade in trades:
    #     plt.axvline(x=trade)
    plt.ylabel('some numbers')
    plt.show()


def test_params(bids, win_length, poly_order, maxmin_range):
    '''
    test out what parameter values will give maximum profit
    '''
    sg_bids = ss.savgol_filter(bids, win_length, poly_order)
    sg_bids_deriv1 = ss.savgol_filter(bids, win_length, poly_order, deriv=1)
    sg_bids_deriv2 = ss.savgol_filter(bids, win_length, poly_order, deriv=2)
    # plt.plot(bids)
    # plt.plot(sg_bids)
    buy = True
    sell = False
    buys_x = []
    buys_y = []
    sells_x = []
    sells_y = []
    profit = 0
    current_buy_price = None
    for i in range(len(bids)):
        if -maxmin_range < sg_bids_deriv1[i] < maxmin_range and sg_bids_deriv2[i] > 0 and buy:
            # print(f'BUY: {i}')
            buys_x.append(i)
            buys_y.append(bids[i])
            current_buy_price = bids[i]
            buy = False
            sell = True
        elif -maxmin_range < sg_bids_deriv1[i] < maxmin_range and sg_bids_deriv2[i] < 0 and sell:
            # print(f'SELL {i}')
            sells_x.append(i)
            sells_y.append(bids[i])
            current_sell_price = bids[i]
            profit += current_sell_price - current_buy_price
            sell = False
            buy = True

    return {
        "profit": profit,
        "buys": {
            "x": buys_x,
            "y": buys_y
        },
        "sells": {
            "x": sells_x,
            "y": sells_y
        }
    }


def process_bid_data():
    '''
    process bid price data for all functions to use
    '''
    bids = []
    for data in open(config.RECORDED_DATA, "r"):
        data = json.loads(data)

        bids.append(data['data']['p'])
    bids_derv1 = np.ediff1d(bids)
    bids_derv2 = np.ediff1d(bids_derv1)

    return {
        "bids": bids,
        "bids_d1": bids_derv1,
        "bids_d2": bids_derv2
    }
    


if __name__ == "__main__":
    # stream_data()
    price_data = process_bid_data()
    best_params = param_guesser(price_data["bids"])
    # print(price_data)
    for item in price_data:
        print(item)
    print(best_params)
    plot_best_actions(
        price_data["bids"],
        price_data["bids_d1"],
        price_data["bids_d2"],
        best_params["action_data"]["buys"]["x"],
        best_params["action_data"]["buys"]["y"],
        best_params["action_data"]["sells"]["x"],
        best_params["action_data"]["sells"]["y"]
        )

    # plot
