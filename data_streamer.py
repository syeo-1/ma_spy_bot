import websocket, json
import config
import ast
from collections import deque
from datetime import datetime
import actions
import strategy

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
    global prod_bot
    processed_msg = json.loads(msg)
    if processed_msg['stream'] == f'T.{config.STOCK_NAME}':
        print(processed_msg['data']['p'])
        prod_bot.process_security(processed_msg['data']['p'])
        

def record_data(ws, msg):
    # convert message from string to dictionary
    dict_msg = ast.literal_eval(msg)
    if dict_msg["stream"] == f"T.{config.STOCK_NAME}":
        trade_file.write(msg+'\n')
    elif dict_msg["stream"] == f"Q.{config.STOCK_NAME}":
        quote_file.write(msg+'\n')

def on_close(ws):
    print("===connection closed===")
    trade_file.close()
    quote_file.close()

prod_bot = None

def initiliaze_stream(runtype, optimal_filterlength, optimal_maxmin_range):

    global prod_bot

    if runtype == 'recording':
        ws = websocket.WebSocketApp(socket, on_open=authenticate_connection, on_message=record_data, on_close=on_close)
        ws.run_forever()
    elif runtype == 'production':
        prod_bot = strategy.MovingAvgStrat(optimal_filterlength, optimal_maxmin_range)
        ws = websocket.WebSocketApp(socket, on_open=authenticate_connection, on_message=stream_data, on_close=on_close)
        ws.run_forever()


if __name__ == "__main__":
    initiliaze_stream('recording', 300, 0.001)