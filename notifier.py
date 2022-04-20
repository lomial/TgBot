import fetcher
import logging
import time
import telegramclient
import Setup
import sqlite3
import HismoduleSQL
database = "testlib002"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)



def checker2(interval,debug):
    running = Setup.running
    debug = debug
    global checkcount
    checkcount = fetcher.onlinecount
    time.sleep(Setup.interval)

    while running:
        if running == False:
            break
        interval = interval 
        time.sleep(interval)
        try:
            if checkcount == 0 :
                logging.info("None value in pipeline")
                time.sleep(2)
                checkcount = fetcher.onlinecount
                time.sleep(1)
                #telegramclient.monitordown()

            if checkcount == fetcher.onlinecount:
                logging.info("Even score")
                if debug:
                    logging.info("                               DEBUG Notifier amount is %s",checkcount)
                    
            elif fetcher.onlinecount < checkcount:
                logging.info ("Debug node went down")
                checkcount = checkcount - 1
                telegramclient.down()
                
            elif fetcher.onlinecount > checkcount:
                logging.info ('Debug went up') 
                checkcount = checkcount + 1
                telegramclient.up()
            
        except Exception:
            logging.error ("Major notifier error")
            raise

def checker(interval,debug):
    conn = HismoduleSQL.create_connection(database)
    cur = conn.cursor()
    testid = "2"
    cur.execute("SELECT * FROM SWTmain WHERE id=? ",testid)
    data2 = cur.fetchone()
    running = Setup.running
    debug = debug
    time.sleep(Setup.interval)

    while running:
        if running == False:
            break
        interval = interval 
        time.sleep(interval)
        try:
            if checkcount == 0 :
                logging.info("None value in pipeline")
                time.sleep(2)
                checkcount = fetcher.onlinecount
                time.sleep(1)
                #telegramclient.monitordown()

            if checkcount == fetcher.onlinecount:
                logging.info("Even score")
                if debug:
                    logging.info("                               DEBUG Notifier amount is %s",checkcount)
                    
            elif fetcher.onlinecount < checkcount:
                logging.info ("Debug node went down")
                checkcount = checkcount - 1
                telegramclient.down()
                
            elif fetcher.onlinecount > checkcount:
                logging.info ('Debug went up') 
                checkcount = checkcount + 1
                telegramclient.up()
            
        except Exception:
            logging.error ("Major notifier error")
            raise            
         
            
  
