import json
import requests
import sqlite3
import HismoduleSQL
import logging
import time
import Datamodule 
import fetcher
import telegramclient
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
running = True
#debug = True

def main(interval,debug):
    global variable
    variable = 1
    fetcher.getlastpage()

    while running:
        time.sleep(interval)
        
        def check():
            global variable
            fetcher.getdata(variable)
            datafetch = fetcher.datavalue 
            #logging.info("variable=")
            #logging.info(variable)
            variable = variable + 1
            
            for loadsql in datafetch:
            
                try:
                    time.sleep(0)
                    keyretrieve = loadsql["publicKey"]
                    activestatus = loadsql["active"]
                    truststatus = loadsql["countTrust"]
                    if debug:
                        logging.info("key is send to module")
                    if HismoduleSQL.checkifpresent(keyretrieve,debug) == True:
                        if debug:
                            logging.info("Key already in db")
                            logging.info("Trying if node value is changed")
                        HismoduleSQL.checkifrunning(keyretrieve,debug)
                        HismoduleSQL.checktrust(keyretrieve,debug)
                        try:
                            if activestatus > HismoduleSQL.runningvalue:
                                HismoduleSQL.singlewrite(loadsql)
                                #telegramclient.dev()
                                if debug:
                                    logging.info("Active status changed trying to write data")

                            if activestatus < HismoduleSQL.runningvalue:
                                HismoduleSQL.singlewrite(loadsql)
                                #telegramclient.dev() 
                                if debug:
                                    logging.info("Active status changed trying to write data")  
                        
                            if int(truststatus) != int(HismoduleSQL.trustvalue):
                                HismoduleSQL.singlewrite(loadsql) 
                                #telegramclient.dev()  
                                if debug:
                                    logging.info("Trust amount increased trying to write data") 
                                 
                            else:
                                if debug:
                                    logging.info("nothing changed")  
                        except Exception as E:
                            logging.info('Error : {}'.format(E))     
               


                    if HismoduleSQL.checkifpresent(keyretrieve,debug) == False:
                        if debug:
                            logging.info("Key is going to be stored in db")    
                        HismoduleSQL.singlewrite(loadsql)
                        time.sleep(0)
        
                except Exception as E:
                    logging.info('Error : {}'.format(E)) 
        if variable < fetcher.lastpage1:
            if debug:
                logging.info("Going to next page")
            check()
            
        if variable == fetcher.lastpage1:
            if debug:
                logging.info("reached max page Starting at page 1")
            time.sleep(2)   
            check() 
            variable = 1        
        if variable > fetcher.lastpage1:
            if debug:
                logging.info("Error")
#main(1,True)

