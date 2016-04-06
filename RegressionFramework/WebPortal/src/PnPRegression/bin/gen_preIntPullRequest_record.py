'''
Created on Dec 10, 2014

@author: liangzw
'''
import sys
import os
import time
import httplib
import urllib
import json

httpClient = None
datafile=sys.argv[1]
devicename=sys.argv[2]
imagefolder=sys.argv[3]
releaseid=sys.argv[4]
localpath=sys.argv[5]
host,port = '10.239.93.157', 9900
def getPreIntPulReq():
    result = {}
    f = open(datafile, 'r')
    for line in f.readlines():
        key = line.split(" ")[1].replace('\n','')
        value = line.split(" ")[0]
        if key != "NONE":
            if result.has_key(key):
                result[key].append(value)
            else:
                result[key] = [value]
    return result
    
def savePreIntPulReqData():
    dataList = getPreIntPulReq()
    params = urllib.urlencode(dataList)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    httpClient = httplib.HTTPConnection(host,port, timeout=30)
    httpClient.request("POST","/rest/addnewpreimgpullreq?devicename="+devicename+"&imagefolder="+imagefolder+"&releaseid="+releaseid+"&localpath="+localpath, params, headers)
    response = httpClient.getresponse()
    if response.status == 200:
        print "preintegration and pull request data insert successfull."

if __name__ == '__main__':
    print savePreIntPulReqData()