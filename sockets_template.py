from binance import AsyncClient, BinanceSocketManager
import streamlit as st
import asyncio, json
import config
import pandas as pd

# async def kline_listener(client):
#     bm = BinanceSocketManager(client)
#     async with bm.kline_socket(symbol='BTCUSDT') as stream:
#         while True:
#             res = await stream.recv()
#             # df = pd.DataFrame(res)
#             print(res)

# async def kline_listener(client):
#     bm = BinanceSocketManager(client)
#     symbol = 'BNBBTC'
#     res_count = 0
#     async with bm.kline_socket(symbol=symbol, interval='1m') as stream:
#         while True:
#             res = await stream.recv()
#             res_count += 1
#             print(res)
#             if res_count == 5:
#                 res_count = 0
#                 order_book = await client.get_order_book(symbol=symbol)
#                 print(order_book)

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)


async def kline_listener(client):
    bm = BinanceSocketManager(client)
    symbol = 'BTCUSDT'
#     res_count = 0
#     async with bm.symbol_ticker_socket(symbol=symbol) as stream:
#         # while True:
#         res = await stream.recv()
#         res_count += 1
#         # df = pd.DataFrame(res)
#         # print(df)
#         print(res)
#         # if res_count == 5:
#         #     res_count = 0
#         #     loop.call_soon(asyncio.create_task, order_book(client, symbol))
    ts = bm.trade_socket(symbol=symbol)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            # j_res = json.loads(res)
            # print(j_res)
            # print(res["s"])
            print(res["p"])



async def main():
    client = await AsyncClient.create(config.API_KEY, config.API_SECRET)
    await kline_listener(client)
    await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
