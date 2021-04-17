# import candlestick_pattern_detect
import config
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

def stream_data():
    # i = 0
    bids = []
    i = 0
    for data in open(config.RECORDED_DATA, "r"):
        data = json.loads(data)

        bids.append(data['data']['p'])
        # asks.append(data['data']['P'])

        # print(f"bid: {data['data']['p']} ask: {data['data']['P']}")
        # current_date = datetime.datetime.fromtimestamp(float(data["data"]["t"])/1e9)
        i+=1
        # if i == 100:
        #     break
    sg_bids = ss.savgol_filter(bids, 99, 3)
    bids_deriv1 = np.ediff1d(bids)
    sg_bids_deriv1 = ss.savgol_filter(bids, 99, 3, deriv=1)
    bids_deriv2 = np.ediff1d(bids_deriv1)
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

if __name__ == "__main__":
    stream_data()