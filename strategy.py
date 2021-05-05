from collections import deque
import scipy.signal as ss
import config
import requests
import json

class BaseStrategy(object):
    ''' base strategy for buying, selling and processing a security on Alpaca. Redefine as necessary '''
    def __init__(self, buy=None, sell=None, process=None):
        if buy:
            self.buy = buy
        if sell:
            self.sell = sell
        if process:
            self.process = process
    
    def buy(self):
        ''' give an argument for defining a buy function depending on strategy '''
        print('buying security functionality not defined')
        exit(1)

    def sell(self):
        ''' give an argument for defining a sell function depending on strategy '''
        print('selling security functionality not defined')
        exit(1)

    def process(self):
        ''' give an argument for defining a processing function depending on strategy '''
        print('processing stream data functionality not defined')
        exit(1)

def StrategyFactory(name, buy=None, sell=None, process=None, BaseStrategy=BaseStrategy, argnames=None):
    def __init__(self, **strategy_vars):
        for key, value in strategy_vars.items():
            if key not in argnames:
                raise TypeError(f'argument {key} not valid for {self.__class__.__name__}')
            setattr(self, key, value)
        BaseStrategy.__init__(self)
    
    strategy_instance = type("test")

'''ABOVE WILL BE FOR FUTURE EXPANSION/STRATEGIES ''' 
####################################################

HEADERS = {'APCA-API-KEY-ID': config.ALPACA_API_KEY, 'APCA-API-SECRET-KEY': config.ALPACA_SECRET_KEY}

class MovingAvgStrat(object):
    ''' Use moving averages to smooth out data to find local maxima and minima in price streams'''
    def __init__(self, filterlength, maxmin_range):
        self.data = deque(maxlen=filterlength)
        self.data_d1_calc = deque(maxlen=3)
        self.data_d1 = deque(maxlen=2)
        self.d1 = None
        self.d2 = None
        self.buy = True
        self.sell = False

    def buy_security(self):
        ''' create a market buy order for the specified security'''

        buy_order_info = {
            "symbol": config.STOCK_NAME,
            "qty": 1, # buy a single share for now
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
        }

        r = requests.post(config.ORDERS_URL, json=buy_order_info, headers=HEADERS)
        response = json.loads(r.content)
        print('just bought 1 share!')

        print(response)

    def sell_security(self):
        ''' create a market sell order for the share that has been bought '''

        buy_order_info = {
            "symbol": config.STOCK_NAME,
            "qty": 1, 
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
        }
        r = requests.post(config.ORDERS_URL, json=buy_order_info, headers=HEADERS)
        response = json.loads(r.content)

        print('just sold 1 share!')

        print(response)

    def process_security(self, stream_price):
        ''' process data from the stream and buy and sell using specified strategy '''
        self.data.append(stream_price)
        if len(self.data) == self.filterlength:
            avg = sum(self.data)/self.filterlength
            self.data_d1_calc.append(avg)
            if len(self.data_d1_calc) == 3:
                for i in range(2):
                    self.data_d1.append(self.data_d1_calc[i+1]-self.data_d1_calc[i])
                self.d1 = self.data_d1[1]
                self.d2 = self.data_d1[1]-self.data_d1[0]

                if -self.maxmin_range < self.d1 < self.maxmin_range and self.d2 > 0 and self.buy:
                    self.buy_security()
                    self.buy = False
                    self.sell = True
                elif -self.maxmin_range < self.d1 < self.maxmin_range and self.d2 < 0 and self.sell:
                    self.sell_security()
                    self.buy = True
                    self.sell = False

if __name__ == '__main__':
    # create instance of movingAvgStrat
    test = MovingAvgStrat(200, 0.001)
    test.sell_security()
    print('test')