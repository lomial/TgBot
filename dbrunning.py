import json
import requests
import sqlite3
import MainmoduleSQL
import logging
import time
import Datamodule
import fetcher
import telegramclient
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
running = True
debug = False

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
                    if debug:
                        logging.info("key is send to module")
                        #logging.info(MainmoduleSQL.checkifpresent)
                    if MainmoduleSQL.checkifpresent(keyretrieve,debug) == True:
                        if debug:
                            logging.info("Key stored in db")
               


                    if MainmoduleSQL.checkifpresent(keyretrieve,debug) == False:
                        if debug:
                            logging.info("Key is going to be stored in db")    
                        MainmoduleSQL.singlewrite(loadsql)
                        time.sleep(0)
        
                except Exception as E:
                    logging.info('Error : {}'.format(E)) 
        if variable < fetcher.lastpage1:
            logging.info("Going to next page")
            check()
            
        if variable == fetcher.lastpage1:
            logging.info("reached max page Starting at page 1")
            time.sleep(2)
            check() 
            variable = 1            
        if variable > fetcher.lastpage1:
            logging.info("test")


#main(1,True)
