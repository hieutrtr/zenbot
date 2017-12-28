from coinmarketcap import Market
import os,sys
import json
import subprocess
import time
import re

# proc = subprocess.Popen(["./zenbot.sh","list-selectors", "|", "grep", "bittrex"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, err = proc.communicate(b"input data that is passed to subprocess' stdin")
# results = output.split('\n')
coinmarketcap = Market()
coins = coinmarketcap.ticker(limit=50)
# print(coins)
# for coin in coins:
#     print(coin.get("symbol",None))
strategies = ["macd","trendline","neural","forex_analytics"]
workers = {"apps": []}
exchange = sys.argv[1]
currency = sys.argv[2]
for coin in coins[1:]:
    if coin.get("symbol", None):
        selector = '{}.{}-{}'.format(exchange,coin["symbol"],currency)
        for strategy in strategies:
            workers['apps'].append({"name": selector+'.'+strategy, "script": "./zenbot.sh", "args": "trade {} --paper --strategy {} --conf ./beta.js".format(selector,strategy)})
    # if len(res) >= 3 and sys.argv[1] in res[2] and '-'+sys.argv[2] in res[2]:
    #     workers['apps'].append({"name": res[2], "script": "./zenbot.sh", "args": "trade {} --paper --strategy {} --conf ./beta.js".format(res[2],sys.argv[3])})

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
