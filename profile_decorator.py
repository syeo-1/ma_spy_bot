import cProfile, pstats, io

def profiler(func):
    '''A decorator that uses cProfile to profile a function'''

    def info_retriever(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        info = func(*args, **kwargs)
        profile.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
        ps.print_stats()
        # print(s.getvalue())
        with open('time_test.txt', 'w+') as output:
            output.write(s.getvalue())
        return info
    
    return info_retriever