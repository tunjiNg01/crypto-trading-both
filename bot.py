import talib
import websocket, json
import ssl
import numpy
import talib

# ssl certificate disable
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
closes = []
def on_open(ws):
    print("Opened connection ")

def on_message(ws, message):
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    is_candle_close = json_message['k']['x']
    if is_candle_close:
        candle = json_message['k']
        closes.append(float(candle['c']))
        print(f"Close: {candle['c']}, High: {candle['h']}, Low: {candle['l']}, Open: {candle['o']}, Volume: {candle['v']}")
        
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print(f"RSI: {rsi}")
      
def on_close(ws, close_status_code, close_msg):
    print(f"Closed connection {close_msg} - Status: {close_status_code}")
websocket.enableTrace(True)
ws = websocket.WebSocketApp(SOCKET, on_open=on_open,on_close=on_close, on_message=on_message,  )
ws.run_forever(sslopt={"context": ssl_context})