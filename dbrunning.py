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

def main(interval,debu):
    global variable
    variable = 1
    fetcher.getlastpage()

    while running:
        time.sleep(interval)

        def check():
            global variable
            fetcher.getdata(variable)
            datafetch = fetcher.datavalue 
            variable = variable + 1
            for loadsql in datafetch:
            
                try:
                    time.sleep(0)
                    keyretrieve = loadsql["publicKey"]
                    activestatus = loadsql["active"]
                    if debug:
                        logging.info("key is send to module")
                    if MainmoduleSQL.checkifpresent(keyretrieve,debug) == True:
                        if debug:
                            logging.info("Key already in db")
                            logging.info("Trying if node value is changed")
                        MainmoduleSQL.checkifrunning(keyretrieve,debug)
                        MainmoduleSQL.checkifpresentuser(keyretrieve)
                        try:
                            if activestatus > MainmoduleSQL.runningvalue:
                                if debug:
                                    logging.info("node is up")
                                MainmoduleSQL.updatestatus(keyretrieve,activestatus)
                                telegramclient.up(keyretrieve)
                                if MainmoduleSQL.usernode == True:
                                    telegramclient.userup(MainmoduleSQL.chatidvar,keyretrieve)
                        
                            if activestatus < MainmoduleSQL.runningvalue:
                                if debug:
                                    logging.info("node is down")  
                                MainmoduleSQL.updatestatus(keyretrieve,activestatus)
                                telegramclient.down(keyretrieve) 

                                if MainmoduleSQL.usernode == True:
                                    telegramclient.userdown(MainmoduleSQL.chatidvar,keyretrieve) 
                            else:
                                if debug:
                                    logging.info("nothing changed")  
                        except Exception as E:
                            logging.info('Error : {}'.format(E))     
               


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
            variable = 1 
            time.sleep(2)
            check()           



#main(1,True)
