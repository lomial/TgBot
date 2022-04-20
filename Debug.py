import time
import fetcher


def start (runningdebug,interval):
    running = runningdebug
    interval = interval * 4

    while running:
        time.sleep(interval)
        print (fetcher.onlinecount)
        #print "variable{}".format(checkcount)

    

 