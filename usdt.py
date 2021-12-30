from binance import Client
import csv, utils
import numpy as np
import pandas as pd
import os
import time

class USDT():
    def __init__(self, client):
        self.client = client
        self.name = "EURUSDT"
        self.file = "EURUSDT/EURUSDT.csv"
        self.config_file = "EURUSDT/EURUSDT_config.csv"
        self.data = pd.DataFrame()
        self.fake_money = 0
        self.money = 0
        self.read_config()

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

    async def remove_fake(self, value):
        if (self.fake_money < value):
            return False
        self.fake_money -= value
        await self.write_config()
        return True

    async def add_fake(self, value):
        self.fake_money += value
        await self.write_config()

    async def update_values(self):
        from_date = 0
        exist = False
        if (os.path.isdir(self.name) == False):
            os.mkdir(self.name)
        if (os.path.isfile(self.file)):
            exist = True
            f_data = pd.read_csv(self.file)
            last_time = int(round(f_data.iloc[-1]['time']))
            actual_time = int(round(time.time() * 1000))
            if (utils.add_time(last_time, 1, 0, 0) < actual_time):
                from_date = last_time
            else:
                return False
        else:
            from_date = "1 Nov, 2021"
   
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