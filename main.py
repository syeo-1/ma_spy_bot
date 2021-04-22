import processing
import sys

def run_backtest_bot():
    pass

def run_prod_bot():
    pass

def main():
    run_type = sys.argv[1]
    if run_type == 'test':
        print('backtesting strat')
    elif run_type == 'prod':
        print('going live!!!')
    else:
        print('invalid run_type given. Please give either test or prod')
        exit(1)

if __name__ == '__main__':
    main()
