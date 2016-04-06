#coding: utf-8
from __future__ import division
import sys
import string
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import httplib
import os
reload(sys) 
sys.setdefaultencoding('utf-8')
httpClient = None

host,port = "10.239.93.157",9900

def SendEmail(msgTo,deviceid,releaseid,jobid):
    msg = MIMEMultipart()
    msg['From'] = 'zhaowangx.liang@intel.com'
    msg['To'] = msgTo
    msg['Cc'] = 'zhaowangx.liang@intel.com'
    reportfilename,msg['Subject'],content = GetMailContent(deviceid,releaseid,jobid)
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    try:
        smtp = smtplib.SMTP('OutlookSH.intel.com', 25)
        smtp.starttls()
        smtp.login(msg['From'], 'lzw,123,9')
        smtp.sendmail('zhaowangx.liang@intel.com', msg['To'].split(','), msg.as_string())
    except Exception,e:
        print e

def SendEmailByMutt(msgTo,deviceid,releaseid,jobid):
    reportfilename,title,content = GetMailContent(deviceid,releaseid,jobid)
    file_object = open("../WebPortal/src/website/templates/static/historyreports/"+reportfilename,'w')
    file_object.write(content)
    file_object.close( )
    os.system('mutt -s "%s" -e "my_hdr content-type:text/html" %s < ../WebPortal/src/website/templates/static/historyreports/%s' % (title,msgTo,reportfilename))
    
def GetMailContent(deviceid,releaseid,jobid):
    httpClient = httplib.HTTPConnection(host, port, timeout=30)
    httpClient.request('GET', '/rest/gettestresultsummary?deviceid='+deviceid+'&releaseid='+releaseid+'&jobid='+jobid)
    response = httpClient.getresponse()
    if response.status == 200:
        records = json.loads(response.read())["result"]
        if len(records) > 0:
            #subject = "[Test] [%s] %s PnP Test Report" % (records[0][13],records[0][11])
            reportfilename = records[0][13].replace(' ','') + "_" + records[0][11] + "_" + jobid + ".html"
            subject = "Pnp Regression Control Report --- [" + records[0][13] + "] " + records[0][11]
            content_p1 = "<html><head></head><body><p><b>PnP Regression Contol Report on "+records[0][13]+" with "+records[0][11]+" image</b></p>"
            content_p2 = "<b>Regression Control Result (device viewpoint) Dashboard:</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;Summary Report: http://10.239.93.157:9900/kpireleaseview<br/><br/>"
            content_p3 = "<b>Test Objective:</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;To control the PnP KPI regression status on " + records[0][13] + "<br/><br/>"
            content_p4 = "<ul><li style='list-style-type:none;margin-left: -50px;margin-bottom:5px;'><b>Build Image:</b></li><li>Image version: " + records[0][11] + "</li><li>BIOS version: " + records[0][11] + "</li><li>Previous Image version: " + records[0][18] + "</li></ul>"
            content_p6 = "<b>Regression Control Summary:</b>"
            total = len(records)
            prePassed = 0;
            curPassed = 0;
            curRegression = 0;
            preRegressionPass = 0;
            preRegressionFail = 0;
            curRegressionPass = 0;
            curRegressionFail = 0;
            regPassToFail = 0;
            regFailToPass = 0;
            preExist = 1;
            failedkpi = []
            regressionkpi = []
            improvementkpi = []
            for record in records:
                target = string.atof(record[2])
                margin = string.atof(record[3])
                tth1 = string.atof(record[4])
                tth2 = string.atof(record[5])
                cur = string.atof(record[7])
                pre = string.atof(record[8])
                
                if str(record[9]) == "1":
                    if margin != 0 and target != 0 and (target-cur)/target <= margin:
                        curPassed += 1
                    elif margin != 0 and target != 0:
                        failedkpi.append(record)
                    if pre != 0:
                        preExist = 1;
                        if margin != 0 and target != 0 and (target-pre)/target <= margin:
                            prePassed += 1

                        if tth2 != 0 and (pre-cur)/pre > tth2:
                            curRegression += 1
                            regressionkpi.append(record)
                        elif tth1 != 0 and (pre-cur)/pre < -tth1:
                            improvementkpi.append(record)
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-pre)/target <= margin:
                            preRegressionPass += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-pre)/target > margin:
                            preRegressionFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-cur)/target > margin:
                            curRegressionFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-cur)/target <= margin:
                            curRegressionPass += 1
                        
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-pre)/target <= margin and (target-cur)/target > margin:
                            regPassToFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (pre-cur)/pre > tth2 and (target-pre)/target > margin and (target-cur)/target <= margin:
                            regFailToPass += 1
                    else:
                        preExist = 0;
                else:
                    if margin != 0 and target != 0 and (cur-target)/cur <= margin:
                        curPassed += 1
                    elif margin != 0 and target != 0:
                        failedkpi.append(record)
                    if pre != 0:
                        preExist = 1;
                        if margin != 0 and target != 0 and (pre-target)/pre <= margin:
                            prePassed += 1
                    
                        if tth2 != 0 and (cur-pre)/cur > tth2:
                            curRegression += 1
                            regressionkpi.append(record)
                        elif tth1 != 0 and (cur-pre)/cur < -tth1:
                            improvementkpi.append(record)
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (pre-target)/pre <= margin:
                            preRegressionPass += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (pre-target)/pre > margin:
                            preRegressionFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (cur-target)/cur > margin:
                            curRegressionFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (cur-target)/cur <= margin:
                            curRegressionPass += 1
                            
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (pre-target)/pre <= margin <= margin and (cur-target)/cur > margin:
                            regPassToFail += 1
                        if margin != 0 and target != 0 and tth2 != 0 and (cur-pre)/cur > tth2 and (pre-target)/pre > margin and (cur-target)/cur <= margin:
                            regFailToPass += 1
                    else:
                        preExist = 0;
            content_p7 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:800px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td style='font-size:12pt;background-color:#3CB371;color:white;font-weight:bold;height:26px;width:180px;'>Pass Status</td></tr><tr style='background-color:#43CD80;height:22px;'><th></th><th>Previous Release</th><th>Current Release</th><th>Pass fluctuation</th></tr>"
            if records[0][12] == "performance":
                content_p7 += "<tr style='height:24px;'><td>Power</td><td>0/0</td><td>0/0</td><td>0</td></tr><tr style='height:24px;'><td>Performace</td><td>%s/%s(%s)</td><td>%s/%s(%s)</td><td>%s(%s)</td></tr>" % (str(prePassed),str(total),str(round(prePassed/total,4)*100)+"%",str(curPassed),str(total),str(round(curPassed/total,4)*100)+"%",str(curPassed-prePassed),str(round((curPassed-prePassed)/total,4)*100)+"%")
            else:
                content_p7 += "<tr style='height:24px;'><td>Power</td><td>%s/%s(%s)</td><td>%s/%s(%s)</td><td>%s(%s)</td></tr><tr style='height:30px;'><td>Performace</td><td>0/0</td><td>0/0</td><td>0</td></tr>" % (str(prePassed),str(total),str(round(prePassed/total,4)*100)+"%",str(curPassed),str(total),str(round(curPassed/total,4)*100)+"%",str(curPassed-prePassed),str(round((curPassed-prePassed)/total,4)*100)+"%")
            content_p7 += "<tr style='height:24px;'><td>Total PnP</td><td>%s/%s(%s)</td><td>%s/%s(%s)</td><td>%s(%s)</td></tr></table><br/>" % (str(prePassed),str(total),str(round(prePassed/total,4)*100)+"%",str(curPassed),str(total),str(round(curPassed/total,4)*100)+"%",str(curPassed-prePassed),str(round((curPassed-prePassed)/total,4)*100)+"%")
            content_p8 = "Previous release test result is not exist!" if preExist == 0 else ""
            content_p9 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:800px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td cols=5 style='font-size:12pt;background-color:#3CB371;color:white;font-weight:bold;height:26px;width:180px;'>Improvement Status</td><td colspan=4 style='text-align:left;border-right:none;border-top:none;color:red;'>"+content_p8+"</td></tr><tr style='background-color:#43CD80;height:26px;'><th></th><th>Current Regression</th><th>Pass</th><th>Pass To Fail</th><th>Fail</th></tr>"
            if records[0][12] == "performance":
                content_p9 += "<tr style='height:24px;'><td>Power</td><td>0/0</td><td>0/0</td><td>0/0</td><td>0/0</td></tr><tr style='height:24px;'><td>Performace</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionPass),str(curRegression),str(regPassToFail),str(curRegression),str(curRegressionFail),str(curRegression))
            else:
                content_p9 += "<tr style='height:24px;'><td>Power</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr><tr><td>Performace</td><td>0/0</td><td>0/0</td><td>0/0</td><td>0/0</td></tr>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionPass),str(curRegression),str(regPassToFail),str(curRegression),str(curRegressionFail),str(curRegression))
            content_p9 += "<tr style='height:24px;'><td>Total PnP</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr></table><br/>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionPass),str(curRegression),str(regPassToFail),str(curRegression),str(curRegressionFail),str(curRegression))
            content_p10 = ""
            content_p11 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:800px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td style='font-size:12pt;background-color:#EE0000;color:white;font-weight:bold;height:26px;width:180px;'>Worse Status</td><td colspan=4 style='text-align:left;border-right:none;border-top:none;color:red;'>"+content_p8+"</td></tr><tr style='background-color:#F08080;height:26px;'><th></th><th>Current Regression</th><th>Fail</th><th>Fail To Pass</th><th>Pass</th></tr>"
            if records[0][12] == "performance":
                content_p11 += "<tr style='height:24px;'><td>Power</td><td>0/0</td><td>0/0</td><td>0/0</td><td>0/0</td></tr><tr style='height:24px;'><td>Performace</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionFail),str(curRegression),str(regFailToPass),str(curRegression),str(curRegressionPass),str(curRegression))
            else:
                content_p11 += "<tr style='height:24px;'><td>Power</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr><tr style='height:24px;'><td>Performace</td><td>0/0</td><td>0/0</td><td>0/0</td><td>0/0</td></tr>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionFail),str(curRegression),str(regFailToPass),str(curRegression),str(curRegressionPass),str(curRegression))
            content_p11 += "<tr style='height:24px;'><td>Total PnP</td><td>%s/%s(%s)</td><td>%s/%s</td><td>%s/%s</td><td>%s/%s</td></tr></table><br/><br/>" % (str(curRegression),str(total),str(round(curRegression/total,4)*100)+"%",str(preRegressionFail),str(curRegression),str(regFailToPass),str(curRegression),str(curRegressionPass),str(curRegression))
            
            content_p12 = "<b>Details:</b>"
            content_p13 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:1340px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td cols=11 style='font-size:12pt;background-color:#EE0000;color:white;font-weight:bold;height:26px;width:180px;'>" + str(len(failedkpi)) + " Failed KPI</td></tr><tr style='background-color:#F08080;height:26px;'><th></th><th style='width:100px;'>Component/s</th><th style='width:100px;'>Key</th><th style='width:400px;'>Summary</th><th style='width:80px;'>Priority</th><th style='width:80px;'>Unit</th><th style='width:80px;'>Target</th><th style='width:80px;'>Margin</th><th style='width:80px;'>Previous</th><th style='width:80px;'>Current</th><th style='width:80px;'>RSD</th></tr>"
            for tr in failedkpi:
                domain = tr[1].split('#')[0] if len(tr[1].split('#')) > 2 else ""
                component = tr[1].split('#')[1] if len(tr[1].split('#')) > 2 else ""
                summary = tr[1].split('#')[2] if len(tr[1].split('#')) > 2 else ""
                key = tr[14].split('/')[-1] if len(tr[14].split('/')) > 0 else ""
                results = getSourceResult(deviceid,releaseid,str(tr[0]),jobid)
                rsd = str(round(stdev(results)/avg(results),4)*100) + "%"
                target = string.atof(tr[2])
                margin = string.atof(tr[3])
                pre = string.atof(tr[8])
                bc = ""
                if pre != 0:
                    bc = "green"
                    if str(tr[9]) == "1":
                        if (target-pre)/target > margin:
                            bc = "red"
                    else:
                        if (pre-target)/pre > margin:
                            bc = "red"
                content_p13 += "<tr style='height:24px;'><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td><a href='%s'>%s<a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style='background-color:%s;'>%s</td><td style='background-color:red;'>%s</td><td>%s</td></tr>" % (domain,component,tr[14],key,tr[15],summary,tr[16],tr[17],tr[2],str(string.atof(tr[3])*100)+"%",bc,tr[8],tr[7],rsd)
            content_p13 += "</table><br/>"
            
            content_p14 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:1420px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td cols=12 style='font-size:12pt;background-color:#EE0000;color:white;font-weight:bold;height:26px;width:180px;'>" + str(len(regressionkpi)) + " Worse KPI</td><td colspan=11 style='text-align:left;border-right:none;border-top:none;color:red;'>"+content_p8+"</td></tr><tr style='background-color:#F08080;height:26px;'><th></th><th style='width:100px;'>Component/s</th><th style='width:100px;'>Key</th><th style='width:400px;'>Summary</th><th style='width:80px;'>Priority</th><th style='width:80px;'>Unit</th><th style='width:80px;'>Target</th><th style='width:80px;'>Margin</th><th style='width:80px;'>Previous</th><th style='width:100px;'>Current</th><th style='width:80px;'>RSD</th><th style='width:80px;'>Regression</th></tr>"
            for tr in regressionkpi:
                domain = tr[1].split('#')[0] if len(tr[1].split('#')) > 2 else ""
                component = tr[1].split('#')[1] if len(tr[1].split('#')) > 2 else ""
                summary = tr[1].split('#')[2] if len(tr[1].split('#')) > 2 else ""
                key = tr[14].split('/')[-1] if len(tr[14].split('/')) > 0 else ""
                results = getSourceResult(deviceid,releaseid,str(tr[0]),jobid)
                rsd = str(round(stdev(results)/avg(results),4)*100) + "%"
                target = string.atof(tr[2])
                margin = string.atof(tr[3])
                cur = string.atof(tr[7])
                pre = string.atof(tr[8])
                reg = (pre-cur)/pre if str(tr[9]) == "1" else (cur-pre)/cur
                cur_bc = "green"
                pre_bc = "green"                
                if target == 0 or margin == 0:
                    cur_bc = ""
                    pre_bc = ""
                else:
                    if str(tr[9]) == "1":
                        if (target-cur)/target > margin:
                            cur_bc = "red"
                        if (target-pre)/target > margin:
                            pre_bc = "red"
                    else:
                        if (cur-target)/cur > margin:
                            cur_bc = "red"
                        if (pre-target)/pre > margin:
                            pre_bc = "red"
                content_p14 += "<tr style='height:24px;'><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td><a href='%s'>%s<a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style='background-color:%s;'>%s</td><td style='background-color:%s;'>%s</td><td>%s</td><td style='background-color:red;'>%s</td></tr>" % (domain,component,tr[14],key,tr[15],summary,tr[16],tr[17],tr[2],str(string.atof(tr[3])*100)+"%",pre_bc,tr[8],cur_bc,tr[7],rsd,str(round(reg,4)*100)+"%")
            content_p14 += "</table><br/>"
            content_p15 = "<table cellspacing=0 cellpadding=2 border='1' style='margin-left:20px;width:1420px;border-collapse:collapse;font-size:10pt;text-align:center;'><tr><td cols=12 style='font-size:12pt;background-color:#3CB371;color:white;font-weight:bold;height:26px;width:180px'>" + str(len(improvementkpi)) + " Improvement KPI</td><td colspan=11 style='text-align:left;border-right:none;border-top:none;color:red;'>"+content_p8+"</td></tr><tr style='background-color:#43CD80;height:26px;'><th></th><th style='width:100px;'>Component/s</th><th style='width:100px;'>Key</th><th style='width:400px;'>Summary</th><th style='width:80px;'>Priority</th><th style='width:80px;'>Unit</th><th style='width:80px;'>Target</th><th style='width:80px;'>Margin</th><th style='width:80px;'>Previous</th><th style='width:80px;'>Current</th><th style='width:80px;'>RSD</th><th style='width:80px;'>Regression</th></tr>"
            for tr in improvementkpi:
                domain = tr[1].split('#')[0] if len(tr[1].split('#')) > 2 else ""
                component = tr[1].split('#')[1] if len(tr[1].split('#')) > 2 else ""
                summary = tr[1].split('#')[2] if len(tr[1].split('#')) > 2 else ""
                key = tr[14].split('/')[-1] if len(tr[14].split('/')) > 0 else ""
                results = getSourceResult(deviceid,releaseid,str(tr[0]),jobid)
                rsd = str(round(stdev(results)/avg(results),4)*100) + "%"
                target = string.atof(tr[2])
                margin = string.atof(tr[3])
                cur = string.atof(tr[7])
                pre = string.atof(tr[8])
                reg = (pre-cur)/pre if str(tr[9]) == "1" else (cur-pre)/cur
                cur_bc = "green"
                pre_bc = "green"

                if target == 0 or margin == 0:
                    cur_bc = ""
                    pre_bc = ""
                else:
                    if str(tr[9]) == "1":
                        if (target-cur)/target > margin:
                            cur_bc = "red"
                        if (target-pre)/target > margin:
                            pre_bc = "red"
                    else:
                        if (cur-target)/cur > margin:
                            cur_bc = "red"
                        if (pre-target)/pre > margin:
                            pre_bc = "red"
                
                content_p15 += "<tr style='height:30px;'><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td><a href='%s'>%s<a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td style='background-color:%s;'>%s</td><td style='background-color:%s;'>%s</td><td>%s</td><td style='background-color:green;'>%s</td></tr>" % (domain,component,tr[14],key,tr[15],summary,tr[16],tr[17],tr[2],str(string.atof(tr[3])*100)+"%",pre_bc,tr[8],cur_bc,tr[7],rsd,str(round(reg,4)*100)+"%")
            content_p15 += "</table><br/>"
            
            content_p16 = "<b>Other info:</b><br/>&nbsp;&nbsp;&nbsp;&nbsp;For more details please refer to attached sheets. The measurement data also can be checked on <a href='http://10.239.93.157:9900/kpireleaseview'>PnP Regression Control Home</a>"
            content_p17 = "<br/><br/>------------------------------------------<br/><font style='font-size:10pt;'><i>This is an auto email sent by <b>Android PnP KPI Regression Control and Analysis Framework.</b><br/>Any question please contact Lou, Guoxian guoxian.lou@intel.com; sun, xiaoye xiaoye.sun@intel.com; Liang, ZhaowangX zhaowangx.liang@intel.com<br/>SSG>OTC>Android PnP Team</i></font><br/></body></html>"
            
            htmlContent = content_p1 + content_p2 + content_p3 + content_p4 + content_p6 + content_p7 + content_p8 + content_p9 + content_p10 + content_p11 + content_p12 + content_p13 + content_p15 + content_p14 + content_p16 + content_p17
            return reportfilename,subject,htmlContent
def getSourceResult(deviceid,releaseid,kpiid,jobid):
    result = []
    httpClient = httplib.HTTPConnection(host, port, timeout=30)
    httpClient.request('GET', '/rest/getsourceresult?deviceid='+deviceid+'&releaseid='+releaseid+'&kpiid='+kpiid+'&jobid='+jobid)
    response = httpClient.getresponse()
    if response.status == 200:
        records = json.loads(response.read())["result"]
        if len(records) > 0:
            for record in records:
                result.append(string.atof(record[0]))
    return result
def avg(list):
    if len(list) < 1:
        return None
    else:
        return sum(list) / len(list)
def stdev(list):
    if len(list) < 1:
        return None
    else:
        sdsq = sum([(i - avg(list)) ** 2 for i in list])
        stdev = (sdsq / (len(list) - 1)) ** .5
        return stdev
        
if __name__=="__main__":
    #SendEmail("zhaowangx.liang@intel.com","6","172","19807")
    SendEmailByMutt("zhaowangx.liang@intel.com","1","183","19938")