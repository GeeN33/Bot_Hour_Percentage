from datetime import datetime

from Binance_WebSocket import WebSocket
import threading

from coin import Coin
import tele_bot

symbol_btc = 'btcusdt'
symbol_eth = 'ethusdt'
percentage_difference = 1

coin = Coin(symbol_btc, symbol_eth, percentage_difference)

socket = WebSocket(coin)

def f():
  threading.Timer(60.0, f).start()
  if socket.connected:
      coin.add_bar_all()
      # print('=' * 10)
      # print(coin.date)
      # print(coin.percent_btc)
      # print(coin.percent_eth)
      # print('percentage_difference: ', coin.percentage_difference_last)
      # print('percentage_difference_max: ', coin.percentage_difference_max)
      # print('count bar: ',len(coin.bars_btc))

def f2():
  threading.Timer(5.0, f2).start()
  if socket.connected:
      tele_bot.runbot(coin)

if __name__ == '__main__':
    print(datetime.fromtimestamp(1676483943492/1000))


    f()
    f2()
    t1 = threading.Thread(target=socket.websocket_run, daemon=True)
    t1.start()
    t1.join()




