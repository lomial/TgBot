import sqlite3
from sqlite3 import Error
import logging
import json
import requests
import telegramclient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

database = "testlib002"
key = "6WTWncHTBCrv6foypFNS7gdPX6avd8bMC1i6QGpxq9wx"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def tablewrite():
    try:
        db = sqlite3.connect('testlib002')
        cursor = db.cursor()
        cursor.execute('''create table SWTMain (
            id VARCHAR, 
            ip VARCHAR, 
            publickey VARCHAR, 
            country VARCHAR, 
            countryname VARCHAR, 
            city VARCHAR, 
            platform VARCHAR, 
            countrust INTEGER, 
            timeregistration VARCHAR, 
            timeactive VARCHAR, 
            latitude VARCHAR, 
            longitude VARCHAR, 
            active VARCHAR, 
            totalfee VARCHAR, 
            timeswritter INTEGER)''')
        logging.info ("Succes")
    except Exception as E:
        logging.error('Error :{}'.format(E))
    else:
        logging.info('table created')

def tablewriteuser():
    try:
        db = sqlite3.connect('testlib002')
        cursor = db.cursor()
        cursor.execute('''create table SWTuser ( 
            chatid VARCHAR,
            publickey VARCHAR,
            running INTEGER)''')
        logging.info ("Succes")
    except Exception as E:
        logging.error('Error :{}'.format(E))
    else:
        logging.info('table created')

def tablewritehourly():
    try:
        db = sqlite3.connect('testlib002')
        cursor = db.cursor()
        cursor.execute('''create table SWThour ( 
            chatid VARCHAR,
            publickey VARCHAR,
            running INTEGER)''')
        logging.info ("Succes")
    except Exception as E:
        logging.error('Error :{}'.format(E))
    else:
        logging.info('table created')

def Adduserkey(key,chatid):
    debug = True
    global userdatafound
    conn = create_connection(database)
    cur = conn.cursor()
    sqlline = "SELECT * FROM SWTuser WHERE publickey='{}' AND chatid='{}' ".format(key,chatid)
    cur.execute(sqlline)
    data = cur.fetchone()
    try:
        if data == None:
            try:
                runningstatus = True
                data = (chatid), (key), (runningstatus)
                cur = conn.cursor()
                logging.info(data)
                cur.execute('INSERT INTO SWTuser VALUES(?,?,?)',data)
                conn.commit()
                logging.info('data inserted')
                userdatafound = False
            except Exception as E:
                logging.info('Error : {}'.format(E))
                if debug:
                    logging.info("Key not found")
                
        elif data != None:
            userdatafound = True
            if debug:
                logging.info("Key found")

    except Exception as E:
        logging.info('Error : {}'.format(E))



def lastid():
    global idvalue
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM SWTmain ")
    #cur.execute("SELECT id FROM SWTmain WHERE active = (SELECT MAX(id) FROM SWTmain)")
    idvalue2 = cur.fetchone()
    idvalue = idvalue2[0]
    logging.info("The last id number is: {}".format(idvalue))


def checkifpresent(publickey,debug):
    conn = create_connection(database)
    cur = conn.cursor()
    key = (publickey,)
    if debug:
        logging.info("Checking key")
    cur.execute("SELECT * FROM SWTmain WHERE publickey=? ",key)
    data = cur.fetchone()
    try:
        if data == None:
            if debug:
                logging.info("Key not found")
                logging.info("Returning value")
            return False    
        elif data != None:
            if debug:
                logging.info("Key found")
                logging.info("Returning value")
            return True
            

    except Exception as E:
        logging.info('Error : {}'.format(E))

def checkifpresentuser(publickey):
    global chatidvar
    global telegramkey
    global usernode

    telegramkey = publickey
    debug = False
    conn = create_connection(database)
    cur = conn.cursor()
    key = (publickey,)
    if debug:
        logging.info("Checking key")
    cur.execute("SELECT * FROM SWTuser WHERE publickey=? ",key)
    data = cur.fetchone()
    try:
        if data == None:
            usernode = False
            if debug:
                logging.info("Key not found")
                logging.info("Returning value")


        elif data != None:
            cur.execute("SELECT * FROM SWTuser WHERE publickey=? ",key)
            runningdata = cur.fetchone()
            runningstatus = runningdata[2]
            chatidvar = runningdata[0]
            if debug:
                logging.info("Key found")
                logging.info("Returning value")
            if runningstatus == "1":
                usernode = True

            if runningstatus == "0":
                usernode = True    

    except Exception as E:
        logging.info('Error : {}'.format(E))

def checkifrunning(var2,debug):
    if debug:
        logging.info("check if running module activated")
    global runningvalue
    global pkey
    var1 = (var2,)
    conn = create_connection(database)
    cur = conn.cursor()
    if debug:
        logging.info("checking db for running status")
    cur.execute("SELECT * FROM SWTmain WHERE publickey=? ",var1)
    data2 = cur.fetchone()
    data = data2[12]
    pkey = data2[2]
    if debug:
        logging.info(data)
    try:
        if data == "0":
            #logging.info("Node Offline with publickey: {}".format(pkey))
            runningvalue = 0

        elif data == "1":
            #logging.info("Node is running with publickey: {}".format(pkey))
            runningvalue = 1

    except Exception as E:
        logging.info('Error : {}'.format(E))    



def singlewrite(var1):
    conn = create_connection(database)
    try:
        lastid()
        idval = int(idvalue) 
        idval = idval + 1

        ni = var1
        logging.info(ni)
        logging.info(idval)

        data = (idval), (ni["ip"]), (ni["publicKey"]), (ni["country"]), (ni["countryName"]), (ni["city"]), (ni["platform"]), (ni["countTrust"]), (ni["timeRegistration"]), (ni["timeActive"]), (ni["latitude"]), (ni["longitude"]), (ni["active"]), (ni["totalFee"]), (ni["timesWriter"])
        cur = conn.cursor()
        cur.execute('INSERT INTO SWTmain VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)
        keyvar = data[2]
        telegramclient.addkey(keyvar)
        


    except Exception as E:
        logging.info('Error : {}'.format(E))
    else:
        conn.commit()
        logging.info('data inserted')

def one(conn):
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO SWTmain VALUES(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)')

    except Exception as E:
        logging.info('Error : {}'.format(E))
    else:
        conn.commit()
        logging.info('data inserted')

def updatestatus(key,active):
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute('UPDATE SWTmain SET active= ? WHERE publickey= ? ',(active,key))
        conn.commit()
        logging.info('data Updated')

    except Exception as E:
        logging.info('Error : {}'.format(E))

def updateuser(chatid,active,key):
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute('UPDATE SWTuser SET running= ? WHERE publickey= ? AND chatid=?',(active,key,chatid))
        conn.commit()
        logging.info('data Updated')

    except Exception as E:
        logging.info('Error : {}'.format(E))

def alltime_trust():
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM SWTmain ORDER BY countrust DESC, active DESC LIMIT 10")
        data2 = cur.fetchall()
        return data2
        
    except Exception as E:
        logging.info('Error : {}'.format(E))

def alltime_written():
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM SWTmain ORDER BY timeswritter DESC, active DESC LIMIT 10")
        data2 = cur.fetchall()
        return data2

    except Exception as E:
        logging.info('Error : {}'.format(E))

def fetchrunning():
    debug = True
    if debug:
        logging.info("fetch running")
    conn = create_connection(database)
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM SWTmain WHERE active=1 ")
        data2 = cur.fetchall()
        return data2

    except Exception as E:
        logging.info('Error : {}'.format(E))    

def Addhourkey(key,chatid):
    debug = True
    global userdatafound
    conn = create_connection(database)
    cur = conn.cursor()
    sqlline = "SELECT * FROM SWThour WHERE publickey='{}' AND chatid='{}' ".format(key,chatid)
    cur.execute(sqlline)
    data = cur.fetchone()
    try:
        if data == None:
            try:
                runningstatus = True
                data = (chatid), (key), (runningstatus)
                cur = conn.cursor()
                logging.info(data)
                cur.execute('INSERT INTO SWThour VALUES(?,?,?)',data)
                conn.commit()
                logging.info('data inserted')
                userdatafound = False
            except Exception as E:
                logging.info('Error : {}'.format(E))
                if debug:
                    logging.info("Key not found")
                
        elif data != None:
            userdatafound = True
            if debug:
                logging.info("Key found")

    except Exception as E:
        logging.info('Error : {}'.format(E))

def checkifpresenthour(publickey):
    global chatidvar
    global telegramkey
    global usernode

    telegramkey = publickey
    debug = False
    conn = create_connection(database)
    cur = conn.cursor()
    key = (publickey,)
    if debug:
        logging.info("Checking key")
    cur.execute("SELECT * FROM SWThour WHERE publickey=? ",key)
    data = cur.fetchone()
    try:
        if data == None:
            usernode = False
            if debug:
                logging.info("Key not found")
                logging.info("Returning value")


        elif data != None:
            cur.execute("SELECT * FROM SWThour WHERE publickey=? ",key)
            runningdata = cur.fetchone()
            runningstatus = runningdata[2]
            chatidvar = runningdata[0]
            if debug:
                logging.info("Key found")
                logging.info("Returning value")
            if runningstatus == "1":
                usernode = True

            if runningstatus == "0":
                usernode = True    

    except Exception as E:
        logging.info('Error : {}'.format(E))

def updatehour(chatid,active,key):
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute('UPDATE SWThour SET running= ? WHERE publickey= ? AND chatid=?',(active,key,chatid))
        conn.commit()
        logging.info('data Updated')

    except Exception as E:
        logging.info('Error : {}'.format(E))

def fetch_hour_nodes():
    debug = True
    if debug:
        logging.info("fetch hour nodes")
    conn = create_connection(database)
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM SWThour ")
        data2 = cur.fetchall()
        return data2

    except Exception as E:
        logging.info('Error : {}'.format(E))

def fetch_user_nodes(chatid):
    chatid = int(chatid)
    debug = True
    if debug:
        logging.info("fetch User nodes")
    conn = create_connection(database)
    cur = conn.cursor()
    sqtext = "SELECT * FROM SWThour WHERE chatid={}".format(chatid)
    try:
        cur.execute(sqtext)
        data2 = cur.fetchall()
        return data2

    except Exception as E:
        logging.info('Error : {}'.format(E))




tablewrite()
tablewriteuser()
tablewritehourly()
#Adduserkey("bNF5NLrQHhTpqxaVaSYQDQm85KjWVxLKJFTq34WnswP",530871094)
#print (checkifpresent("EsWnHGtNx8fDFwfLBNR5xwpeVpCt79Bc2uj7ZSpwdYzu",True))
#updateuser(530871094,True,"bNF5NLrQHhTpqxaVaSYQDQm85KjWVxLKJFTq34WnswP")

