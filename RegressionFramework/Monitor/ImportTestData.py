#coding=utf8
import httplib
import urllib
import json
import datetime
import time
import os
import re
import logging
httpClient = None
atsStatus = {"PENDING":"1","DEPLOYED":"1", "INSTALL":"1", "TESTING":"2", "DONE":"4", "ABORT":"3", "TIMEOUT":"3", "CANCELLED":"3", "EXIT":"3"}

def start():
    ats = parseAtsResult(os.popen('python ats.py -s 17057','r').read())
    print ats

def parseAtsResult(result):
    r = {}
    status = (re.compile('<-----(\w+)----->')).findall(result)[0]
    sum = len((re.compile('.+\s+100%',re.M)).findall(result))
    nousenum = len((re.compile('(Image_Flash|Setup_Wizard|Mount_LKP|test_env|Retrieve_Log|Notify_LKP|REBOOT_DEVICE)\s+100%',re.M)).findall(result))
    r["status"] = status
    print sum
    print nousenum
    r["completenum"] = sum-nousenum
    return r
if __name__ == "__main__":
    start()