#coding=utf8
import httplib
import urllib
import json
import datetime
import time
import os
import re
import logging
import AutoMail
import AutoRunBisect
httpClient = None
atsStatus = {"PENDING":"1","DEPLOYED":"1", "INSTALL":"1", "TESTING":"2", "DONE":"4", "ABORT":"3", "TIMEOUT":"3", "CANCELLED":"3", "EXIT":"3"}
curPath = os.path.split(os.path.realpath(__file__))[0]

def start():
    logging.basicConfig(filename='/home/liangzw/work/LKPServer/ImportInfo.log',filemode='w',level=logging.DEBUG)
    try:
        httpClient = httplib.HTTPConnection('10.239.93.157', 9900, timeout=30)
        httpClient.request('GET', '/rest/getkpilist')
        response = httpClient.getresponse()
        kpis = json.loads(response.read())["result"]
        kpilist = {}
        for kpi in kpis:
            kpilist[kpi[1]] = kpi[0]

        httpClient.request('GET', '/rest/getrecipemonitor')
        response = httpClient.getresponse()
        if response.status == 200:
            rms = json.loads(response.read())["result"]
            for rm in rms:
                httpClient.request('GET', '/rest/getrecipemonitor?jobid='+rm[4])
                response = httpClient.getresponse()
                logging.info("---------start: Time = "+str(datetime.datetime.now())+" job id = " + rm[4] + "------------")
                ats = parseAtsResult(os.popen('python '+ curPath +'/autotestservice-1.4.py -s '+rm[4],'r').read())
                print ats
                httpClient.request('GET', '/rest/getrunstatus?runid='+str(rm[3])+'&statusid='+atsStatus[ats["status"]])
                response = httpClient.getresponse()
                if response.status == 200:
                    result = json.loads(response.read())["result"]
                    if str(result[0][0]) == "0":
                        logging.info("add status:" + atsStatus[ats["status"]])
                        httpClient.request('GET', '/rest/addrunstatus?runid='+str(rm[3])+'&statusid='+atsStatus[ats["status"]]+'&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                    elif atsStatus[ats["status"]]=="2":
                        logging.info("update status:" + atsStatus[ats["status"]])
                        httpClient.request('GET', '/rest/updaterunstatus?runid='+str(rm[3])+'&statusid='+atsStatus[ats["status"]]+'&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                
                httpClient.request('GET', '/rest/updatetaskrunstatus?rid='+str(rm[3])+'&status='+str(atsStatus[ats["status"]])+'&completekpinum='+str(ats["completenum"]))
                response = httpClient.getresponse()

                if(atsStatus[ats["status"]]=="4"):
                    httpClient.request('GET', '/rest/gettestdata?jobid='+rm[4])
                    response = httpClient.getresponse()
                    faileCount = 0
                    if response.status == 200:
                        time.sleep(1)
                        logging.info("get test data")
                        httpClient.request('GET', '/rest/gettestdata?jobid='+rm[4])
                        response = httpClient.getresponse()
                        results = json.loads(response.read())["result"]
                        for result in results:
                            if kpilist.has_key(result[0]):
                                releaseid = str(rm[1])
                                deviceid = str(rm[2])
                                kpiid = str(kpilist[result[0]])
                                jobid = rm[4]
                                remark = "http://10.239.97.26/automation-logs/" + rm[4] + "/cti-master.sh.intel.com_" + rm[4] + "/" + result[0]
                                for score in json.loads(result[1]):
                                    print score
                                    params = urllib.urlencode({'deviceid':deviceid,'releaseid':releaseid,'kpiid':kpiid,'jobid':jobid,'remark':remark,'score':score,'datafrom':'1'})
                                    httpClient.request('GET', '/rest/savetestdata?' + params)
                                    response = httpClient.getresponse()
                                    if response.status != 200:
                                        faileCount += 1
                        httpClient.request('GET', '/rest/updaterecipemonitor?id='+str(rm[0])+'&failecount='+str(faileCount))
                        response = httpClient.getresponse()
                        httpClient.request('GET', '/rest/updatetaskrunstatus?rid='+str(rm[3])+'&status=6&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                        httpClient.request('GET', '/rest/addrunstatus?runid='+str(rm[3])+'&statusid=6&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                        
                        logging.info("get regression.")
                        httpClient.request('GET', '/rest/getregression?deviceid='+str(rm[2])+'&releaseid='+str(rm[1])+'&jobid='+str(rm[4])+'&plantaskrunid='+str(rm[3]))
                        response = httpClient.getresponse()
                        
                        logging.info("send email.")
                        logging.info(str(rm[2])+" "+str(rm[1])+" "+str(rm[4]))
                        AutoMail.SendEmailByMutt("otc.android.pnp.engineering.sh@intel.com,shaoyongx.a.niu@intel.com,zhaowangx.liang@intel.com",str(rm[2]),str(rm[1]),str(rm[4]))
                        
                        #logging.info("run bisect.")
                        #AutoRunBisect.RunBisect(str(rm[5]),str(rm[6]),str(rm[1]))
                    else:
                        httpClient.request('GET', '/rest/updatetaskrunstatus?rid='+str(rm[3])+'&status=5&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                        httpClient.request('GET', '/rest/addrunstatus?runid='+str(rm[3])+'&statusid=5&completekpinum='+str(ats["completenum"]))
                        response = httpClient.getresponse()
                        
                if(atsStatus[ats["status"]]=="3"):
                    httpClient.request('GET', '/rest/updaterecipemonitor?id='+str(rm[0])+'&failecount=0')
                    response = httpClient.getresponse()
                    
                logging.info("------------end Time = "+str(datetime.datetime.now())+"------------")
    except Exception, e:
        logging.error(e)
        logging.info("error!")
    finally:
        if httpClient:
            httpClient.close()

def parseAtsResult(result):
    print result
    r = {}
    status = (re.compile('<-----(\w+)----->')).findall(result)[0]
    sum = len((re.compile('.+\s+100%',re.M)).findall(result))
    nousenum = len((re.compile('(Image_Flash|Setup_Wizard|Mount_LKP|get_default_volume|test_env|Retrieve_Log|Notify_LKP|REBOOT_DEVICE)\s+100%',re.M)).findall(result))
    r["status"] = status
    r["completenum"] = sum-nousenum
    return r
if __name__ == "__main__":
    start()
