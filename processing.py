'''streaming symbol meanings: https://alpaca.markets/docs/api-documentation/api-v2/market-data/alpaca-data-api-v1/streaming/'''
import json

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

def jsonify_recorded_data(filename):
    '''turns recorded text data from a file and returns a list of dictionaries'''
    processed_data = []

    for line in open(filename, "r"):
        processed_line = json.loads(line)
        processed_data.append(processed_line)

    return processed_data

def jsonify_stream_data(data):
    '''turns single websocket message into a dictionary'''
    return json.loads(data)

def get_streamed_quote_data(data, key):
    '''return specified quote data given a key'''
    return data['data'][key]

def get_recorded_data(data, key):
    '''return list of specified quote data given a key'''
    return [quote['data'][key] for quote in data]
    

# demo/test below
a = jsonify_recorded_data("GME_quote_data.txt")
b = get_recorded_data(a, 'P')
print(b)
