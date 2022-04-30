import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import logging
import sys
import nodeinformation
import fetcher
import Setup
import Blockchain
import notifier
import MainmoduleSQL
import HismoduleSQL
import swthourmodule

version = "0.2"

Succes = "the message is successfully sended"
token = Setup.setuptoken
bot = telegram.Bot(token= token)
chatid = Setup.chatid
chatiddev = Setup.chatiddev
chatiddebug = Setup.chatiddev
debugtelegram = Setup.debugtelegram
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
reply_keyboard = [['public adres'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#logging settings
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def help(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    bot.send_message(chat_id=userid, text='''
Information regarding SWT Node update Bot

Version : {}

Current functions of the SWT Bot:

The Bot sends messages to the Technical chat of SWT when Nodes are going offline or online

/start function allocated to the bot developer

/help Displays all bot functions, you are getting this message

/release Release notes of the current version [NEW]

/onlinenode Shows you the amount of Online Nodes at this moment in time

/offlinenode Shows you the amount of Offline Nodes at this moment in time

/totalnodes The number of registered Nodes running the SWT Blockchain

/lastblock Displays the latest block of the SWT public Blockchain with the number of transactions

/public This function requires your public Key information to retrieve your Node information Example below 

/public HgjVJ1xsEXqnkP77BVNFAbEzPapUfskAeuMpnTtjtidq

/10min This functions shows amount trust/fee in 10 min

/30min This functions shows amount trust/fee in 30 min

/onehour This functions shows amount trust/fee in 1H

/top10alltrust This function shows highest trust count of running nodes

/top10allwritten This function shows highest writer of running nodes

/top10last24h This functions show best performing nodes last 24H

/top10last24hstake This functions show best performing nodes last 24H with staking

/status This function shows module status of the bot

/mynodes This function shows which nodes are stored in hourly notifications

/mynodestats This function manually overwrite the hourly notifications and sends 1 time the information regarding your nodes after this the hourly notification continues

/bestnode This functions shows the best peforming node last 24H

Private notifcations:

/notion This function enables private notifcations when entered public key example below
/notion HgjVJ1xsEXqnkP77BVNFAbEzPapUfskAeuMpnTtjtidq

/notioff This function Disables private notifications with given public key example below
/notioff HgjVJ1xsEXqnkP77BVNFAbEzPapUfskAeuMpnTtjtidq

Hourly notifications:

/houron This function will enable hourly statistics about your node
/houron HgjVJ1xsEXqnkP77BVNFAbEzPapUfskAeuMpnTtjtidq

/houroff This function will disable hourly statistics about your node
/houroff HgjVJ1xsEXqnkP77BVNFAbEzPapUfskAeuMpnTtjtidq

It also works when sending private messages to the bot directly 

Bot is still under Development and will get a lot more features in the future

If there are any questions please contact me !

Created by @swtsupport
    '''.format(version))

def release(update, context):
    update.message.reply_text('''
Information regarding development in new version of SWT Bot

Version {}

- In the future there will be updates for this bot

    '''.format(version))

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('bot already started')


def public(update, context):
    
    returnkey = update.message.text[8:]
    #returnkey = keystring[:8]
    if debugtelegram:
        bot.send_message(chat_id=chatiddev, text="Node information issued with key: {}".format(returnkey))
 
    node_data = nodeinformation.getnodeinformation(returnkey)
    consensus_data = nodeinformation.consensus(returnkey)
    staked = nodeinformation.balance_get(returnkey)
    node_lastcount = HismoduleSQL.checklasttrust(returnkey,True,24,0)
    if node_lastcount == None:
        node_lastcount = 0,0
    public_key = node_data[0]
    country = node_data[1]
    city = node_data[2]
    totalfee = node_data[3]
    trustcount = node_data[4]
    timeswritter = node_data[5]
    active = node_data[6]
    writeratio = node_data[7]
    last_fee = node_lastcount[1]
    last_trust = node_lastcount[0]
    
    
    
    
    if public_key == None:
        update.message.reply_text("This key seems to be non exisiting on the SWT platform")
        
    else:
        """This will give information regarding node status"""
        #bot.send_message(chat_id=chatiddebug, text="System booting up")
        update.message.reply_text('''
Total information of node
Public key: {}
Country: {}
City: {}
Total fee earned {}
Trust count till now {}
Blocks written {}
If the node is running now : {}
Enough coins for consensus : {}
Trust count last 24H: {}
Total fee last 24H {}
Written block ratio: {}
Staked amount is: {}
        '''.format(public_key,country,city,totalfee,trustcount,timeswritter,active,consensus_data,last_trust,last_fee,writeratio,staked))

    return ConversationHandler.END
def notion(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[8:]
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
         bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:
        MainmoduleSQL.Adduserkey(returnkey2,userid)
        if MainmoduleSQL.userdatafound == False:
            bot.send_message(chat_id=chatiddebug, text="Notifications turned on for {}".format(returnkey2))
            bot.send_message(chat_id=userid, text="Notifications turned on for this chat with this key {}".format(returnkey2))
        if MainmoduleSQL.userdatafound == True:
            bot.send_message(chat_id=userid, text="The key {} is already added to the private notifications for turning this key on type /on with key".format(returnkey2,returnkey2))

def userup(chatidvar,key):
    bot.send_message(chat_id=chatidvar, text="[Private message]Your node went Online with key: {}".format(key))

def userdown(chatidvar,key):
    bot.send_message(chat_id=chatidvar, text="[Private message]Your node went Offline with key: {}".format(key))

def notioff(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[9:]
    value = False
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
        bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:    
        MainmoduleSQL.updateuser(userid,value,returnkey2)
        bot.send_message(chat_id=chatiddebug, text="Notifications turned off for {}".format(returnkey2))
        bot.send_message(chat_id=userid, text="notifications turned off for : {}".format(returnkey2))

def on(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[4:]
    value = True
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
        bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:    
        MainmoduleSQL.updateuser(userid,value,returnkey2)
        bot.send_message(chat_id=chatiddebug, text="Notifications turned on for {}".format(returnkey2))
        bot.send_message(chat_id=userid, text="notifications turned on for : {}".format(returnkey2))

def bestnode(update, context):
    """Send a message when the command /start is issued."""
    x = HismoduleSQL.fetch_trust_ratio_top()
    n1 = x[0][5],x[0][2],x[0][4]
    p1 = n1[1]
    balance = nodeinformation.balance_get(p1)
    data_his = HismoduleSQL.checklasttrust(p1,True,24,0)
    total_fee = data_his[1]
    update.message.reply_text('''
    Best performing node last 24H
Count={}
TotalFee={}
Public={} 
Country={}
Staked={}
'''.format(n1[0],total_fee,p1,n1[2],balance))

def worstnode(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Staking for Alexander is still not received')    
       
def onlinenode(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("There are {} nodes connected to SWT platform at the moment.".format(fetcher.onlinecount))
    logging.info(Succes) 

def offlinenode(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("There are {} nodes not connected to SWT platform at the moment.".format(fetcher.offlinecount))
    logging.info(Succes)    

def totalnode(update, context):
    """Send a message when the command /help is issued."""
    totalnodes = fetcher.onlinecount + fetcher.offlinecount
    update.message.reply_text("There are {} nodes registered to SWT platform at the moment.".format(totalnodes))
    logging.info(Succes) 

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)
 
def down(keyreg):
    if nodeinformation.consensus(keyreg) == True:
        varcons = "Yes"
    if nodeinformation.consensus(keyreg) == False:
        varcons = "No" 
    bot.send_message(chat_id=chatid, text="Node went Offline[{}] Key: {} Running consensus: {}".format(fetcher.onlinecount,MainmoduleSQL.pkey,varcons))

def addkey(keyreg):
    if nodeinformation.consensus(keyreg) == True:
        varcons = "Yes"
    if nodeinformation.consensus(keyreg) == False:
        varcons = "No"    
    bot.send_message(chat_id=chatid, text="New node detected public key: {} Running consensus: {} ".format(keyreg,varcons))
    
def module_error(thread):
    bot.send_message(chat_id=chatiddev, text="Module restarted {}".format(thread))


def up(keyreg):
    if nodeinformation.consensus(keyreg) == True:
        varcons = "Yes"
    if nodeinformation.consensus(keyreg) == False:
        varcons = "No" 
    bot.send_message(chat_id=chatid, text="Node went Online[{}] Key: {} Enough balance for running consensus: {}".format(fetcher.onlinecount,MainmoduleSQL.pkey,varcons))

def newblock():
    bot.send_message(chat_id=chatid, text="Block :{} Created with {} ".format(Blockchain.lastblock,Blockchain.lastblocktx))

def latestblock(update, context):
    update.message.reply_text("The latest Block at this moment is :{} with amount tx: {}".format(Blockchain.lastblock,Blockchain.lastblocktx))

def monitordown():
    bot.send_message(chat_id=chatid, text=" Starting bot / no connection ")

def dev():
    bot.send_message(chat_id=chatid, text=" Change detected storing data[NEW] ")

def status(update, context):
    update.message.reply_text("""
    Bot running Status:
Module 1 is running: {}
Module 2 is running: {}
Module 3 is running: {}
Module 4 is running: {}
Module 6 is running: {}
Module 7 is running: {}
Module 8 is running: {}
Module 9 is running: {}
    """.format(x1,x2,x3,x4,x6,x7,x8,x9))

x1 = False 
x2 = False
x3 = False
x4 = False
x6 = False
x7 = False
x8 = False
x9 = False


#---------------------------------------------------------------------------

def onehour(update, context):
    returnkey = update.message.text[9:]
    if debugtelegram:
        bot.send_message(chat_id=chatiddev, text="Node information issued with key: {}".format(returnkey))
    node_data = nodeinformation.getnodeinformation(returnkey)
    node_lastcount = HismoduleSQL.checklasttrust(returnkey,True,1,0)
    public_key = node_data[0]
    last_fee = node_lastcount[1]
    last_trust = node_lastcount[0]
    
    
    if public_key == None:
        update.message.reply_text("This key seems to be non exisiting on the SWT platform")
    else:
        """This will give information regarding node status"""
        update.message.reply_text('''
Trust count last 1H: {}
Total fee last 1H {}
        '''.format(last_trust,last_fee))

def tenmin(update, context):
    #del HismoduleSQL.trusthour

    returnkey = update.message.text[7:]
    if debugtelegram:
        bot.send_message(chat_id=chatiddev, text="Node information issued with key: {}".format(returnkey))
        
    node_data = nodeinformation.getnodeinformation(returnkey)
    node_lastcount = HismoduleSQL.checklasttrust(returnkey,True,0,10)
    public_key = node_data[0]
    last_fee = node_lastcount[1]
    last_trust = node_lastcount[0]

    if public_key == None:
        update.message.reply_text("This key seems to be non exisiting on the SWT platform")
    else:
        """This will give information regarding node status"""
        update.message.reply_text('''
Trust count last 10M: {}
Total fee last 10M {}
        '''.format(last_trust,last_fee))        

def thirtymin(update, context):
    returnkey = update.message.text[7:]
    if debugtelegram:
        bot.send_message(chat_id=chatiddev, text="Node information issued with key: {}".format(returnkey))
        
    node_data = nodeinformation.getnodeinformation(returnkey)
    node_lastcount = HismoduleSQL.checklasttrust(returnkey,True,0,30)
    public_key = node_data[0]
    last_fee = node_lastcount[1]
    last_trust = node_lastcount[0]
    
    if public_key == None:
        update.message.reply_text("This key seems to be non exisiting on the SWT platform")
    else:
        """This will give information regarding node status"""
        update.message.reply_text('''
Trust count last 30M: {}
Total fee last 30M {}
        '''.format(last_trust,last_fee))

def debug3(update, context):
    var = update.message.from_user
    var2 = update.message.chat_id
    userid = var["id"]
    update.message.reply_text("userid:{}".format(userid))
    update.message.reply_text("chatid:{}".format(var2))

def top10AllTrust(update, context):
    x = MainmoduleSQL.alltime_trust()
    n1 = x[0][7],x[0][2],x[0][3]
    n2 = x[1][7],x[1][2],x[1][3]
    n3 = x[2][7],x[2][2],x[2][3]
    n4 = x[3][7],x[3][2],x[3][3]
    n5 = x[4][7],x[4][2],x[4][3]
    n6 = x[5][7],x[5][2],x[5][3]
    n7 = x[6][7],x[6][2],x[6][3]
    n8 = x[7][7],x[7][2],x[7][3]
    n9 = x[8][7],x[8][2],x[8][3]
    n10 = x[9][7],x[9][2],x[9][3]
    p1 = n1[1]
    p1 = p1[:6]
    p2 = n2[1]
    p2 = p2[:6]
    p3 = n3[1]
    p3 = p3[:6]
    p4 = n4[1]
    p4 = p4[:6]
    p5 = n5[1]
    p5 = p5[:6]
    p6 = n6[1]
    p6 = p6[:6]
    p7 = n7[1]
    p7 = p7[:6]
    p8 = n8[1]
    p8 = p8[:6]
    p9 = n9[1]
    p9 = p9[:6]
    p10 = n10[1]
    p10 = p10[:6]
    update.message.reply_text('''
    Top 10 Trust Count of running nodes

n1 Count={}Public={} Country={}
n2 Count={}Public={} Country={}
n3 Count={}Public={} Country={}
n4 Count={}Public={} Country={}
n5 Count={}Public={} Country={}
n6 Count={}Public={} Country={}
n7 Count={}Public={} Country={}
n8 Count={}Public={} Country={}
n9 Count={}Public={} Country={}
n10 Count={}Public={} Country={}
    '''.format(n1[0],p1 , n1[2], n2[0],p2 , n2[2], n3[0], p3, n3[2], n4[0], p4, n4[2], n5[0], p5, n5[2], n6[0], p6, n6[2], n7[0], p7, n7[2], n8[0], p8, n8[2], n9[0], p9, n9[2], n10[0], p10, n10[2]))


def top10AllWritten(update, context):
    x = MainmoduleSQL.alltime_written()
    n1 = x[0][14],x[0][2],x[0][3]
    n2 = x[1][14],x[1][2],x[1][3]
    n3 = x[2][14],x[2][2],x[2][3]
    n4 = x[3][14],x[3][2],x[3][3]
    n5 = x[4][14],x[4][2],x[4][3]
    n6 = x[5][14],x[5][2],x[5][3]
    n7 = x[6][14],x[6][2],x[6][3]
    n8 = x[7][14],x[7][2],x[7][3]
    n9 = x[8][14],x[8][2],x[8][3]
    n10 = x[9][14],x[9][2],x[9][3]
    p1 = n1[1]
    p1 = p1[:6]
    p2 = n2[1]
    p2 = p2[:6]
    p3 = n3[1]
    p3 = p3[:6]
    p4 = n4[1]
    p4 = p4[:6]
    p5 = n5[1]
    p5 = p5[:6]
    p6 = n6[1]
    p6 = p6[:6]
    p7 = n7[1]
    p7 = p7[:6]
    p8 = n8[1]
    p8 = p8[:6]
    p9 = n9[1]
    p9 = p9[:6]
    p10 = n10[1]
    p10 = p10[:6]
    update.message.reply_text('''
    Top 10 Writers of running nodes
    
n1 Count={}Public={} Country={}
n2 Count={}Public={} Country={}
n3 Count={}Public={} Country={}
n4 Count={}Public={} Country={}
n5 Count={}Public={} Country={}
n6 Count={}Public={} Country={}
n7 Count={}Public={} Country={}
n8 Count={}Public={} Country={}
n9 Count={}Public={} Country={}
n10 Count={}Public={} Country={}
    '''.format(n1[0],p1 , n1[2], n2[0],p2 , n2[2], n3[0], p3, n3[2], n4[0], p4, n4[2], n5[0], p5, n5[2], n6[0], p6, n6[2], n7[0], p7, n7[2], n8[0], p8, n8[2], n9[0], p9, n9[2], n10[0], p10, n10[2]))

    
def top10last24h(update, context):
    x = HismoduleSQL.fetch_trust_ratio_top()
    n1 = x[0][5],x[0][2],x[0][3]
    n2 = x[1][5],x[1][2],x[1][3]
    n3 = x[2][5],x[2][2],x[2][3]
    n4 = x[3][5],x[3][2],x[3][3]
    n5 = x[4][5],x[4][2],x[4][3]
    n6 = x[5][5],x[5][2],x[5][3]
    n7 = x[6][5],x[6][2],x[6][3]
    n8 = x[7][5],x[7][2],x[7][3]
    n9 = x[8][5],x[8][2],x[8][3]
    n10 = x[9][5],x[9][2],x[9][3]
    p1 = n1[1]
    p1 = p1[:6]
    p2 = n2[1]
    p2 = p2[:6]
    p3 = n3[1]
    p3 = p3[:6]
    p4 = n4[1]
    p4 = p4[:6]
    p5 = n5[1]
    p5 = p5[:6]
    p6 = n6[1]
    p6 = p6[:6]
    p7 = n7[1]
    p7 = p7[:6]
    p8 = n8[1]
    p8 = p8[:6]
    p9 = n9[1]
    p9 = p9[:6]
    p10 = n10[1]
    p10 = p10[:6]
    update.message.reply_text('''
    Top 10 performing nodes last 24H
    
n1 Count={}Public={} Country={}
n2 Count={}Public={} Country={}
n3 Count={}Public={} Country={}
n4 Count={}Public={} Country={}
n5 Count={}Public={} Country={}
n6 Count={}Public={} Country={}
n7 Count={}Public={} Country={}
n8 Count={}Public={} Country={}
n9 Count={}Public={} Country={}
n10 Count={}Public={} Country={}
    '''.format(n1[0],p1 , n1[2], n2[0],p2 , n2[2], n3[0], p3, n3[2], n4[0], p4, n4[2], n5[0], p5, n5[2], n6[0], p6, n6[2], n7[0], p7, n7[2], n8[0], p8, n8[2], n9[0], p9, n9[2], n10[0], p10, n10[2]))
    
def top10last24hstake(update, context):
    x = HismoduleSQL.fetch_trust_ratio_top()
    n1 = x[0][5],x[0][2],x[0][3]
    n2 = x[1][5],x[1][2],x[1][3]
    n3 = x[2][5],x[2][2],x[2][3]
    n4 = x[3][5],x[3][2],x[3][3]
    n5 = x[4][5],x[4][2],x[4][3]
    n6 = x[5][5],x[5][2],x[5][3]
    n7 = x[6][5],x[6][2],x[6][3]
    n8 = x[7][5],x[7][2],x[7][3]
    n9 = x[8][5],x[8][2],x[8][3]
    n10 = x[9][5],x[9][2],x[9][3]
    p1 = n1[1]
    p1_balance = nodeinformation.balance_get(p1)
    p1 = p1[:6]
    p2 = n2[1]
    p2_balance = nodeinformation.balance_get(p2)
    p2 = p2[:6]
    p3 = n3[1]
    p3_balance = nodeinformation.balance_get(p3)
    p3 = p3[:6]
    p4 = n4[1]
    p4_balance = nodeinformation.balance_get(p4)
    p4 = p4[:6]
    p5 = n5[1]
    p5_balance = nodeinformation.balance_get(p5)
    p5 = p5[:6]
    p6 = n6[1]
    p6_balance = nodeinformation.balance_get(p6)
    p6 = p6[:6]
    p7 = n7[1]
    p7_balance = nodeinformation.balance_get(p7)
    p7 = p7[:6]
    p8 = n8[1]
    p8_balance = nodeinformation.balance_get(p8)
    p8 = p8[:6]
    p9 = n9[1]
    p9_balance = nodeinformation.balance_get(p9)
    p9 = p9[:6]
    p10 = n10[1]
    p10_balance = nodeinformation.balance_get(p10)
    p10 = p10[:6]
    update.message.reply_text('''
    Top 10 performing nodes last 24H
    
n1 Count={} Public={} Country={} 
Staked={}
n2 Count={} Public={} Country={} 
Staked={}
n3 Count={} Public={} Country={} 
Staked={}
n4 Count={} Public={} Country={} 
Staked={}
n5 Count={} Public={} Country={} 
Staked={}
n6 Count={} Public={} Country={} 
Staked={}
n7 Count={} Public={} Country={} 
Staked={}
n8 Count={} Public={} Country={} 
Staked={}
n9 Count={} Public={} Country={} 
Staked={}
n10 Count={} Public={} Country={} 
Staked={}
    '''.format(n1[0], p1, n1[2], p1_balance, n2[0], p2, n2[2], p2_balance, n3[0], p3, n3[2], p3_balance, n4[0], p4, n4[2], p4_balance, n5[0], p5, n5[2], p5_balance, n6[0], p6, n6[2], p6_balance, n7[0], p7, n7[2], p7_balance, n8[0], p8, n8[2], p8_balance, n9[0], p9, n9[2], p9_balance, n10[0], p10, n10[2], p10_balance))
        
#-------------------------=hourly=------------------
def hour_off(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[9:]
    value = False
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
        bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:    
        MainmoduleSQL.updatehour(userid,value,returnkey2)
        bot.send_message(chat_id=chatiddebug, text="Hourly stats turned off for {}".format(returnkey2))
        bot.send_message(chat_id=userid, text="Hourly stats turned off for : {}".format(returnkey2))

def activate_hour(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[5:]
    value = True
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
        bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:    
        MainmoduleSQL.updatehour(userid,value,returnkey2)
        bot.send_message(chat_id=chatiddebug, text="Hourly stats turned on for {}".format(returnkey2))
        bot.send_message(chat_id=userid, text="Hourly stats turned on for : {}".format(returnkey2))

def hour_on(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    returnkey2 = update.message.text[8:]
    checkup = nodeinformation.getnodeinformation(returnkey2)
    if checkup[0] == None:
         bot.send_message(chat_id=userid, text="This key seems to be non exisiting on the SWT platform")
    else:
        MainmoduleSQL.Addhourkey(returnkey2,userid)
        if MainmoduleSQL.userdatafound == False:
            bot.send_message(chat_id=chatiddebug, text="Hourly stats turned on for {}".format(returnkey2))
            bot.send_message(chat_id=userid, text="Hourly stats turned on for this chat with this key {}".format(returnkey2))
        if MainmoduleSQL.userdatafound == True:
            bot.send_message(chat_id=userid, text="The key {} is already added to the private notifications for turning this key on type /hon with key".format(returnkey2,returnkey2))

def public_hour(chatid,returnkey):
    
    if debugtelegram:
        bot.send_message(chat_id=chatiddev, text="Automatic message send ")

    node_lastcount = HismoduleSQL.checklasttrust(returnkey,True,1,0)
    public_key = returnkey
    last_fee = node_lastcount[1]
    last_trust = node_lastcount[0]

    bot.send_message(chat_id=chatid,text=('''
Automatic hour message
Public key: {}
Trust count last 1H: {}
Total fee last 1H {}
    '''.format(public_key,last_trust,last_fee)))

def my_nodes(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    count = 1
    bot.send_message(chat_id=chatiddev, text="Mynodes requested")
    user_data = MainmoduleSQL.fetch_user_nodes(userid)
    for a in user_data:
        update.message.reply_text("""
    Node number{} 
{}       
        """.format(count, a[1]))
        count = count + 1

def my_nodestats(update, context):
    uservar = update.message.from_user
    userid = uservar["id"]
    bot.send_message(chat_id=chatiddev, text="Mynodes requested")
    swthourmodule.singlesend(userid)

#--------------------------------------------------

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True,request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("bestnode", bestnode))
    dp.add_handler(CommandHandler("onlinenode", onlinenode))
    dp.add_handler(CommandHandler("offlinenode", offlinenode))
    dp.add_handler(CommandHandler("worstnode", worstnode))
    dp.add_handler(CommandHandler("public", public))
    dp.add_handler(CommandHandler("totalnodes", totalnode))
    dp.add_handler(CommandHandler("lastblock", latestblock))
    dp.add_handler(CommandHandler("release", release))
    dp.add_handler(CommandHandler("notion", notion))
    dp.add_handler(CommandHandler("notioff", notioff))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("debug", debug3))
    dp.add_handler(CommandHandler("onehour", onehour))
    dp.add_handler(CommandHandler("10min", tenmin))
    dp.add_handler(CommandHandler("30min", thirtymin))
    dp.add_handler(CommandHandler("top10alltrust", top10AllTrust))
    dp.add_handler(CommandHandler("top10allwritten", top10AllWritten))
    dp.add_handler(CommandHandler("top10last24h", top10last24h))
    dp.add_handler(CommandHandler("top10last24hstake", top10last24hstake))
    dp.add_handler(CommandHandler("houron", hour_on))
    dp.add_handler(CommandHandler("houroff", hour_off))
    dp.add_handler(CommandHandler("hon", activate_hour))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("mynodes", my_nodes))
    dp.add_handler(CommandHandler("mynodestats", my_nodestats))
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    
    

    

    

    # Start the Bot
    updater.start_polling()

  


    bot.send_message(chat_id=chatid, text="System booting up")
    
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()
 
