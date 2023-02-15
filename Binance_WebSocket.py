import websocket
import json

from coin import Coin

class WebSocket():
    def __init__(self, coin:Coin):
      self.coin = coin
      self.connected = False

    def on_message(self, ws, message):
        data = json.loads(message)
        date = int(data["data"]["E"])
        symbol = data["data"]["s"].lower()
        last = float(data["data"]["p"])
        self.coin.trade(symbol, last, date)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        self.connected = False
        print("### closed ###")

    def on_open(self, ws):
        self.connected = True
        print("### connected ###")

    def websocket_run(self):
        ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams="+self.coin.symbol_btc+"@aggTrade/"+self.coin.symbol_eth+"@aggTrade",
          on_message = self.on_message,
          on_error = self.on_error,
          on_close = self.on_close)

        ws.on_open = self.on_open
        ws.run_forever()