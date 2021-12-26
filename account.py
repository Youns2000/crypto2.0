from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager, AsyncClient
import pandas as pd
import csv, time, asyncio
import config, utils, os, usdt, currency
import streamlit as st

class Account(object):
    @classmethod
    async def create(cls):
        self = Account()
        self.client = await AsyncClient.create(config.API_KEY, config.API_SECRET)
        self.usdt_var = usdt.USDT(self.client)
        await self.usdt_var.update_values()
        self.currencies = []
        await self.check_currs()
        for c in self.currencies:
            await c.update_values()
        return self

    # check every file to add to the account every existing currs
    async def check_currs(self):
        dirs = os.listdir('./')
        for item in dirs:
            if (os.path.isdir(item) and item.endswith('USDT')):
                item = utils.remove_suffix(item, 'USDT')
                if item != "EUR":
                    await self.add_curr(item)

    # check if the curr exist with USDT in the binance api
    async def exist_curr(self, name):
        all_data = pd.DataFrame(await self.client.get_ticker())
        df = all_data[all_data['symbol'] == name + 'USDT']
        return not df.empty

    async def total(self):
        usdttotal = 0.00
        # gt = await asyncio.gather(self.client.get_all_tickers())
        gt = await self.client.get_all_tickers()
        all_data = pd.DataFrame(gt)
        usdttotal += self.usdt_var.fake_money
        for c in self.currencies:
            usdttotal += c.fake_money / float(all_data[all_data['symbol'] == c.name]['price'])

        return usdttotal / float(all_data[all_data['symbol'] == 'EURUSDT']['price'])

    # creating a currency
    # update the currency values (or create them if the curr wasn't never created)
    # append it to the currs tab of the account
    async def add_curr(self, name):
        curr = currency.Currency(name, self.client, self.usdt_var)
        await curr.update_values()
        self.currencies.append(curr)  

    # buy fake_money of the given curr for a given value
    def buy_curr(self, name, value):
        for c in self.currencies:
            if (c.name == (name + "USDT")):
                c.buy_fake(value)

    # sell a percent of the fake_money of a given curr
    def sell_curr(self, name, percent):
        for c in self.currencies:
            if (c.name == (name + "USDT")):
                c.sell_fake(percent)

    async def update_all_files(self):
        while True:
            for c in self.currencies:
                await c.update_values()
            await self.usdt_var.update_values()
            print("updating...")
            time.sleep(3)
    
    # write the data of each currs and the usdt and close the client connection (binance api)
    async def close(self):
        for c in self.currencies:
            await c.close()
        await self.usdt_var.close()
        await self.client.close_connection()