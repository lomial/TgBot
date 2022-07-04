import Blockchain
import logging
import telegramclient
import config
import sched, time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
running = True
chatiddev = config.chatiddev

def check():
    
    while running:
        time.sleep(10)
        lastblock_reg = Blockchain.lastblock
    
    
        logging.info("lastblock:")
        logging.info(lastblock_reg)
        
        time.sleep(290)
        if lastblock_reg != Blockchain.lastblock:
            logging.info("Good")
            #time.sleep(3600)
            

        if lastblock_reg == Blockchain.lastblock:
            telegramclient.checkblock(lastblock_reg)
            time.sleep(600)


