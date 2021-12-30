from requests import *
import numpy as np
import pandas as pd
import config, account, currency, utils
import json, asyncio
import csv
from binance import Client
from datetime import datetime
import usdt
import os
import streamlit as st
import time
# from multiprocessing import Process, Queue
# import multiprocessing as mp
import threading

SLEEPING_TIME = 0.01

# def front_end(acc):
#     curr_names = []
#     for c in acc.currencies:
#         curr_names.append(c.name)

#     curr_names.append("Add Currency")

#     actual_curr = st.sidebar.radio(
#     "Select a crypto currency :",
#     (curr_names))

#     usdt_fake_total = st.sidebar.empty()
#     curr_money = st.empty()
#     curr_chart = st.empty()

#     with st.form("add"):
#         st.write("""
#         # Buy
#         """)
#         buy_val = st.text_input('Value')
#         buy = st.form_submit_button("BUY")
#         if buy:
#             acc.buy_curr(utils.remove_suffix(actual_curr, 'USDT'), float(buy_val))
#             acc.close()
#         st.write("""
#         # Sell
#         """)
#         sell_val = st.text_input('SellValue')
#         sell = st.form_submit_button("SELL")
#         if sell:
#             acc.sell_curr(utils.remove_suffix(actual_curr, 'USDT'), float(sell_val))
#             acc.close()  

#     usdt_fake_total.markdown("""
#     # USDT (*fake*) : %s
#     """ % acc.usdt_var.fake_money)

#     for c in acc.currencies:
#         if c.name == actual_curr:
#             curr_money.markdown("""
#             # %s : %s
#             """ % (c.name, c.fake_money))
#             curr_chart.line_chart(c.data)
                
#     if actual_curr == "Add Currency":
#         with st.container():
#             st.write("""
#             # Add Currency
#             """)
#             with st.form("add"):
#                 curr = st.text_input('Currency')
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     if acc.exist_curr(curr):
#                         acc.add_curr(curr)

#                         acc.close()
#                         st.write("Add", curr, "currency")
#                     else:
#                         st.error("Currency doesn't exist")


async def get_total(total, acc):
    while True:
        t = await acc.total()
        total.markdown("""
        # TOTAL : %s EUR""" % t)
        await asyncio.sleep(3)

# def get_info(tab, acc, df):
#     tab.markdown(df)


async def set_acc():
    # loading account data :
    # - creating client
    # - creating USDT_curr :
    #           - reading the EURUSDT config file
    # - update usdt data
    # - add every curr that have a conf file
    acc = await account.Account.create()
    return acc


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()

    # data_load_state = st.text('Loading data...')
    # loop.run_until_complete()
    # asyncio.run(set_acc(set_acc()))
    # loop.close()
    asyncio.run(set_acc())
    # data_load_state.text('Loading data...done!')

    # # dic = {}
    # # dic = {'name': [], 'money': []}
    # # dic['name'].append('USDT')
    # # dic['money'].append(acc.usdt_var.fake_money)
    # # for c in acc.currencies:
    # #     dic['name'].append(c.name)
    # #     dic['money'].append(c.fake_money)
    # # df = pd.DataFrame(dic)

    # total = st.empty()
    # tab = st.empty()

    # asyncio.run(get_total(total, acc))
    # loop = asyncio.get_event_loop()
    # set_acc()
    # try:
    #     asyncio.ensure_future(get_total(total, acc))
    #     # asyncio.ensure_future(secondWorker())
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     print("Closing Loop")
    #     acc.close()
    #     loop.close()
    # loop = asyncio.new_event_loop()