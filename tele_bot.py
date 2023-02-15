import json
import os
import time
from dotenv import load_dotenv
import requests
from coin import Coin


load_dotenv()
TOKEN = os.environ.get('TOKEN')

URL = f'https://api.telegram.org/bot{TOKEN}/'


HELP_COMMAND = """
список команд 
/alerts - чтоб посмотреть список alerts 
/last - чтоб посмотреть last price
/diff - чтоб посмотреть percentage_difference
"""

class Message():
    def __init__(self, data):
        self.date = data['message']['date']
        self.update_id = int(data['update_id'])
        self.chat_id = int(data['message']['chat']['id'])
        self.username = data['message']['chat']['username']
        self.text = data['message']['text']

    def __str__(self):
        return  self.text

message_list = []

def requests_tg(curl, metod):
  r =  requests.get(curl + metod).json()
  return r

def send_message(chat_id, text):
    url = URL+'sendMessage'
    answer = {'chat_id' : chat_id, 'text': text}
    r = requests.post(url,json=answer)

def parsing(data, coin:Coin):
    max = 0
    for m in message_list:
        if m.update_id > max:
            max = m.update_id
    message_list_temp = []

    for i in data['result']:
        message_list_temp.append(Message(i))

    for m in message_list_temp:
        if m.update_id > max:
            message_list.append(m)
            if m.text == '/start':
                send_message(m.chat_id, HELP_COMMAND)
            elif m.text == '/alerts':
                print("tele bot alerts")
                if len(coin.alerts_list):
                    strrez = 'список alerts:\n'
                    for g in coin.alerts_list:
                        strrez = strrez + g + '\n'
                    send_message(m.chat_id, strrez)
                else:
                    send_message(m.chat_id, "пока ничего нет")
            elif m.text == '/last':
                strrez = f'BTC last price: {coin.last_btc}\n'
                strrez += f'ETH last price: {coin.last_eth}\n'
                send_message(m.chat_id, strrez)
            elif m.text == '/diff':
                strrez = f'percentage_difference: {coin.percentage_difference_last}\n'
                strrez += f'percentage_difference_max: {coin.percentage_difference_max}\n'
                send_message(m.chat_id, strrez)


def runbot(coin:Coin):
    r = requests_tg(URL, 'getUpdates?timeout=30')
    try:
        if r['ok']:
           parsing(r,coin)
           time.sleep(5)
        else:
           time.sleep(30)

    except Exception:
         time.sleep(60)