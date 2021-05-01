import websocket, json
import config
import ast
from collections import deque
from datetime import datetime

fresh_minute = False

socket = "wss://data.alpaca.markets/stream"

def authenticate_connection(ws):
    print("===connection opened===")
    authentication = {
        "action":"authenticate",
        "data": {
            "key_id": f"{config.ALPACA_API_KEY}",
            "secret_key": f"{config.ALPACA_SECRET_KEY}"
        }
    }

    return_value = ws.send(json.dumps(authentication))
    print(return_value)

    channel_data = {
        "action": "listen",
        "data": { 
            "streams": [f"T.{config.STOCK_NAME}", f"Q.{config.STOCK_NAME}"]
        }
    }
    return_value2 = ws.send(json.dumps(channel_data))
    print(return_value2)

trade_file = open("/Users/seanyeo/Desktop/studying resources/self-learning/alpaca_trading/ma_spy_bot/SPY_trade_data.txt", "a")
quote_file = open("/Users/seanyeo/Desktop/studying resources/self-learning/alpaca_trading/ma_spy_bot/SPY_quote_data.txt", "a")

def stream_data(ws, msg):
    # convert message from string to dictionary
    dict_msg = ast.literal_eval(msg)
    global fresh_minute
    # print(dict_msg)
    # only process stock ticker data
    if dict_msg["stream"] == f"T.{config.STOCK_NAME}":
        # print(dict_msg)
        trade_file.write(msg+'\n')
        # process(dict_msg)
    elif dict_msg["stream"] == f"Q.{config.STOCK_NAME}":
        quote_file.write(msg+'\n')

def on_close(ws):
    print("===connection closed===")
    trade_file.close()
    quote_file.close()

def initiliaze_stream():
    # make sure to build candlesticks only if the minute is new
    # while not fresh_minute:
    #     current_second = datetime.now().time().second
    #     if current_second == 0:
    #         break

    # begin streaming data
    ws = websocket.WebSocketApp(socket, on_open=authenticate_connection, on_message=stream_data, on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    # creator = Candlestick_creator()
    # trade_file.write('testing123')
    # quote_file.write('testing123')
    initiliaze_stream()