# Historical Bitmex Funding Rate

Download historical data of bitmex funding rate.

1. Input api_key and api_secret into setting.py file. (UPDATE: this also works without using api_key and api_secret, you can use empty string.)
2. By default, running main.py will generate new "XBT-funding-rate.csv"
3. To generate another instrument, modify symbol if needed.

Note : It starts at 2016-06-04 20:00:00 because 22 rows earlier are only have daily funding rate(not 3 times per day every 8 hours).
