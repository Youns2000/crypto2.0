import numpy as np
import pandas as pd
import streamlit as st
import config
import json, asyncio, csv
from binance import AsyncClient
from threading import Thread
import queue

SLEEPING_TIME = 3

if __name__ == "__main__":
    q = queue.Queue(maxsize=0)
    num_threads = 10

    for i in range(num_threads):
        worker = Thread(target=do_stuff, args=(q,))
        worker.setDaemon(True)
        worker.start()

    for x in range(100):
        q.put(x)


    q.join()