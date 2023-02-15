from bar import Bar
from datetime import datetime
import os


class Coin():

    def __init__(self, symbol_btc: str, symbol_eth: str, percentage_difference):
        self.percentage_difference = percentage_difference
        self.percentage_difference_last = 0
        self.percentage_difference_max = 0
        self.alerts_list = []
        self.date = 0
        self.symbol_btc = symbol_btc
        self.symbol_eth = symbol_eth
        self.bars_btc:list[Bar]  = []
        self.bars_eth:list[Bar]  = []
        self.last_btc = 0
        self.last_eth = 0
        self.percent_btc = 0
        self.percent_eth = 0
        self.start_btc = False
        self.start_eth = False
        self.alerts_f = True

    def add_bar_all(self):
        if self.start_btc and self.start_eth:
            if len(self.bars_btc) > 59:
                self.bars_btc.pop(0)
                self.bars_eth.pop(0)
            self.bars_btc.append(Bar(self.bars_btc[len(self.bars_btc) - 1].close))
            self.bars_eth.append(Bar(self.bars_eth[len(self.bars_eth) - 1].close))

    def add_bar_btc(self, symbol, last):
        if self.start_btc == False and  self.last_btc != 0:
            if symbol == self.symbol_btc:
                self.start_btc = True
                self.bars_btc.append(Bar(last))

    def add_bar_eth(self, symbol, last):
        if self.start_eth == False and self.last_eth != 0:
            if symbol == self.symbol_eth:
                self.start_eth = True
                self.bars_eth.append(Bar(last))

    def trade(self,  symbol, last, date):
        self.date = datetime.fromtimestamp(date/1000)

        self.add_bar_btc(symbol, last)
        self.add_bar_eth(symbol, last)

        if symbol == self.symbol_btc:
            self.last_btc =  last
            if self.start_btc:
                 self.bars_btc[len(self.bars_btc) - 1].sort(last)
        if symbol == self.symbol_eth:
            self.last_eth = last
            if self.start_eth:
                self.bars_eth[len(self.bars_eth) - 1].sort(last)

        self.percent_calculation_btc()
        self.percent_calculation_eth()
        if len(self.bars_btc) > 2:
             self.alerts()
        # os.system('cls||clear')
        # print(self.bars_btc[len(self.bars_btc) - 1])
        # print(self.bars_eth[len(self.bars_eth) - 1])

    def percent_calculation_btc(self):
        max = 0
        min = 1000000

        for b in self.bars_btc:

            if max < b.high:
                max = b.high

            if min > b.low:
                min = b.low

        if max - self.last_btc >= self.last_btc - min:
            if self.last_btc - max != 0:
                 self.percent_btc = (self.last_btc - max) / (self.last_btc / 100)
        else:
            if self.last_btc - min != 0:
                self.percent_btc = (self.last_btc - min) / (self.last_btc / 100)

    def percent_calculation_eth(self):
        max = 0
        min = 1000000

        for b in self.bars_eth:
            if max < b.high:
                max = b.high
            if min > b.low:
                min = b.low

        if max - self.last_eth >= self.last_eth - min:
            if self.last_eth - max != 0:
                self.percent_eth = (self.last_eth - max) / (self.last_eth / 100)

        else:
            if self.last_eth - min != 0:
                 self.percent_eth = (self.last_eth - min) / (self.last_eth / 100)

    def  alerts(self):

        self.percentage_difference_last = abs(self.percent_btc - self.percent_eth)

        if self.percentage_difference_max < self.percentage_difference_last:
             self.percentage_difference_max = self.percentage_difference_last

        if self.alerts_f and abs(self.percent_btc) < 0.2  and self.percentage_difference_last > self.percentage_difference:
            print(f"{self.date} alerts: percentage difference >  {abs(self.percent_btc - self.percent_eth)}")
            self.alerts_list.append(f"{self.date} percentage difference > {abs(self.percent_btc - self.percent_eth)}")
            self.alerts_f = False

        if not self.alerts_f and self.percentage_difference_last < 0.1:
            print('alerts: percentage difference < ', abs(self.percent_btc - self.percent_eth))
            self.alerts_f = True