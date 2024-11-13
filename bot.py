import websocket, json, pprint
import ssl
# ssl certificate disable
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
def on_open(ws):
    print("Opened connection ")

def on_message(ws, message):
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    is_candle_close = json_message['k']['x']
    if is_candle_close:
        candle = json_message['k']
        print(f"Close: {candle['c']}, High: {candle['h']}, Low: {candle['l']}, Open: {candle['o']}, Volume: {candle['v']}")
    
def on_close(ws, close_status_code, close_msg):
    print(f"Closed connection {close_msg} - Status: {close_status_code}")
websocket.enableTrace(True)
ws = websocket.WebSocketApp(SOCKET, on_open=on_open,on_close=on_close, on_message=on_message,  )
ws.run_forever(sslopt={"context": ssl_context})