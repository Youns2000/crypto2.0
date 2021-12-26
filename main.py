from binance import AsyncClient, BinanceSocketManager
import streamlit as st
import asyncio
import config
import pandas as pd

# async def order_book(client, symbol):
#     order_book = await client.get_order_book(symbol=symbol)
#     print(order_book)


# async def kline_listener(client):
#     bm = BinanceSocketManager(client)
#     symbol = 'BNBBTC'
#     res_count = 0
#     async with bm.kline_socket(symbol=symbol) as stream:
#         while True:
#             res = await stream.recv()
#             res_count += 1
#             print(res)
#             if res_count == 5:
#                 res_count = 0
#                 loop.call_soon(asyncio.create_task, order_book(client, symbol))

async def funct():
    client = await AsyncClient.create(config.API_KEY, config.API_SECRET)
    res = await asyncio.gather(
        client.get_exchange_info(),
        client.get_all_tickers()
    )
    # print(client)
    print(res[0][0])


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    loop.run_until_complete(funct())
    loop.close()
