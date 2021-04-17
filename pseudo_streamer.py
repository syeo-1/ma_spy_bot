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

# create global data variable for all functions to use
bids = []
i = 0
for data in open(config.RECORDED_DATA, "r"):
    data = json.loads(data)

    bids.append(data['data']['p'])


def param_guesser():
    # initial_balance = 400_000
    max_profit = -inf
    maxmin_range = 0.0001
    best_polyorder = None
    best_window_length = None
    best_maxmin_range = None
    # if polyorder is one less than win_length, then its a perfect fit, which is not wanted
    iteration = 1
    for win_length in range(3, 200):
        print(f"current iteration: {iteration}")
        for poly_order in range(1, winlength-1):
            while maxmin_range < 1:
                profit = test_params(win_length, poly_order, maxmin_range)
                if profit > max_profit:
                    max_profit = profit
                    best_window_length = win_length
                    best_polyorder = polyorder
                    best_maxmin_range = maxmin_range
                maxmin_range+=0.0001
        iteration += 1
    print(f"best window length: {best_window_length}")
    print(f"best polyorder: {best_polyorder}")
    print(f"best maxmin range: {best_maxmin_range}")


def plot_best_params():
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


def test_params(win_length, poly_order, maxmin_range):
    sg_bids = ss.savgol_filter(bids, win_length, poly_order)
    sg_bids_deriv1 = ss.savgol_filter(bids, 99, 3, deriv=1)
    sg_bids_deriv2 = ss.savgol_filter(bids, 99, 3, deriv=2)
    # plt.plot(bids)
    # plt.plot(sg_bids)
    buy = True
    sell = False
    buys_x = []
    buys_y = []
    sells_x = []
    sells_y = []
    for i in range(len(bids)):
        if -0.00001 < sg_bids_deriv1[i] < 0.00001 and sg_bids_deriv2[i] > 0 and buy:
            print(f'BUY: {i}')
            buys_x.append(i)
            buys_y.append(bids[i])
            buy = False
            sell = True
        elif -0.00001 < sg_bids_deriv1[i] < 0.00001 and sg_bids_deriv2[i] < 0 and sell:
            print(f'SELL {i}')
            sells_x.append(i)
            sells_y.append(bids[i])
            sell = False
            buy = True


if __name__ == "__main__":
    stream_data()