'''use this file for creating plots with matplotlib'''
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    a = [{
        'a':1,
        'b':2,
        'c':3
    },
    {
        'a':3,
        'b':6,
        'c':8
    }]
    plot_dict_list(a, 'a')