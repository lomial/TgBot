import json
import urllib2
import time
import requests
#pagenumber = 1
#checkpage = 1
pagecheck = urllib2.urlopen('https://monitor.credits.com/CreditsNetwork/Api/GetNodesData?page=1&limit=100')

jsonStr2 = urllib2.urlopen('https://monitor.credits.com/CreditsNetwork/Api/GetNodesData?page=2&limit=100')

json_data2 = json.load(jsonStr2)
pagedata = json.load(pagecheck)
#pagetrue = pagedata["haveNextPage"]
maxpage2 = pagedata["lastPage"]
maxpage = maxpage2 + 1
pagenumber = 1
checkpage = 1
#layout = {}
#layout['nodes'] = []
def fetch():
    global checkpage
    global pagenumber
    open('nodeinformation.txt', 'w').close()
    
    while checkpage < maxpage: 
        

        if checkpage < maxpage:
            jsonStr = urllib2.urlopen('https://monitor.credits.com/CreditsNetwork/Api/GetNodesData?page={}&limit=100'.format(pagenumber))
            json_data = json.load(jsonStr)
            storedata = json_data["nodes"]
    
            with open('nodeinformation.txt', 'a') as outfile:
                #json.dump(storedata, outfile)
                for p in storedata:
                    json.dump(storedata["ip"], outfile)
            print ("Data succes")
            #checkpage = checkpage + 1
            #pagenumber = pagenumber + 1
            #time.sleep(0.1)
            break
        if checkpage == maxpage:
            break        
            #for test in nodedata:
                #print test["publicKey"],test["country"],test["countTrust"]
             

def fetch2():
    global checkpage
    global pagenumber
    open('nodeinformation.txt', 'w').close()
    
    while checkpage < maxpage: 
        

        if checkpage < maxpage:
            jsonStr = urllib2.urlopen('https://monitor.credits.com/CreditsNetwork/Api/GetNodesData?page={}&limit=100'.format(pagenumber))
            json_data = json.load(jsonStr)
            storedata = json_data["nodes"]

            print storedata[0]
            #checkpage = checkpage + 1
            #pagenumber = pagenumber + 1
            #time.sleep(0.1)
            break
        if checkpage == maxpage:
            break        
            #for test in nodedata:
                #print test["publicKey"],test["country"],test["countTrust"]
             


def read():
    with open('nodeinformation.txt') as nodeopen:
        
        t = json.load(nodeopen)
        test5 = t
        #print (test5[0])
        for p in t:
            print(p["ip"],p["country"],p["active"])
        #print('Website: ' + p['website'])
        #print('From: ' + p['from'])
        #print('')





def simpel():

    a_dict = {'new_key': 'new_value'}

    with open('nodeinformation.txt') as f:
        data = json.load(f)

    data.update(a_dict)

    with open('nodeinformation.txt', 'w') as f:
        json.dump(data, f)    

    


#simpel()
#read()
fetch2()
#writejson()

#url = "https://monitor.credits.com/CreditsNetwork/Api/GetNodesData?page=1&limit=100"
#json_obj = urllib2.urlopen(url).read
#player_json_list = json.loads(json_obj)
#for player in player_json_list:
    #print player['nodes']