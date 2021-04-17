# import candlestick_pattern_detect
import config
import json
import datetime
import numpy
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
        # if i == 5000:
        #     break
    sg_bids = ss.savgol_filter(bids, 99, 3)
    plt.plot(bids)
    plt.plot(sg_bids)
    # plt.plot(asks)
    plt.ylabel('some numbers')
    # ill be looking for the minimum ask prices and the maximum bid prices!!!!
    plt.show()

if __name__ == "__main__":
    stream_data()