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

        print(f"bid: {data['data']['p']} ask: {data['data']['P']}")
        # current_date = datetime.datetime.fromtimestamp(float(data["data"]["t"])/1e9)
        i+=1
        if i == 100:
            break
    sg_bids = ss.savgol_filter(bids, 99, 3)
    bids_deriv1 = np.ediff1d(bids)
    sg_bids_deriv1 = ss.savgol_filter(bids, 99, 3, deriv=1)
    # plt.plot(bids)
    # plt.plot(sg_bids)
    fig, axs = plt.subplots(2)
    fig.suptitle('stock info!')
    axs[0].plot(bids)
    axs[0].plot(sg_bids)
    axs[1].plot(bids_deriv1)
    axs[1].plot(sg_bids_deriv1)
    # plt.plot(asks)
    plt.ylabel('some numbers')
    # ill be looking for the minimum ask prices and the maximum bid prices!!!!
    plt.show()

if __name__ == "__main__":
    stream_data()