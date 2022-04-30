import json
import time
import logging
import requests
import config
import fetcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
onlinecount = 0

def connect(debug,running,interval):
    global onlinecount
    global offlinecount
    global lastpage1
    global checkcount
    checkcount = fetcher.onlinecount
    running = running
    debug = debug
    interval = interval
    while running:
        time.sleep(interval)

        try:
            #logging.info("Fetching data")
            resp = requests.get('{}/Api/GetNodesData?page=1&limit=10'.format(config.networkurl))
            jsonStr = resp.text
            json_data = json.loads(jsonStr)
            onlinecount = json_data["onlineCount"]
            offlinecount = json_data["offlineCount"]
            lastpage1 = json_data["lastPage"]
            logging.info("Lastpageid is fetched")
            logging.info("Lastpageid = {}".format(lastpage1))
            logging.info ("Updated url count to : %i", onlinecount)
            if debug:
                logging.info ('DEBUG : Value as onlinecount %i', onlinecount)


        except Exception as E:
            logging.info('Error : {}'.format(E)) 
            
    return onlinecount

def getlastpage():
    global lastpage1
    try:
        logging.info("Fetching lastpageid")
        resp = requests.get('{}/Api/GetNodesData?page=1&limit=10'.format(config.networkurl))
        jsonStr = resp.text
        json_data = json.loads(jsonStr)
        lastpage1 = json_data["lastPage"]
        logging.info("Lastpageid is fetched")
        logging.info("Lastpageid = {}".format(lastpage1))

    except Exception as E:
        logging.info('Error : {}'.format(E))    

def getdata(pagenumber):
    global datavalue
    try:
        logging.info("Fetching all nodes")
        resp = requests.get('{}/Api/GetNodesData?page={}&limit=10'.format(config.networkurl,pagenumber))
        jsonStr = resp.text
        json_data = json.loads(jsonStr)
        datavalue = json_data["nodes"]
        logging.info("Node page is fetched")
        

    except Exception as E:
        logging.info('Error : {}'.format(E))    