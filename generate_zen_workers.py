from coinmarketcap import Market
import os,sys
import json
import subprocess
import time
import re

coinmarketcap = Market()
coins = coinmarketcap.ticker(limit=200)

strategy_conf = {
    "trendline": {
        "period": "5m"
    },
    "rsi": {
        "period": "1h"
    },
    "trend_ema": {
        "period": "15m"
    }
}

strategies = sys.argv[4].split(',') if sys.argv[4] else ["macd","trendline","neural","forex_analytics"]
workers = {"apps": []}
exchange = sys.argv[1]
currency = sys.argv[2]
for coin in coins[1:]:
    if coin.get("symbol", None):
        selector = '{}.{}-{}'.format(exchange,coin["symbol"],currency)
        for strategy in strategies:
            conf = strategy_conf.get(strategy,{})
            ops = "--period {}".format(conf["period"]) if(conf.get("period",None) != None) else ""
            workers['apps'].append({"autorestart": False ,"name": selector+'.'+strategy, "script": "./zenbot.sh", "args": "trade {} --paper --strategy {} {} --conf ./beta.js".format(selector,strategy,ops)})

def chunks(l, n):
    res = []
    for i in range(0, len(l), n):
        res.append(l[i:i + n])
    return res
chunk_size = int(sys.argv[3])
print "Number of workers : " + str(len(workers["apps"]))
for k,chunk in enumerate(chunks(workers["apps"], chunk_size)):
    workers["apps"] = chunk
    with open('./workers/beta_{}.json'.format(k), "w") as workerFile:
        workerFile.write(json.dumps(workers,sort_keys=True,indent=4, separators=(',', ': ')))
        workerFile.close()
