import os,sys
import json
import subprocess
import time
import re

proc = subprocess.Popen(["./zenbot.sh","list-selectors", "|", "grep", "bittrex"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = proc.communicate(b"input data that is passed to subprocess' stdin")
results = output.split('\n')
if "failed" in results:
    raise Exception("{} Generation Fail\n")
else:
    repls = ['\x1b','[36m','[39m','[90m','[32m']

    workers = {"apps": []}

    for res in results:
        for repl in repls:
            res = res.replace(repl,'')
        res = res.split(' ')
        if len(res) >= 3 and sys.argv[1] in res[2] and '-'+sys.argv[2] in res[2]:
            workers['apps'].append({"name": res[2], "script": "./zenbot.sh", "args": "trade {} --paper --strategy macd".format(res[2])})

print workers
with open("./workers/beta.json", "w") as workerFile:
    workerFile.write(json.dumps(workers,sort_keys=True,indent=4, separators=(',', ': ')))
    workerFile.close()
