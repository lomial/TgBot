import sqlite3
from sqlite3 import Error
import logging
import json
import requests
import telegramclient
from datetime import datetime, timedelta
from decimal import *
import decimal
import time
import MainmoduleSQL
from datetime import datetime, timedelta
from time import gmtime, strftime 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

running = True
debug = False

def deleteoldstring(interval,debug):       
    #vartime = datetime.today() - timedelta(days=30)
    deletepool = [0,1,2,3,4,5,6,7,8,9]
    i = 0
    #ito = [1,2,3,4,5,6,7,8,9,10]
    #nowtime = datetime.today()
    #vartimestr = vartime.strftime("%Y-%m-%d %H:%M:%S") #из даты в строку

    while running:
        time.sleep(interval)
            
        def check():
        
            #conn = MainmoduleSQL.create_connection(MainmoduleSQL.database)
            #cur = conn.cursor()
            #cur.execute("SELECT COUNT(id) FROM SWThistory")
            #countstr = cur.fetchone()  
            #cur = conn.close()
        
            conn = MainmoduleSQL.create_connection(MainmoduleSQL.database)
            cur = conn.cursor()
            cur.execute("SELECT * FROM SWThistory LIMIT 10")
            fullinfo = cur.fetchall() 
            #logging.info("fullinfo=")
            #logging.info(fullinfo)
            cur = conn.close()                
            
            for i in deletepool:
                try:  
                    #logging.info("i=")
                    #logging.info(i)       
            
                    dbtimehistory = datetime.strptime(fullinfo[i][15], "%Y-%m-%d %H:%M:%S.%f") #из строки в дату обратно

                    #logging.info("dbtimehistory=")
                    #logging.info(dbtimehistory)

                    if dbtimehistory < datetime.today() - timedelta(days=30):
                        #deletepool.append(fullinfo[0])
                        #logging.info("добавлено значение в пул")
                        #logging.info(deletepool)
                        conn = MainmoduleSQL.create_connection(MainmoduleSQL.database)
                        cur = conn.cursor()
                        #logging.info("проверка успешна, на удаление")
                        #logging.info(dbtimehistory)
                        delstrDB = "DELETE FROM SWThistory WHERE storetime='{}'".format(fullinfo[i][15])
                        cur.execute(delstrDB)
                        conn.commit()  
                        #logging.info("запись удалена")
                        #logging.info(delstrDB)
                        cur = conn.close() 
                        #logging.info('last id'+ MainmoduleSQL.lastid.idvalue)
                        time.sleep(0)   
                    else:
                        if debug:
                            logging.info("проверка прошла удаление не требуется")
                
                except Exception as E:
                    logging.info('Error : {}'.format(E)) 
                
                
            
        #nowtime.strftime("%Y-%m-%d %H:%M:%S")
        #vartime.strftime("%Y-%m-%d %H:%M:%S")
    
            
    #logging.info("vartime")
    #logging.info(vartime)
        if i < 9:
            time.sleep(0)  
            check()
    
        if i == 9:
            time.sleep(120)  
            i = 0
            check()
            
                
                    
                    
                
            
    
    
    
    
    
    
    
    
    
    

