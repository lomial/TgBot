
import threading 
import fetcher
import Debug
import telegramclient
import time
import notifier
import logging
import Blocknotifier
import Blockchain
import signal,sys
import dbrunning
import config
import dbhistoricrunning
import swtoprunning,swthourmodule
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(threadName)-12.12s',level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

debug = False
running = True
runningdebug = True
debugtelegram = True



interval = config.refreshinterval
chatid = config.chatid
chatiddev = config.chatiddev


setuptoken = config.token






if __name__ == "__main__":
    global x1
    # creating thread 
    t1 = threading.Thread(target=fetcher.connect, args=(debug,running,interval)) 
    logging.info("Setting Thread Fetcher")

    t2 = threading.Thread(target=Debug.start, args=(runningdebug,interval)) 
    logging.debug("Setting Thread Debug Module")

    t3 = threading.Thread(target=telegramclient.main,)
    logging.debug("Setting Thread Telegramclient")
    
    t4 = threading.Thread(target=dbrunning.main, args=(interval,debug))
    logging.debug("Setting Thread Notifier")

    #t5 = threading.Thread(target=Blocknotifier.blockchecker, args=(interval,debug))
    logging.debug("Setting Thread Blocknotifier")

    t6 = threading.Thread(target=Blockchain.blockchain, args=(debug,running,interval))
    logging.debug("Setting Thread Blockchain")

    t7 = threading.Thread(target=dbhistoricrunning.main, args=(interval,debug))
    logging.debug("Setting History module")

    t8 = threading.Thread(target=swtoprunning.main)
    logging.debug("Setting top module")

    t9 = threading.Thread(target=swthourmodule.main)
    logging.debug("Setting hourly module")
#------
    
    t1.start() 
    logging.info("Starting Thread Fetcher")
    #time.sleep(2)

   
    t2.start() 
    logging.debug("Starting Debug Node")
    #time.sleep(2)
    
    t3.start()
    logging.debug("Starting Thread Telegram Client")
    #time.sleep(2)

    t4.start()
    logging.debug("Starting Thread DBRunning")

    #t5.start()
    #print "Starting blocknotifier"
    #logging.debug("Starting Thread Blocknotifier")

    t6.start()
    logging.debug("Starting Thread Blockchain")
    
    t7.start()
    logging.debug("Starting History")
    
    t8.start()
    logging.debug("Starting top module")
    
    t9.start()
    logging.debug("Starting hourly module")


    x1 = t1.is_alive()
    logging.info(x1)

    x2 = t2.is_alive()
    logging.info(x2)

    x3 = t3.is_alive()
    logging.info(x3)

    x4 = t4.is_alive()
    logging.info(x4)

    x6 = t6.is_alive()
    logging.info(x6)

    x7 = t7.is_alive()
    logging.info(x7)

    x8 = t8.is_alive()
    logging.info(x8)

    x9 = t9.is_alive()
    logging.info(x9)

    while True:
        telegramclient.x1 = x1
        telegramclient.x2 = x2
        telegramclient.x3 = x3
        telegramclient.x4 = x4
        telegramclient.x6 = x6
        telegramclient.x7 = x7
        telegramclient.x8 = x8
        telegramclient.x9 = x9

        time.sleep(100)
        if x1 == False:
            telegramclient.module_error("Module 1")
            t1.start() 

        if x2 == False:
            telegramclient.module_error("Module 2")
            t2.start()

        if x3 == False:
            telegramclient.module_error("Module 3")
            t3.start()    

        if x4 == False:
            telegramclient.module_error("Module 4")
            t4.start()

        if x6 == False:
            telegramclient.module_error("Module 6")
            t6.start()

        if x7 == False:
            telegramclient.module_error("Module 7")
            t7.start()

        if x8 == False:
            telegramclient.module_error("Module 8")
            t8.start()

        if x9 == False:
            telegramclient.module_error("Module 8")
            t9.start()    
