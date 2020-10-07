import pandas as pd
import math
import os.path
import time
from bitmex import bitmex
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm #(Optional, used for progress-bars)
from setting import API_KEY, API_SECRET

bitmex_client = bitmex(test=False, api_key=API_KEY, api_secret=API_SECRET)

symbol = 'XBT'
count = 500

def minutes_of_new_data(symbol, data):
    if len(data) > 0:
        old = parser.parse(data['timestamp'].iloc[-1])
    elif symbol == 'XBT':
        old = bitmex_client.Funding.Funding_get(symbol=symbol, reverse=False, count=count).result()[0][22]['timestamp']
    if symbol == 'XBT':
        new = bitmex_client.Funding.Funding_get(symbol=symbol, reverse=True, count=count).result()[0][0]['timestamp']
    return old, new

def get_funding_rate(symbol):
    filename = '%s-funding-rate.csv' % (symbol)
    data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data('XBT', data_df)
    delta_period = (newest_point - oldest_point).total_seconds()/28800
    available_data = math.ceil(delta_period)
    rounds = math.ceil(available_data / 500)
    if rounds > 0:
        print('Downloading funding rate')
        for round_num in tqdm(range(rounds)):
            time.sleep(1)
            new_time = (oldest_point + timedelta(hours = round_num * 500 * 8))
            data = bitmex_client.Funding.Funding_get(symbol=symbol, count=count, startTime = new_time).result()[0]
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
    data_df.set_index('timestamp', inplace=True)
    data_df.to_csv(filename)
    return data_df

get_funding_rate('XBT')