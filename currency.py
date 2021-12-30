import streamlit as st
from binance import AsyncClient, BinanceSocketManager
import csv, utils, os, time, threading, asyncio
import numpy as np
import pandas as pd
from usdt import *

class Currency():
    def __init__(self, name, client, usdt):
        self.client = client
        self.name = name+"USDT"
        self.file = self.name+"/"+self.name+".csv"
        self.config_file = self.name+"/"+self.name+"_config.csv"
        self.logs_file = "logs.txt"
        self.data = pd.DataFrame()
        self.fake_money = 0
        self.money = 0
        self.read_config()
        self.usdt = usdt
        self.activated = True
        self.last_action_price_evolution = 0
        self.thread = threading.Thread(target=self.between_trade)
        self.purchases = []
        self.bm = BinanceSocketManager(self.client)

    def read_config(self):
        if (os.path.isfile(self.config_file)):
            d = pd.read_csv(self.config_file, 
                index_col='id', 
                header=0,
                names=['id', 'value'])
            self.fake_money = d['value']['fake_money']
            self.money = d['value']['money']

    async def write_config(self):
        if (os.path.isdir(self.name) == False):
            os.mkdir(self.name)
        d = [{'id': 'fake_money', 'value': self.fake_money}, 
             {'id': 'money',      'value': self.money}]

        df = pd.DataFrame(data=d)
        df.to_csv(self.config_file, index=False)

    async def buy_fake(self, value):
        data = pd.DataFrame(await self.client.get_ticker())
        to_rm =  float(data[data.symbol == self.name]['lastPrice']) * value
        if ((await self.usdt.remove_fake(to_rm)) == True):
            self.fake_money += value
            with open(self.logs_file, "a") as myfile:
                myfile.write("Bought %s %s for %s USDT" % (value, self.name, to_rm))
        else:
            st.error('Not enought USDT')
            with open(self.logs_file, "a") as myfile:
                myfile.write("Tried to buy %s %s for %s USDT but not anought money" % (value, self.name, to_rm))

    async def buy_fake_percent_usdt(self, percent):
        percent /= 100
        to_rm = self.usdt.fake_money * percent
        async with self.bm.ticker_socket():
            tmp_bsm = await self.bm.ticker_socket()
            print(tmp_bsm)
        exit()
        data = pd.DataFrame()
        value =  to_rm / float(data[data.symbol == self.name]['lastPrice'])
        if ((await self.usdt.remove_fake(to_rm)) == True):
            self.fake_money += value
            print("Bought %s %s for %s USDT" % (value, self.name, to_rm))
            with open(self.logs_file, "a") as myfile:
                myfile.write("Bought %s %s for %s USDT" % (value, self.name, to_rm))
        else:
            st.error('Not enought USDT')
            with open(self.logs_file, "a") as myfile:
                myfile.write("Tried to buy %s %s for %s USDT but not anought money" % (value, self.name, to_rm))

    async def sell_fake(self, percent):
        percent /= 100
        data = pd.DataFrame(await self.client.get_ticker())
        current_price =  float(data[data.symbol == self.name]['lastPrice'])
        add_usdt = (self.fake_money * percent) * current_price
        save_to_print = self.fake_money * percent
        self.fake_money *= (1-percent)
        await self.usdt.add_fake(add_usdt)
        with open(self.logs_file, "a") as myfile:
                myfile.write("Sold %s %s and got %s USDT" % (save_to_print, self.name, add_usdt))

    async def update_values(self):
        from_date = 0
        exist = False
        if (os.path.isdir(self.name) == False):
            os.mkdir(self.name)
        if (os.path.isfile(self.file)):
            exist = True

            # self.data = pd.read_csv(self.file)
            self.data = pd.read_csv(self.file, 
                index_col='time', 
                header=0,
                names=['time', 'values'])

            last_time = int(round(self.data.iloc[-1].name))
            actual_time = int(round(time.time() * 1000))
            if (utils.add_time(last_time, 1, 0, 0) < actual_time):
                from_date = last_time
            else:
                return False
        else:
            from_date = "1 Nov, 2021"
   
        # utils.save_graph(self.file)
        data = await self.client.get_historical_klines(self.name, Client.KLINE_INTERVAL_15MINUTE, from_date)
        t_v = utils.average_graph(data)
        p_t_v = pd.DataFrame(t_v.items(), columns=['time', 'values'])
        if (exist):
            self.data.append(p_t_v)
            p_t_v.to_csv(self.file, mode='a', index=False, header=False)
        else:
            self.data = p_t_v
            p_t_v.to_csv(self.file, index=False)
        

            
        return True

    async def close(self):
        await self.write_config()

    # -1 for from day is the actual day
    # other numbers for the from day is counting from today in reverse
    def pourcent_evo(self, from_day, to_day):
        first = float(self.data.iloc[-(4*24*int(to_day))])
        if from_day == -1:
            total = from_day
        else:
            total = -(4*24*int(from_day))

        last = float(self.data.iloc[total])
        pourcent = ((last - first) / first) * 100
        # print("%s -> %s = %s " % (first, last, pourcent))
        return pourcent

    async def trade(self):
        while True:
            # if self.name == "ADAUSDT":
            print("%s 1 last days evolution = %s" % (self.name, self.pourcent_evo(-1, 1)))
            # print("%s 5 last days evolution = %s" % (self.name, self.pourcent_evo(1, 5)))
            # if self.pourcent_evo(-1, 1) > 1.0 and self.pourcent_evo(1, 5) < 5.0:
            # print(self.purchases)
            if self.pourcent_evo(-1, 1) > 1.0 and not self.purchases:
                print("YEAHHHHHHHHHHHHH")
                actual_time = int(round(time.time() * 1000))
                before = self.fake_money
                a = await self.buy_fake_percent_usdt(50)
                after = self.fake_money

                self.purchases.append([actual_time, (after - before)])
                # self.purchases.append(actual_time)
            # print("I'm trading %s..." % self.name)
            time.sleep(3)

    def between_trade(self):
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        loop.run_until_complete(self.trade())
        loop.close()