import sqlite3
from sqlite3 import Error
import logging
import json
import requests
import telegramclient
import datetime
from decimal import *
import decimal
import time
from datetime import datetime, timedelta
from time import gmtime, strftime 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
getcontext().prec =14

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
        cursor.execute('''create table SWThistory (
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
            totalfee INTEGER, 
            timeswritter INTEGER, 
            storetime VARCHAR)''')
        logging.info ("Succes")
    except Exception as E:
        logging.error('Error :{}'.format(E))
    else:
        logging.info('table created')



def lastid():
    global idvalue
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM SWThistory ")
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
    cur.execute("SELECT * FROM SWThistory WHERE publickey=? ",key)
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
    cur.execute("SELECT * FROM SWThistory WHERE publickey=? ORDER BY storetime DESC LIMIT 1",var1)
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

def checktrust(var2,debug):
    if debug:
        logging.info("check if running module activated")
    global trustvalue
    global pkey
    var1 = (var2,)
    conn = create_connection(database)
    cur = conn.cursor()
    if debug:
        logging.info("checking db for trust status_1")
    cur.execute("SELECT * FROM SWThistory WHERE publickey=? ORDER BY storetime DESC LIMIT 1",var1)
    data2 = cur.fetchone()
    data = data2[7]
    pkey = data2[2]
        
    if debug:
        logging.info(data)
    try:
        trustvalue = data
        
    except Exception as E:
        logging.info('Error : {}'.format(E))  

def checklasttrust(var2,debug,hours,minutes):
    nowtime = datetime.today() 
    vartime = datetime.today() - timedelta(hours=hours, minutes=minutes)
    nowtime.strftime("%Y-%m-%d %H:%M:%S")
    vartime.strftime("%Y-%m-%d %H:%M:%S")
    if debug:
        logging.info("check if running module activated")
    global pkey
    try:
        feetotal = Decimal(0)
        feehour = int(0)
        var1 = (var2)
        conn = create_connection(database)
        cur = conn.cursor()
        stringsql1 = "SELECT * FROM SWThistory WHERE publickey='{}' AND storetime BETWEEN '{}' AND '{}' ORDER BY storetime ASC LIMIT 1".format(var1,vartime,nowtime)
        stringsql2 = "SELECT * FROM SWThistory WHERE publickey='{}' AND storetime BETWEEN '{}' AND '{}' ORDER BY storetime DESC LIMIT 1".format(var1,vartime,nowtime)
        if debug:
            logging.info("checking db for trust status_2")
        cur.execute(stringsql1)
        datavallow = cur.fetchone()
        cur.execute(stringsql2)
        datvalhigh = cur.fetchone()
        datalow = datavallow[7]
        datahigh = datvalhigh[7]
        datafeelow = datavallow[13]
        datafeehigh = datvalhigh[13]
        
        feetotal = Decimal(datafeehigh) - Decimal(datafeelow)
        endtotal = int(datahigh) - int(datalow)
        if feetotal == Decimal(0):
            feetotal = int(0)
        logging.info(feetotal) 
        
        if endtotal == int(0):
            endtotal = int(0)  
   
        trusthour = endtotal
        feehour = feetotal
           
        return trusthour,feehour

    except TypeError:
        trusthour = 0
        feehour = 0
    except Exception as E:
        logging.info('Error : {}'.format(E))  

def singlewrite(var1):
    
    vartime = datetime.today() 
    vartime.strftime("%Y-%m-%d %H:%M:%S")
    conn = create_connection(database)
    try:
        lastid()
        idval = int(idvalue) 
        idval = idval + 1
        
        
        ni = var1
        logging.info(ni)
        logging.info(idval)

        data = (idval), (ni["ip"]), (ni["publicKey"]), (ni["country"]), (ni["countryName"]), (ni["city"]), (ni["platform"]), (ni["countTrust"]), (ni["timeRegistration"]), (ni["timeActive"]), (ni["latitude"]), (ni["longitude"]), (ni["active"]), (ni["totalFee"]), (ni["timesWriter"]), (vartime)
        cur = conn.cursor()
        cur.execute('INSERT INTO SWThistory VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)

    except Exception as E:
        logging.info('Error : {}'.format(E))
    else:
        #telegramclient.dev()
        conn.commit()
        logging.info('data inserted')

def one():
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO SWThistory VALUES(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)')

    except Exception as E:
        logging.info('Error : {}'.format(E))
    else:
        conn.commit()
        logging.info('data inserted')

def updatestatus(key,active):
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute('UPDATE SWThistory SET active= ? WHERE publickey= ? ',(active,key))
        conn.commit()
        logging.info('data Updated')

    except Exception as E:
        logging.info('Error : {}'.format(E))


def tablewritetop():
    try:
        db = sqlite3.connect('testlib002')
        cursor = db.cursor()
        cursor.execute('''create table SWTtoptrust (
            id VARCHAR, 
            ip VARCHAR, 
            publickey VARCHAR, 
            country VARCHAR, 
            countryname VARCHAR,   
            countrust INTEGER, 
            active VARCHAR, 
            totalfee INTEGER, 
            timeswritter INTEGER, 
            storetime INTEGER)''')
        logging.info ("Succes")
    except Exception as E:
        logging.error('Error :{}'.format(E))
    else:
        logging.info('table created')

def lastidtop():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM SWTtoptrust ")
    #cur.execute("SELECT id FROM SWTmain WHERE active = (SELECT MAX(id) FROM SWTmain)")
    idvalue2 = cur.fetchone()
    idvalue = idvalue2[0]
    logging.info("The last id number is: {}".format(idvalue))
    return idvalue

def singlewritetop(var1,var2):
    vartime = datetime.today() 
    vartime.strftime("%Y-%m-%d %H:%M:%S")
    conn = create_connection(database)    
    try:
        idval = int(lastidtop())
        idval = idval + 1
        logging.info(var2)
        if var2 == None:
            trust_hour = 0
            fee_hour = 0
        if var2 != None:
        
            trust_hour = int(var2[0])
            fee_hour = int(var2[1])
            
        logging.error(trust_hour)
        logging.error(fee_hour)
        logging.info(idval)
        logging.info(var1)

        #data = (idval), (ni["ip"]), (ni["publicKey"]), (ni["country"]), (ni["countryName"]), (trust_hour), (ni["active"]), (fee_hour), (ni["timesWriter"]), (vartime)
        data = (idval), (var1[1]), (var1[2]), (var1[3]), (var1[4]), (trust_hour), (var1[12]), (fee_hour), (var1[14]), (vartime)
        cur = conn.cursor()
        cur.execute('INSERT INTO SWTtoptrust VALUES(?,?,?,?,?,?,?,?,?,?)',data)

    except Exception as E:
        logging.info('Error : {}'.format(E))
    else:
        #telegramclient.dev()
        conn.commit()
        logging.info('data inserted')

def checklasttrusttop(var2,debug,hours,minutes):
    nowtime = datetime.today() 
    vartime = datetime.today() - timedelta(hours=hours, minutes=minutes)
    nowtime.strftime("%Y-%m-%d %H:%M:%S")
    vartime.strftime("%Y-%m-%d %H:%M:%S")
    if debug:
        logging.info("check if running module activated")
    global pkey
    try:
        feetotal = Decimal(0)
        feehour = int(0)
        var1 = (var2)
        conn = create_connection(database)
        cur = conn.cursor()
        stringsql1 = "SELECT * FROM SWThistory WHERE publickey='{}' AND storetime BETWEEN '{}' AND '{}' ORDER BY storetime ASC LIMIT 1".format(var1,vartime,nowtime)
        stringsql2 = "SELECT * FROM SWThistory WHERE publickey='{}' AND storetime BETWEEN '{}' AND '{}' ORDER BY storetime DESC LIMIT 1".format(var1,vartime,nowtime)
        if debug:
            logging.info("checking db for trust status_3")
        cur.execute(stringsql1)
        datavallow = cur.fetchone()
        cur.execute(stringsql2)
        datvalhigh = cur.fetchone()
        datalow = datavallow[7]
        datahigh = datvalhigh[7]
        datafeelow = datavallow[13]
        datafeehigh = datvalhigh[13]
        
        feetotal = Decimal(datafeehigh) - Decimal(datafeelow)
        endtotal = int(datahigh) - int(datalow)
        if feetotal == Decimal(0):
            feetotal = int(0)
        logging.info(feetotal) 
        
        if endtotal == int(0):
            endtotal = int(0)        
        trusthour = endtotal
        feehour = feetotal
        return trusthour,feehour

    except TypeError:
        trusthour = 0
        feehour = 0
    except Exception as E:
        logging.info('Error : {}'.format(E))  


def deletetop():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("DELETE FROM SWTtoptrust ")
    conn.commit()
 
def fetch_trust_ratio_top():
    try:
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM SWTtoptrust ORDER BY countrust DESC, active DESC LIMIT 10")
        data2 = cur.fetchall()
        return data2

    except Exception as E:
        logging.info('Error : {}'.format(E))

tablewrite()
tablewritetop()
#print (checklasttrust("AN76mZMoJ18ZFyxvJ8rFSriHovYEcn1s8xweN41xBSAx",True,24,0))

