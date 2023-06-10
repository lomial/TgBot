import json
import logging
import fetcher
import requests
import config
import requests
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
debug = False
def getnodeinformation(publicadres):

    try:
        
        resp = requests.get('{}/Api/GetNodeData/{}'.format(config.networkurl,publicadres))
        jsonStr = resp.text
        json_data = json.loads(jsonStr)
        publickey = json_data['publicKey']
        #registrationtime = json_data['timeRegistration']
        country = json_data['countryName']
        city = json_data['city']
        totalfee = json_data['totalFee']
        trustcount = json_data['countTrust']
        timeswritter = json_data['timesWriter']
        active2 = json_data['active']
        try:
            val1 = float(timeswritter) / float(trustcount)
            writeratio = round(val1,2)
            writeratio = (""+"{:.2%}".format(writeratio))
        except Exception:
            writeratio = 0    

        if active2 == True:
            active = "Yes"
        if active2 == False:
            active = "No"  
        if totalfee == None:
            totalfee = 0          
        return publickey,country,city,totalfee,trustcount,timeswritter,active,writeratio
        
    
    except Exception as E:
        logging.info('Error : {}'.format(E))     


def consensus(publickey):
    
    try:
        logging.info("Fetching data")
        resp = requests.get('{}/api/Balance?id={}'.format(config.networkurl,publickey))
        jsonStr = resp.text
        balance = json.loads(jsonStr)
        logging.info(balance)
        if balance > 500000:
            balanceconsensus = True
            logging.info("Enough coins for entering consensus")
            return balanceconsensus

        if balance < 500000:
            balanceconsensus = False
            logging.info("Not enough coins for entering consensus")
            return balanceconsensus

    except Exception as E:
        logging.info('Error : {}'.format(E))   

def balance_get(publickey):

    try:
        logging.info("Fetching data")
        resp = requests.get('{}/api/Balance?id={}'.format(config.networkurl,publickey))
        jsonStr = resp.text
        balance = json.loads(jsonStr)
        logging.info(balance)
        staked = balance
        return staked
        
    except Exception as E:
        logging.info('Error : {}'.format(E))       
    
    
#print (getnodeinformation("AN76mZMoJ18ZFyxvJ8rFSriHovYEcn1s8xweN41xBSAx"))
#print (consensus("AN76mZMoJ18ZFyxvJ8rFSriHovYEcn1s8xweN41xBSAx"))



