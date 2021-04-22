'''streaming symbol meanings: https://alpaca.markets/docs/api-documentation/api-v2/market-data/alpaca-data-api-v1/streaming/'''
import json

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
# the below will only run if the file is being called directly!
# ie. 'python3 processing.py'
# if the below is being imported, then below will not run!
if __name__ == '__main__':
    a = jsonify_recorded_data("GME_quote_data.txt")
    b = get_recorded_data(a, 'P')
    print(b)
