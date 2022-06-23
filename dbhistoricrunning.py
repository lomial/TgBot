import functools
import json
import operator
import requests
import sqlite3
import MainmoduleSQL
import logging
import time
import Datamodule
import fetcher 
import telegramclient
import nodeinformation
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
running = True
debug = True

def main(interval,debug):
    global variable
    countuser = sum(MainmoduleSQL.getcountuser())
    
    variable = 0
    
    
    while running:
        time.sleep(interval)
        
        def check():        
            global variable
            countuser = sum(MainmoduleSQL.getcountuser())
            #logging.info("countuser")
            #logging.info(countuser)     
            datasql = MainmoduleSQL.getdatauser()
            #countuser = sum(countuser) #преобразование в нужный тип данных tuple -> int
            
            if debug:
                logging.info("datasql")
                logging.info(datasql)
            
            
            for i in range(countuser+1):
                #print ("i=",i)
                try:
                    time.sleep(0)
                    keyretrieve = functools.reduce(operator.add, (datasql[i][2]))
                    activestatus = int(datasql[i][12])
                    
                    if debug:
                        logging.info("activestatus")
                        logging.info(activestatus)
                        
                    logging.info("keyretrieve")
                    logging.info(keyretrieve)
                    
                    if debug:
                        logging.info("key is send to module")
                        logging.info(MainmoduleSQL.checkifpresent)
                        
                    try:
                        logging.info("keyretrieve")
                        logging.info(MainmoduleSQL.runningvalue)
                        logging.info("activestatus")
                        logging.info(activestatus)
                        onlinenodedata = nodeinformation.getnodeinformation(keyretrieve) 
                            
                            
                        if onlinenodedata[6] == "Yes":
                            runningvalue = 1
                                
                        elif onlinenodedata[6] == "No":
                            runningvalue = 0
                            
                            
                        if activestatus < runningvalue:
                                
                            if debug:
                                logging.info("node is up")
                            MainmoduleSQL.updatestatus(keyretrieve,runningvalue)
                            telegramclient.up(keyretrieve)
                            if MainmoduleSQL.usernode == True:
                                telegramclient.userup(MainmoduleSQL.chatidvar,keyretrieve)
                        
                        if activestatus > runningvalue:
                                
                            if debug:
                                logging.info("node is down")  
                            MainmoduleSQL.updatestatus(keyretrieve,runningvalue)
                            telegramclient.down(keyretrieve)
                            if MainmoduleSQL.usernode == True:
                                telegramclient.userdown(MainmoduleSQL.chatidvar,keyretrieve) 
                        else:
                            if debug:
                                logging.info("nothing changed")
                                
                                
                    except Exception as E:
                        logging.info('Error : {}'.format(E))     
               
        
                except Exception as E:
                    logging.info('Error : {}'.format(E)) 
                    
        if variable < countuser+1:
            logging.info("Going to next str")
            time.sleep(2)
            variable = variable + 1
            check()
            
            
        if variable == countuser+1:
            logging.info("reached max srt Starting at str 1")
            time.sleep(2)
            variable = 0
            check() 
                
            

