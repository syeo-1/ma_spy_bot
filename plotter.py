'''use this file for creating plots with matplotlib'''
import matplotlib.pyplot as plt
import config
import json

def plot_dict_list(dict_ls, sortkey):
    ''' takes a list of dictionaries and plots linegraphs for the values '''
    ''' sort the values based on a common key in a dictionary '''

    plot_colors = ['green', 'blue', 'orange']

    if len(dict_ls[0]) != len(plot_colors):
        print('number of plots doesn\'t match number of colors. Please add colors or remove plots' )
        exit(1)

    sortby = sorted(dict_ls, key=lambda k: k[sortkey])

    # sort the data
    sorted_datas = []
    for key in dict_ls[0]:
        sorted_datas.append([data[key] for data in sortby])

    # set the data to be used by the plots
    for sorted_data, color in zip(sorted_datas, plot_colors):
        plt.plot(sorted_data, color)


    # show the plots
    plt.show()

def plot_recorded_shared_data():
    ''' read and plot the recorded shared data from shared_data file '''

    # read the data
    shared_data = []
    with open(config.SHARED_DATA_FILE, 'r') as shared_data_file_contents:
        for line in shared_data_file_contents:
            shared_data.append(json.loads(line))
    
    plot_arrs = []
    for key in shared_data[0]:
        plot_arrs.append([data[key] for data in shared_data])
    
    for arr in plot_arrs:
        plt.plot(arr)
    
    plt.show()

def is_int(str_num):
    try:
        int_num = int(str_num)
        float_num = float(str_num)
    except (TypeError, ValueError):
        return False
    else:
        return int_num == float_num

def plot_optimal_params():
    # get the optimal params stored in param_file.txt
    param_file = open(config.BEST_PARAM_FILE, 'r')
    
    is_header = True
    filterlengths  = []
    profits = []
    maxmin_ranges = []
    for line in param_file:
        if is_header:
            is_header = False
            continue
        data = line.strip().split(',')
        for i in range(len(data)):
            if is_int(data[i]):
                filterlengths.append(int(data[i]))
            else:
                if i == 0:
                    profits.append(float(data[i]))
                elif i == 2:
                    maxmin_ranges.append(float(data[i]))
    
    plot_data = [profits, filterlengths, maxmin_ranges]

    # plot out the data
    for data in plot_data:
        plt.plot(data)
    
    plt.show()

    # create a plot using the best parameters

if __name__ == '__main__':
    # plot_recorded_shared_data()
    plot_optimal_params()