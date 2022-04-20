import nodeinformation
import MainmoduleSQL
import time,logging
import telegramclient
def main():

    while True:
        time.sleep(3600)
        hour_data = MainmoduleSQL.fetch_hour_nodes()
        for a in hour_data:
            if a[2] == 1:
                logging.info("Sending message")
                telegramclient.public_hour(a[0],a[1])
            if a[2] == 0:
                logging.info("nothing to do")  
        #time.sleep(10)          


def singlesend(chatid):
    user_data = MainmoduleSQL.fetch_user_nodes(chatid)
    print (user_data)
    if user_data != None:
        for a in user_data:
            telegramclient.public_hour(chatid,a[1])



