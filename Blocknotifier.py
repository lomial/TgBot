import Blockchain
import logging
import time
import telegramclient
import Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def blockchecker(interval,debug):
    running = True
    debug = debug
    global checkblock
    checkblock = Blockchain.lastblock

    while running:
        interval = interval 
        time.sleep(interval)

        if checkblock == 0 :
            logging.info("None value in pipeline")
            time.sleep(2)
            checkblock = Blockchain.lastblock

        if checkblock == Blockchain.lastblock:
            logging.info("Even score")
            if debug:
                logging.info("                                                               DEBUG BLOCKnotifier amount is %s",checkblock)
                
        if  Blockchain.lastblock < checkblock:
            logging.info ("Debug node went down")
            #telegramclient.down()
            checkblock = checkblock - 1


        if Blockchain.lastblock > checkblock:
            logging.info ('Debug New Block created with{}'.format(Blockchain.lastblocktx)) 
            telegramclient.newblock()
            checkblock = checkblock + 1

            
           