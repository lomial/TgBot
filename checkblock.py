import Blockchain
import logging
import telegramclient
import config
import sched, time
from datetime import datetime, timedelta

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
running = True
chatiddev = config.chatiddev

def check():
    time_reg = datetime.today()
    while running:
        
        lastblock_reg = Blockchain.lastblock
        time.sleep(10)
        
        logging.info("lastblock:")
        logging.info(lastblock_reg)
    
        logging.info("time_reg:")
        logging.info(time_reg)
    
        if time_reg < datetime.today() - timedelta(minutes=5):
            
            logging.info("time_reg:")
            logging.info(time_reg)
        
            if lastblock_reg != Blockchain.lastblock:
                logging.info("Good Block")
                time_reg = datetime.today()
            

            if lastblock_reg == Blockchain.lastblock:
                logging.info("Bad  Block")
                telegramclient.checkblock(lastblock_reg)
                time_reg = datetime.today()



