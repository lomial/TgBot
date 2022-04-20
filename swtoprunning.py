import logging,time
import MainmoduleSQL
import HismoduleSQL


def main():

    while True:
        HismoduleSQL.deletetop()
        for a in MainmoduleSQL.fetchrunning():
            time.sleep(0)
            trust_value = HismoduleSQL.checklasttrusttop(a[2],True,24,0)
            HismoduleSQL.singlewritetop(a,trust_value)
        time.sleep(900)        





