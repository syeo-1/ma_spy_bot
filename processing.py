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
    
def record_best_param_data(data, filename):
    ''' append current best parameter data to specified file '''

    # get rid of oldest data in file if more than 1 weeks worth of param data
    trading_param_file = open(filename, 'r')
    new_file_contents = []
    if len(trading_param_file.readlines()) == 8:

        # reset file pointer position after confirming 8 lines
        trading_param_file.seek(0, 0)

        # skip reading the oldest param data
        line_count = 1
        for line in trading_param_file:
            if line_count == 2:
                line_count += 1
                continue
            new_file_contents.append(line)
            line_count += 1
        
        # overwrite the file without the oldest date's best params
        trading_param_file = open(filename, 'w')
        for line in new_file_contents:
            trading_param_file.write(line)
        
        # close the file
        trading_param_file.close()
    
    # append most recent day's best params to the file
    trading_param_file = open(filename, 'a')
    trading_param_file.write(f'''\n{data["best_profit"]},{data["best_filterlength"]},{data["best_maxmin_range"]}''')
    trading_param_file.close()
    
def record_shared_data(shared_data, shared_data_file):
    ''' records the used params vs profits data to a text file '''

    # sort the shared data
    sorted_shared_data = sorted(shared_data, key=lambda k: k['profit'], reverse=True)

    with open(shared_data_file, 'w+') as output:
        for dic in sorted_shared_data:
            output.write(json.dumps(dic)+'\n')


# demo/test below
# the below will only run if the file is being called directly!
# ie. 'python3 processing.py'
# if the below is being imported, then below will not run!
if __name__ == '__main__':
    a = jsonify_recorded_data("GME_quote_data.txt")
    b = get_recorded_data(a, 'P')
    print(b)
