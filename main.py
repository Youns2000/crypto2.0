import numpy as np
import pandas as pd
import config, account, currency, utils, usdt
import json, asyncio, csv
from binance import Client
import streamlit as st
import threading
import traceback
# import ptvsd
# from thread_safe_st import ThreadSafeSt

# thread_safe_st = ThreadSafeSt()

SLEEPING_TIME = 3

async def print_infos(total, acc, df, tab, logs):
    while True:
        t = await acc.total()
        total.markdown("""
        # TOTAL : %s EUR""" % t)
        tab.table(df)
        str = ""
        with open('logs.txt', 'r') as f:
            lines = f.readlines()
            for l in lines:
                str += l
                str += '\n'
            logs.markdown("""
            # LOGS : \n %s """ % str)
        a = await asyncio.sleep(SLEEPING_TIME)

def between_update_files(acc):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(acc.update_all_files())
    loop.close()

async def set_acc():
    # loading account data :
    # - creating client
    # - creating USDT_curr :
    #           - reading the EURUSDT config file
    # - update usdt data
    # - add every curr that have a conf file
    acc = await account.Account.create()
    return acc

async def close_acc(acc):
    await acc.close()

async def add_curr(curr, acc):
    if await acc.exist_curr(curr):
        await acc.add_curr(curr)
        st.write("Added", curr, "currency")
    else:
        st.error("Currency doesn't exist")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    ######### SETTING ACCOUNT ############

    acc = loop.run_until_complete(set_acc())
    print("Account Created !")

    ######### SETTING STREAMLIT DISPLAY ZONES ############

    total = st.empty()
    tab = st.empty()
    logs = st.empty()
    print("Streamlit empty display zones total and tab created !")
    
    ######### ADD CURRENCY ############
    with st.form("add"):
        st.write("""
        # Add Currency
        """)
        curr = st.text_input('Currency')
        submitted = st.form_submit_button("Submit")
        if submitted:
            loop.run_until_complete(add_curr(curr, acc))

    print("Add currency form created !")

    ######### INIT CURRENCIES ############
    dic = {'name': [], 'activated': [], 'money': []}
    dic['name'].append('USDT')
    dic['activated'].append(False)
    dic['money'].append(acc.usdt_var.fake_money)
    for c in acc.currencies:
        dic['name'].append(utils.remove_suffix(c.name, 'USDT'))
        dic['activated'].append(c.activated)
        dic['money'].append(c.fake_money)
    df = pd.DataFrame(dic)

    st.success("Currencies initialized :")
    print("Currencies initialized :")
    print(df)

    ######### STARTING THREADS ############
    update_files_thread = threading.Thread(target=between_update_files, args=(acc,))
    st.success("Update files thread created !")
    print("Update files thread created !")
    # print_info_thread = threading.Thread(target=between_print_infos, args=(total, acc, df, tab,))
    # print("Print info thread created !")

    for c in acc.currencies:
        if c.activated:
            c.thread.start()
            st.success("%s thread started !" % c.name)
            print("%s thread started !" % c.name)

    try:
        update_files_thread.start()
    except Exception:
        traceback.print_exc()
    st.success("Update files thread started !")
    print("Update files thread started !")

    
    # try:
    #     print_info_thread.start()
    # except Exception:
    #     traceback.print_exc()
    # print("Print info thread started !")

    loop.run_until_complete(print_infos(total, acc, df, tab, logs))

    ######### ENDING THREADS ############
    for c in acc.currencies:
        if c.activated:
            c.thread.join()
            st.success("%s thread killed !" % c.name)
            print("%s thread killed !" % c.name)

    update_files_thread.join()
    st.success("Update files thread killed !" % c.name)
    print("Update files thread killed !" % c.name)
    # print_info_thread.join()
    # print("Print info thread killed !" % c.name)

    ######### CLOSE EVERYTHING #############

    loop.run_until_complete(close_acc(acc))
    loop.close()