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
            datasql = MainmoduleSQL.getdatauser()
            #countuser = sum(countuser) #преобразование в нужный тип данных tuple -> int
            
            if debug:
                logging.info("datasql")
                logging.info(datasql)
            
            
            for i in range(countuser):
                #print ("i=",i)
                try:
                    time.sleep(0)
                    pubkeyretrieve = functools.reduce(operator.add, (datasql[i][2]))
                    activestatus = int(datasql[i][12])
                    
                    if debug:
                        #logging.info("activestatus")
                        #logging.info(activestatus)
                        
                        logging.info("keyretrieve")
                        logging.info(pubkeyretrieve)
                    
                    if debug:
                        logging.info("key is send to module")
                        #logging.info(MainmoduleSQL.checkifpresent)
                        
                    if MainmoduleSQL.checkifpresent(pubkeyretrieve,debug) == True: 
                        
                        if debug:
                            logging.info("Key already in db")
                            logging.info("Trying if node value is changed")
                            
                        MainmoduleSQL.checkifrunning(pubkeyretrieve,debug)
                        MainmoduleSQL.checkifpresentuser(pubkeyretrieve)
                        
                        try:
                            #logging.info(MainmoduleSQL.runningvalue)
                            #logging.info(activestatus)
                            onlinenodedata = nodeinformation.getnodeinformation(pubkeyretrieve) 
                            
                            
                            if onlinenodedata[6] == "Yes":
                                runningvalue = 1
                                
                            elif onlinenodedata[6] == "No":
                                runningvalue = 0
                            
                            
                            if activestatus < runningvalue:
                                
                                if debug:
                                    logging.info("node is up")
                                MainmoduleSQL.updatestatus(pubkeyretrieve,runningvalue)
                                telegramclient.up(pubkeyretrieve)
                                if MainmoduleSQL.usernode == True:
                                    telegramclient.userup(MainmoduleSQL.chatidvar,pubkeyretrieve)
                        
                            if activestatus > runningvalue:
                                
                                if debug:
                                    logging.info("node is down")  
                                MainmoduleSQL.updatestatus(pubkeyretrieve,runningvalue)
                                telegramclient.down(pubkeyretrieve)
                                if MainmoduleSQL.usernode == True:
                                    telegramclient.userdown(MainmoduleSQL.chatidvar,pubkeyretrieve) 
                            else:
                                if debug:
                                    logging.info("nothing changed")
                                
                                
                        except Exception as E:
                            logging.info('Error : {}'.format(E))     
               
                    if MainmoduleSQL.checkifpresent(pubkeyretrieve,debug) == False:
                        if debug:
                            logging.info("Key is going to be stored in db")    
                        MainmoduleSQL.singlewrite(datasql[i])
                        time.sleep(0)
        
                except Exception as E:
                    logging.info('Error : {}'.format(E)) 
                    
        if variable < countuser:
            logging.info("Going to next str")
            time.sleep(2)
            variable = variable + 1
            check()
            
            
        if variable == countuser:
            logging.info("reached max srt Starting at str 1")
            time.sleep(2)
            variable = 0
            check() 
                
            

