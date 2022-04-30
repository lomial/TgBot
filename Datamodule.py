import time
import json
import requests
import logging
import config
maxpage = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
datalist = list()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
returndata = datalist

def fetch():
    global checkpage
    global returndata

    pagenumber = 1
    checkpage = 1
    for test in maxpage:
        try:
            
            logging.info("Retrieving pages")
            resp = requests.get('{}/Api/GetNodesData?page={}&limit=10'.format(config.networkurl,test))
            jsonStr = resp.text
            json_data = json.loads(jsonStr)
            storedata = json_data["nodes"]
            logging.info("Data retrieved for page{}".format(test))
            pagenumber + 1
            time.sleep(0.1)
            returndata = datalist
            print (storedata[0])

        except IndexError:
            logging.info("Last page reached")    
                

        except Exception as E:
            logging.info('Error : {}'.format(E))

def fetch2():
    global checkpage
    global datalist
    pagenumber = 1
    checkpage = 1
    for test in 8:
        
        try:

            if checkpage < maxpage:
                logging.info("Retrieving pages")
                resp = requests.get('{}/Api/GetNodesData?page={}&limit=10'.format(config.networkurl,pagenumber))
                jsonStr = resp.text
                json_data = json.loads(jsonStr)
                storedata = json_data["nodes"]
                datalist.append(storedata)
                checkpage = checkpage + 1
                pagenumber = pagenumber + 1
                logging.info("One page stored in variable")
                time.sleep(0.1)
            if checkpage == maxpage:
                print (datalist[0])
                logging.info("Data retrieved from monitor")
                break

        except Exception as E:
            logging.info('Error : {}'.format(E))



          