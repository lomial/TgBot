import logging
import time
import json
import requests
import telegramclient
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

lastblock = 0

def blockchain(debug,running,interval):
    global lastblock
    global lastblocktx
    running = running
    debug = debug
    interval = interval
    while running:
        time.sleep(interval)

        try:
            resp= requests.get('http://194.87.103.77:63500/Network/api/IndexData?')
            jsonStr = resp.text
            json_data = json.loads(jsonStr)
            lastblockdata = json_data["lastBlockData"]
            lastblock = lastblockdata["lastBlock"]
            lastblocktx = lastblockdata["lastBlockTxCount"]

            
            #logging.info ("Updated last block to : %d", lastblock)
            if debug:
                logging.info ('DEBUG : Value as Lastblock %d', lastblock)

        except Exception:
            logging.error ("Major notifier error")
            telegramclient.blockchainerror()
            raise    
         
    