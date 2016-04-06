# -*- coding: utf-8 -*-
import sys
from django.shortcuts import render
from django.http import HttpResponse
import website.settings as settings
import string
import json
import datetime
import MySQLdb
import urllib2
from bs4 import BeautifulSoup
from warnings import filterwarnings
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')
filterwarnings('ignore', category = MySQLdb.Warning)

downloadImgsDevices = ['TREKSTOR','ECS210A','MALATA10']

def index(request):
    return HttpResponse("Hello,word!")

def GetKpiReleaseView(request):
    con = ""
    deviceid = 1 if request.GET.get("deviceid") == None else request.GET.get("deviceid")
    releasetype = request.GET.get("releasetype")
    domain = request.GET.get("domain")
    
    if releasetype != None and releasetype != "-1":
        con += " and b.releasetype_id="+releasetype
    if domain != None and domain != "-1":
        con += " and a.kpi_id in (select kpi_id from  BaseInfo_kpidomain where domain_id=%s)" % (str(domain))

    queryStr = """DROP TABLE IF EXISTS `tmp_result`;
                DROP TABLE IF EXISTS `tmp_result2`;
                Create temporary table tmp_result(
                    select a.release_id,a.kpi_id,c.summary,c.`key`,a.device_id,b.`name` "Releases",e.id pre_id,e.`name` Pre,c.testcasename,Concat(g.`name`,'*_*',c.showname,'*_*',f.`name`,'*_*',c.largeisbetter,'*_*',c.id,'*_*',ifnull(h.target,0),'*_*',ifnull(h.margin,0),'*_*',ifnull(h.regthrethold1,0),'*_*',ifnull(h.regthrethold2,0),'*_*',ifnull(h.regthrethold3,0)) KPI,d.`name` Device,avg(a.score) score,i.`comment` cmt,max(j.runindex) runindex from BaseInfo_testresult a 
                    left join BaseInfo_release b on a.release_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id left join BaseInfo_unit f on c.unit_id=f.id inner join BaseInfo_release e on b.pre_id=e.id 
                    left join BaseInfo_device d on a.device_id=d.id left join BaseInfo_kpitype g on c.kpitype_id=g.id  left join BaseInfo_target h on h.device_id=d.id and h.kpi_id=c.id
                    left join BaseInfo_testresultcomment i on a.device_id=i.device_id and a.release_id=i.release_id and a.kpi_id=i.kpi_id
                    left join BaseInfo_testresult j on a.device_id=j.device_id and a.release_id=j.release_id and a.kpi_id=j.kpi_id
                    where a.device_id=%s %s and a.runindex<3 group by device_id,kpi_id,release_id
                );
                set @sql1='Create temporary table tmp_result2(select release_id,device_id,summary,`key`,testcasename,KPI,pre_id';
                set @sql2='select summary,`key`,testcasename,KPI';
                select @sql1 := Concat(@sql1,', (case release_id when ',release_id,' then Concat(format(score,2),"*_*",',release_id,',"*_*",',pre_id,',"*_*",ifnull(cmt,"")',',"*_*",runindex) else 0 end) ' ,Releases ,', (case release_id when ',pre_id,' then Concat(format(score,2),"*_*",',pre_id,') else 0 end) Pre_' ,Releases),
                       @sql2 := Concat(@sql2,', max(' ,Releases ,') ',Releases,',max(Pre_' ,Releases ,') ',Releases,'_Pre')
                from (select distinct release_id,Releases,pre_id,Pre from tmp_result) a;
                select @sql1 := Concat(@sql1,' from tmp_result)');
                PREPARE stmt1 FROM @sql1;
                EXECUTE stmt1;
                select @sql2 := Concat(@sql2,' from tmp_result2 group by KPI');
                PREPARE stmt2 FROM @sql2;
                EXECUTE stmt2;""" % (deviceid,con)
    results = dbhandlebymultistr(queryStr)
    return HttpResponse(json.dumps({"viewdata":results}))

def GetKpiDeviceView(request):
    releaseid=13
    prereleaseid=12
    con = ""
    platform = request.GET.get("platform")
    domain = request.GET.get("domain")
    
    if platform != None and platform != "-1":
        con += " and d.platform_id="+platform
    if domain != None and domain != "-1":
        con += " and a.kpi_id in (select kpi_id from  BaseInfo_kpidomain where domain_id=%s)" % (str(domain))
        
    queryStr = """DROP TABLE IF EXISTS `tmp_result`;
                DROP TABLE IF EXISTS `tmp_result2`;
                Create temporary table tmp_result(
                    select a.kpi_id,a.device_id,b.`name` "Releases",c.testcasename,Concat(g.`name`,'*_*',c.showname,'*_*',f.`name`,'*_*',c.largeisbetter,'*_*',c.id) KPI,Concat(d.`name`,'*_*',release_id) Device,
                    Concat(format(avg(a.score),2),'*_*',ifnull(h.target,0),'*_*',ifnull(h.margin,0),'*_*',ifnull(h.regthrethold1,0),'*_*',ifnull(h.regthrethold2,0),'*_*',ifnull(h.regthrethold3,0)) score from BaseInfo_testresult a 
                    left join BaseInfo_release b on a.release_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id left join BaseInfo_device d on a.device_id=d.id 
                    left join BaseInfo_unit f on c.unit_id=f.id left join BaseInfo_kpitype g on c.kpitype_id=g.id left join BaseInfo_target h on h.device_id=d.id and h.kpi_id=c.id 
                    where a.release_id in(%s,%s) %s and a.release_id in(12,13)  group by kpi_id,device_id,release_id
                );
                set @sql1='Create temporary table tmp_result2(select device_id,testcasename,KPI';
                set @sql2='select device_id,testcasename,KPI';
                select @sql1 := Concat(@sql1,',(case Device when "',Device ,'" then score else 0 end) "' ,Device,'"'),
                             @sql2 := Concat(@sql2,', max(`' ,Device ,'`) "',Device,'"')
                from (select distinct device_id,Device from tmp_result) a;
                select @sql1 := Concat(@sql1,' from tmp_result)');
                PREPARE stmt1 FROM @sql1;
                EXECUTE stmt1;
                select @sql2 := Concat(@sql2,' from tmp_result2 group by KPI');
                PREPARE stmt2 FROM @sql2;
                EXECUTE stmt2;""" % (releaseid,prereleaseid,con)
    results = dbhandlebymultistr(queryStr)
    return HttpResponse(json.dumps({"viewdata":results}))

def GetDeviceReleaseView(request):
    kpiid=9
    con = ""
    releasetype = request.GET.get("releasetype")
    domain = request.GET.get("domain")
    
    if releasetype != None and releasetype != "-1":
        con += " and b.releasetype_id="+releasetype
    if domain != None and domain != "-1":
        con += " and a.kpi_id in (select kpi_id from  BaseInfo_kpidomain where domain_id=%s)" % (str(domain))
    
    platform = request.GET.get("platform")
    if platform != None and platform != "-1":
        con += " and d.platform_id="+platform
        
    queryStr = """DROP TABLE IF EXISTS `tmp_result`;
                DROP TABLE IF EXISTS `tmp_result2`;
                Create temporary table tmp_result(
                        select release_id,a.kpi_id,a.device_id,b.`name` "Releases",e.id pre_id,e.`name` Pre,Concat(d.`name`,'*_*',f.`name`,'*_*',c.largeisbetter,'*_*',ifnull(h.target,0),'*_*',ifnull(h.margin,0),'*_*',ifnull(h.regthrethold1,0),'*_*',ifnull(h.regthrethold2,0),'*_*',ifnull(h.regthrethold3,0)) Device,avg(a.score) score from BaseInfo_testresult a 
                        left join BaseInfo_release b on a.release_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id left join BaseInfo_unit f on c.unit_id=f.id inner join BaseInfo_release e on b.pre_id=e.id 
                        left join BaseInfo_device d on a.device_id=d.id left join BaseInfo_kpitype g on c.kpitype_id=g.id  left join BaseInfo_target h on h.device_id=d.id and h.kpi_id=c.id
                        where a.kpi_id=%s %s group by device_id,kpi_id,release_id
                );
                select * from tmp_result;
                set @sql1='Create temporary table tmp_result2(select release_id,pre_id,device_id,Device';
                set @sql2='select device_id,Device';
                select @sql1 := Concat(@sql1,', (case release_id when ',release_id,' then Concat(format(score,2),"*_*",',release_id,',"*_*",',pre_id,') else 0 end) ' ,Releases ,', (case release_id when ',pre_id,' then format(score,2) else 0 end) Pre_' ,Releases),
                             @sql2 := Concat(@sql2,', max(' ,Releases ,') ',Releases,',max(Pre_' ,Releases ,') ',Releases,'_Pre')
                from (select distinct release_id,Releases,pre_id,Pre from tmp_result) a;
                select @sql1 := Concat(@sql1,' from tmp_result)');
                PREPARE stmt1 FROM @sql1;
                EXECUTE stmt1;
                select * from tmp_result2;
                select @sql2 := Concat(@sql2,' from tmp_result2 group by device_id');
                PREPARE stmt2 FROM @sql2;
                EXECUTE stmt2;""" % (kpiid,con)
    results = dbhandlebymultistr(queryStr)
    return HttpResponse(json.dumps({"viewdata":results}))

def GetTestResultByJobid(request):
    jobid = request.GET.get("jobid")
    queryStr = "select a.id,format(score,2),device_id,kpi_id,release_id,datafrom_id,a.remark,b.`name`,d.testcasename,c.`name` from BaseInfo_testresult a left join BaseInfo_device b on a.device_id=b.id left join BaseInfo_release c on a.release_id=c.id left join BaseInfo_kpi d on a.kpi_id=d.id where jobid='%s' order by a.id desc;" % (jobid)  # isavailable=1 and
    resultList = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":resultList}))
    
def GetDomainList(request):
    queryStr = "select id,name from BaseInfo_domain"
    domainList = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":domainList}))
    
def GetPlatformList(request):
    queryStr = "select id,name from BaseInfo_platform"
    platformList = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":platformList}))
def GetDeviceTypeList(request):
    queryDevicetypeStr = "select id,name from BaseInfo_devicetype"
    deviceList = dbhandlebystr(queryDevicetypeStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetDeviceList(request):
    queryDeviceStr = "select a.id,a.name,b.name,c.name,remark,devicetype_id,platform_id from BaseInfo_device a left join BaseInfo_devicetype b on a.devicetype_id=b.id left join BaseInfo_platform c on a.platform_id=c.id"
    deviceList = dbhandlebystr(queryDeviceStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetDeviceListWithTarget(request):
    queryDeviceStr = "select a.id,a.name,b.name,c.name,remark,devicetype_id,platform_id from BaseInfo_device a left join BaseInfo_devicetype b on a.devicetype_id=b.id left join BaseInfo_platform c on a.platform_id=c.id where a.id in(select distinct device_id from BaseInfo_target)"
    deviceList = dbhandlebystr(queryDeviceStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetDeviceListWithoutTarget(request):
    queryDeviceStr = "select a.id,a.name,b.name,c.name,remark,devicetype_id,platform_id from BaseInfo_device a left join BaseInfo_devicetype b on a.devicetype_id=b.id left join BaseInfo_platform c on a.platform_id=c.id where a.id not in(select distinct device_id from BaseInfo_target)"
    deviceList = dbhandlebystr(queryDeviceStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetDeployedDeviceList(request):
    queryDeviceStr = "select b.name,c.name,ip,a.sn,bbcode,site,room,b.id,c.id,a.id from BaseInfo_devicedeploy a left join BaseInfo_device b on a.device_id=b.id left join BaseInfo_pnprole c on a.pnprole_id=c.id"
    deviceList = dbhandlebystr(queryDeviceStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetPnpRoleList(request):
    queryDeviceStr = "select id,name from BaseInfo_pnprole"
    deviceList = dbhandlebystr(queryDeviceStr)
    return HttpResponse(json.dumps({"result":deviceList}))
def GetReleaseList(request):
    queryReleaseStr = "select b.id c_id,a.id p_id,b.`name` current,a.`name` pre,c.`id` type,c.`name`,DATE_FORMAT(a.releasedate,'%Y-%m-%d'),a.remark from BaseInfo_release a right join BaseInfo_release b on a.id=b.pre_id left join BaseInfo_releasetype c on b.releasetype_id=c.id order by b.id desc;";
    releaseList = dbhandlebystr(queryReleaseStr)
    return HttpResponse(json.dumps({"result":releaseList}))
def GetReleaseTypeList(request):
    queryReleaseTypeStr = "select `id`,`name`,gituri,branchpath,ismonitor from BaseInfo_releasetype"
    releaseTypeList = dbhandlebystr(queryReleaseTypeStr)
    return HttpResponse(json.dumps({"result":releaseTypeList}))

def GetKpiList(request):
    queryKpiStr = "select id,testcasename from BaseInfo_kpi order by testcasename"
    kpiList = dbhandlebystr(queryKpiStr)
    return HttpResponse(json.dumps({"result":kpiList}))
def GetKpiTable(request):
    queryKpiStr = """select a.id,showname,concat(b.name,(case largeisbetter when 1 then '(+)' else '(-)' end)) unit,c.`name` kpitype,d.`name` priority,`key`,summary,remark,testcasename,b.id,largeisbetter,c.id,d.id from BaseInfo_kpi a 
                    left join BaseInfo_unit b on a.unit_id=b.id 
                    left join BaseInfo_kpitype c on a.kpitype_id=c.id 
                    left join BaseInfo_kpipriority d on a.kpipriority_id=d.id"""
    kpiTable = dbhandlebystr(queryKpiStr)
    return HttpResponse(json.dumps({"result":kpiTable}))
def GetFlagList(request):
    queryFlagStr = "select id,name from BaseInfo_flag"
    flagList = dbhandlebystr(queryFlagStr)
    return HttpResponse(json.dumps({"result":flagList}))
def GetKpiTypeList(request):
    queryKpiTypeStr = "select id,name from BaseInfo_kpitype"
    kpitypeList = dbhandlebystr(queryKpiTypeStr)
    return HttpResponse(json.dumps({"result":kpitypeList}))
def GetUnitList(request):
    queryUnitStr = "select id,name from BaseInfo_unit"
    unitList = dbhandlebystr(queryUnitStr)
    return HttpResponse(json.dumps({"result":unitList}))
def GetPriorityList(request):
    queryPriorityStr = "select id,name from BaseInfo_kpipriority"
    priorityList = dbhandlebystr(queryPriorityStr)
    return HttpResponse(json.dumps({"result":priorityList}))

def GetTestData(request):
    results = []
    jobid = request.GET.get("jobid")
    url_base = "http://10.239.97.26/automation-logs/%s" % (str(jobid))
    response_base = urllib2.urlopen(url_base)
    soup_base = BeautifulSoup(response_base.read())
    for item in soup_base.findAll("tr"):
        if item.find("td") != None:
            if item.find("td").find("img",src='/icons/folder.gif') != None:
                subJobid = item.find("td").findNextSibling("td").find("a").text;
                url_lkpserver = "http://10.239.97.26/automation-logs/%s/%s" % (str(jobid),str(subJobid))
                response = urllib2.urlopen(url_lkpserver)
                html = response.read()
                soup = BeautifulSoup(html)
                for tr in soup.findAll("tr"):
                    if tr.find("td") != None:
                        if tr.find("td").find("img",src='/icons/folder.gif') != None:
                            casename = tr.find("td").findNextSibling("td").find("a").text;
                            if casename.find("#") >= 0 or casename.find('Performance_') >=0:
                                values = GetLog(str(jobid),str(subJobid),casename.replace("#","%23").replace("/",""))
                                if len(values) > 0 and values.find("[") >= 0:
                                    results.append([casename.replace("/",""), values, subJobid.replace("cti-master.sh.intel.com_","").replace("/","")]);
    return HttpResponse(json.dumps({"result":results}))
def GetLog(jobid,subjobid,casename):
    url = 'http://10.239.97.26/automation-logs/%s/%s/%s/%s.log' % (jobid,subjobid,casename,casename)
    html = "";
    try:
        response = urllib2.urlopen(url)
        html = response.read().split("\n")[1].split("=")[1]
    except:
        return ""
    return html

def GetScoreDetail(request):
    releaseid = request.GET.get("releaseid")
    kpiid = request.GET.get("kpiid")
    deviceid = request.GET.get("deviceid")
    queryStr = """select format(a.score,2) score,b.`name`,a.remark,c.testcasename,concat(d.`name`,"(",(case c.largeisbetter when 0 then "-" else "+" end),")") unit,a.jobid
                from BaseInfo_testresult a left join BaseInfo_release b on a.release_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id left join BaseInfo_unit d on c.unit_id=d.id
                where a.kpi_id='%s' and a.device_id='%s' and a.release_id='%s' 
               """ % (kpiid,deviceid,releaseid)
    result = dbhandlebystr(queryStr)
    queryCommentStr = "select `comment` from BaseInfo_testresultcomment where device_id=%s and release_id=%s and kpi_id=%s" % (deviceid,releaseid,kpiid)
    temp = dbhandlebystr(queryCommentStr)
    comment = temp[0][0] if len(temp) > 0 else " "
    return HttpResponse(json.dumps({"result":result,"comment":comment}))
    
def GetKpiListByPnprole(request):
    pnprole = request.GET.get("pnprole")
    queryStr = "select c.id,c.testcasename from BaseInfo_pnprolekpi a left join BaseInfo_pnprole b on a.pnprole_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id where b.id=" + pnprole
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
def GetKpiListByDomain(request):
    domain = request.GET.get("domain")
    queryStr = "select c.id,c.testcasename from BaseInfo_kpidomain a left join BaseInfo_domain b on a.domain_id=b.id left join BaseInfo_kpi c on a.kpi_id=c.id where b.id=" + domain
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def GetTargetList(request):
    deviceid = request.GET.get("device")
    kpiid = request.GET.get("kpi")
    con = "";
    if kpiid != None and kpiid != "-1":
        con = " and b.id="+kpiid
    queryStr = "select a.id,b.showname,c.`name`,format(target,2),format(margin,2),format(rsd,2),format(regthrethold1,2),format(regthrethold2,2),format(regthrethold3,2),b.testcasename from BaseInfo_target a left join BaseInfo_kpi b on a.kpi_id=b.id left join BaseInfo_unit c on b.unit_id=c.id where device_id=%s %s" % (deviceid,con)
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def getRecipeMonitorList(request):
    deviceid = request.GET.get("device")
    releaseid = request.GET.get("release")
    con = "";
    if deviceid != None and deviceid != "-1":
        con += " and b.id="+deviceid
    if releaseid != None and releaseid != "-1":
        con += " and c.id="+releaseid
    queryStr = "select a.id,b.`name`,c.`name`,recipe,`status`,b.id,c.id from BaseInfo_recipemonitor a left join BaseInfo_device b on a.device_id=b.id left join BaseInfo_release c on a.release_id=c.id"
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def GetRecipeMonitor(request):
    queryStr = "select a.id,a.release_id,a.device_id,a.run_id,a.recipe,b.name,c.name from BaseInfo_recipemonitor a left join BaseInfo_release b on a.release_id=b.id left join BaseInfo_device c on a.device_id=c.id where `status`=0"
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))

def NewPlatform(request):
    name = request.GET.get("name")
    addStr = "insert into BaseInfo_platform(name) values('%s')" % (name)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
    
def NewDevice(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_device(name,devicetype_id,platform_id,remark) values('%s',%s,%s,'%s')" % (dataDict["name"],dataDict["devicetype"],dataDict["platform"],dataDict["remark"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
    
def NewDeployDevice(request):
    deviceid = request.GET.get("deviceid")
    pnproleid = request.GET.get("pnproleid")
    ip = request.GET.get("ip")
    sn = request.GET.get("sn")
    bbcode = request.GET.get("bbcode")
    site = request.GET.get("site")
    room = request.GET.get("room")
    addStr = "insert into BaseInfo_devicedeploy(device_id,pnprole_id,ip,sn,bbcode,site,room) values(%s,%s,'%s','%s','%s','%s','%s')" % (deviceid,pnproleid,ip,sn,bbcode,site,room)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
    
def NewPnprole(request):
    name = request.GET.get("name")
    addStr = "insert into BaseInfo_pnprole(name) values('%s')" % (name)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
def NewDomain(request):
    name = request.GET.get("name")
    addStr = "insert into BaseInfo_domain(name) values('%s')" % (name)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
def NewPnproleKpi(request):
    pnproleid = request.GET.get("pnprole")
    kpiid = request.GET.get("kpi")
    addStr = "insert into BaseInfo_pnprolekpi(pnprole_id,kpi_id) values(%s,%s)" % (pnproleid,kpiid)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
def NewDomainKpi(request):
    domainid = request.GET.get("domain")
    kpiid = request.GET.get("kpi")
    addStr = "insert into BaseInfo_kpidomain(domain_id,kpi_id) values(%s,%s)" % (domainid,kpiid)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))

def NewKpi(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_kpi(showname,testcasename,unit_id,largeisbetter,kpitype_id,kpipriority_id,`key`,summary,remark) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (dataDict["showname"],dataDict["testcasename"],dataDict["unit"],dataDict["largeisbetter"],dataDict["kpitype"],dataDict["kpipriority"],dataDict["key"],dataDict["summary"],dataDict["remark"])
        result = dbhandlebystr(addStr)
        queryDeviceStr = "select id from BaseInfo_device"
        deviceList = dbhandlebystr(queryDeviceStr)
        for device in deviceList:
            addTargetStr = "insert into BaseInfo_target(device_id,kpi_id,regthrethold1,regthrethold2,regthrethold3) values(%s,%s,0.03,0.05,0.07)" %(device[0],result)
            dbhandlebystr(addTargetStr)
    return HttpResponse(json.dumps({"message":result}))

def CopyTarget(request):
    sourcedevice = request.GET.get("sourcedevice")
    targetdevice = request.GET.get("targetdevice")
    copyStr = """DROP TABLE IF EXISTS `tmp_result`;
                Create temporary table tmp_result(select * from BaseInfo_target where device_id=%s);
                update tmp_result set device_id=%s;
                insert into BaseInfo_target(device_id,kpi_id,target,margin,rsd,regthrethold1,regthrethold2,regthrethold3) (select device_id,kpi_id,target,margin,rsd,regthrethold1,regthrethold2,regthrethold3 from tmp_result);""" % (sourcedevice,targetdevice)
    result = dbhandlebymultistr(copyStr)
    return HttpResponse(json.dumps({"result":result}))
    
def AutoImportTestData(request):
    release_name = request.GET.get("release_name")
    release_date = request.GET.get("release_date")
    release_pre = request.GET.get("release_pre")
    release_type = request.GET.get("release_type")
    release_remark = request.GET.get("release_remark")
    addReleaseStr = "insert into BaseInfo_release (name,releasedate,pre_id,releasetype_id,remark) values ('%s','%s',%s,%s,'%s')" % (release_name,release_date,release_pre,release_type,release_remark)
    releaseid = dbhandlebystr(addStr)
    deviceid = request.GET.get("deviceid")
    kpiid = request.GET.get("kpiid")
    jobid = request.GET.get("jobid")
    score = request.GET.get("score")
    remark = request.GET.get("remark")
    addTestDataStr = "insert into BaseInfo_testresult ( device_id,release_id,kpi_id,remark,score,jobid) values ( %s,%s,%s,'%s',%s,'%s')" % (deviceid,releaseid,kpiid,remark,score,jobid)
    result = dbhandlebystr(saveTestDataStr)
    return HttpResponse(json.dumps({"message":result}))
    
def SaveTestData(request):
    deviceid = request.GET.get("deviceid")
    releaseid = request.GET.get("releaseid")
    kpiid = request.GET.get("kpiid")
    remark = request.GET.get("remark")
    score = request.GET.get("score")
    jobid = request.GET.get("jobid")
    datafrom = request.GET.get("datafrom")
    getRunIndexStr = "select count(id) from BaseInfo_testresult where device_id=%s and release_id=%s and kpi_id=%s" % (deviceid,releaseid,kpiid)
    runindex = dbhandlebystr(getRunIndexStr)
    saveTestDataStr = "insert into BaseInfo_testresult (device_id,release_id,kpi_id,remark,score,jobid,datafrom_id,runindex) values ( %s,%s,%s,'%s',%s,'%s',%s,%s)" % (deviceid,releaseid,kpiid,remark,score,jobid,datafrom,runindex[0][0])
    print saveTestDataStr
    result = dbhandlebystr(saveTestDataStr)
    print result
    return HttpResponse(json.dumps({"message":result}))

def NewTestResult(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_testresult(device_id,kpi_id,release_id,jobid,score,datafrom_id,isavailable,remark) values(%s,%s,%s,'%s','%s',3,1,'%s')" % (dataDict["deviceid"],dataDict["kpiid"],dataDict["releaseid"],dataDict["jobid"],dataDict["score"],dataDict["remark"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))

def NewRecipeMonitor(request):
    result = "insert error!"
    recipeid = request.GET.get("recipeid")
    taskid = request.GET.get("taskid")
    isbisect = "0" if request.GET.get("isbisect")==None else request.GET.get("isbisect")
    getReleaseIDStr = "select id,`name` from BaseInfo_release where name='" + request.GET.get("release") + "'"
    getDeviceIDStr = "select id from BaseInfo_device where name='" + request.GET.get("device") + "'"
    release = dbhandlebystr(getReleaseIDStr)
    device = dbhandlebystr(getDeviceIDStr)
    
    if isbisect == "1":
        getTotalKpiNumStr = "select count(*) from BaseInfo_bisecttaskkpi a left join BaseInfo_bisecttaskkpi b on a.bisecttask_id=b.id where b.id=" + taskid
        totalkpinum = dbhandlebystr(getTotalKpiNumStr)
        addBisectTaskRunStr = "insert into BaseInfo_bisecttaskrun (bisecttask_id,preimage_id,jobid,status_id,totalkpinum) values (%s,'%s','%s',1,%s)" % (taskid,release[0][1],recipeid,totalkpinum[0][0])
        bisectrunid = dbhandlebystr(addBisectTaskRunStr)
        addBisectTaskRunPiplineStr = "insert into BaseInfo_bisecttaskrunpipline(bisecttaskrun_id,status_id,completekpinum,`timestamp`) values (%s,%s,%s,'%s')" % (bisectrunid,"1","0",str(datetime.datetime.now()))
        bisectrunpiplineid = dbhandlebystr(addBisectTaskRunPiplineStr)
    else:
        getTotalKpiNumStr = "select count(*) from BaseInfo_pnprolekpi a left join BaseInfo_devicedeploy b on a.pnprole_id=b.pnprole_id left join BaseInfo_plantask c on c.devicedeploy_id=b.id where c.id=" + taskid
        totalkpinum = dbhandlebystr(getTotalKpiNumStr)
        print release
        addTaskRunStr = "insert into BaseInfo_plantaskrun (task_id,image,jobid,status_id,totalkpinum) values (%s,'%s','%s',1,%s)" % (taskid,release[0][1],recipeid,totalkpinum[0][0])
        runid = dbhandlebystr(addTaskRunStr)
        addTaskRunPiplineStr = "insert into BaseInfo_plantaskrunpipline(run_id,status_id,completekpinum,`timestamp`) values (%s,%s,%s,'%s')" % (runid,"1","0",str(datetime.datetime.now()))
        runpiplineid = dbhandlebystr(addTaskRunPiplineStr)
    addStr = "insert into BaseInfo_recipemonitor (run_id,device_id,release_id,recipe,isbisect,status,failecount) values (%s,%s,%s,'%s',%s,0,0)" % (runid,device[0][0],release[0][0],recipeid,isbisect)
    result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
    
def UpdateRecipeMonitor(request):
    result = "insert error!"
    id = request.GET.get("id")
    failecount = request.GET.get("failecount")
    updateStr = "update BaseInfo_recipemonitor set status=1,failecount="+failecount+" where id="+id
    result = dbhandlebystr(updateStr)
    return HttpResponse(json.dumps({"result":result}))
def UpdateTaskRunStatus(request):
    result = "insert error!"
    rid = request.GET.get("rid")
    statusid = request.GET.get("status")
    finishedkpinum = request.GET.get("completekpinum")
    updateStr = "update BaseInfo_plantaskrun set status_id=%s,finishedkpinum=%s where id=%s" % (statusid,finishedkpinum,rid)
    result = dbhandlebystr(updateStr)
    return HttpResponse(json.dumps({"result":result}))
def UpdateBisectTaskRunStatus(request):
    result = "insert error!"
    rid = request.GET.get("rid")
    statusid = request.GET.get("status")
    finishedkpinum = request.GET.get("completekpinum")
    updateStr = "update BaseInfo_bisecttaskrun set status_id=%s,finishedkpinum=%s where id=%s" % (statusid,finishedkpinum,rid)
    result = dbhandlebystr(updateStr)
    return HttpResponse(json.dumps({"result":result}))
    
def NewRelease(request):
    result = "insert error!"
    releasename = request.GET.get("releasename")
    releasetype = "" 
    if releasename.startswith("LM"):
        releasetype = "1"
    elif releasename.startswith("L1"):
        releasetype = "3"
    elif releasename.startswith("MMR"):
        releasetype = "5"
    
    checkReleaseStr = "select id from BaseInfo_release where name='" + request.GET.get("releasename") + "'"
    check = dbhandlebystr(checkReleaseStr)
    if len(check) > 0:
        result = releasename + " exist!"
    else:
        getIDStr = "select id from BaseInfo_release where name='" + request.GET.get("prerelease") + "'"
        print getIDStr
        release = dbhandlebystr(getIDStr)
        prerelease = release[0][0]
        
        addStr = "insert into BaseInfo_release (name,releasedate,pre_id,releasetype_id,remark) values ('%s','%s',%s,%s,'%s')" % (releasename,str(datetime.datetime.now())[0:10],prerelease,releasetype,"")
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
def NewReleaseByWeb(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_release (name,releasedate,pre_id,remark,releasetype_id) values ('%s','%s',%s,'%s',%s)" % (dataDict["name"],dataDict["releasedate"],dataDict["pre"],dataDict["remark"],dataDict["releasetype"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"message":result}))
    
def NewReleaseType(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_releasetype (name,gituri,branchpath,ismonitor) values ('%s','%s','%s','%s')" % (dataDict["name"],dataDict["gituri"],dataDict["branchpath"],dataDict["ismonitor"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
    
def AddNewRelease(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_release (name,releasedate,pre_id,releasetype_id,remark) values ('%s','%s',%s,%s,'%s')" % (dataDict["name"],dataDict["releasedate"],dataDict["pre"],dataDict["releasetype"],dataDict["remark"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
def AddNewPullrequest(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_pullrequest (name,pullurl,preingration,ingrationurl,remark) values ('%s','%s','%s','%s','%s')" % (dataDict["name"],dataDict["pullurl"],dataDict["preingration"],dataDict["ingrationurl"],dataDict["remark"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
    
def AddReleasePullrequest(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        addStr = "insert into BaseInfo_releasepullrequest (pullrequest_id,release_id) values (%s,%s)" % (dataDict["pullrequestid"],dataDict["releaseid"])
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))

def EditPnprole(request):
    pid = request.GET.get("pid")
    name = request.GET.get("name")
    editStr = "update BaseInfo_pnprole set name='%s' where id=%s" % (name,pid)
    result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"result":result}))
def EditDomain(request):
    did = request.GET.get("did")
    name = request.GET.get("name")
    editStr = "update BaseInfo_domain set name='%s' where id=%s" % (name,did)
    result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"result":result}))
def EditTarget(request):
    tid = request.GET.get("tid")
    target = request.GET.get("target")
    margin = request.GET.get("margin")
    rsd = request.GET.get("rsd")
    tt1 = request.GET.get("tt1")
    tt2 = request.GET.get("tt2")
    tt3 = request.GET.get("tt3")
    editStr = "update BaseInfo_target set target='%s',margin='%s',rsd='%s',regthrethold1='%s',regthrethold2='%s',regthrethold3='%s' where id=%s" % (target,margin,rsd,tt1,tt2,tt3,tid)
    result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"result":result}))
def EditDeploy(request):
    did = request.GET.get("did")
    deviceid = request.GET.get("deviceid")
    pnproleid = request.GET.get("pnproleid")
    ip = request.GET.get("ip")
    sn = request.GET.get("sn")
    bbcode = request.GET.get("bbcode")
    site = request.GET.get("site")
    room = request.GET.get("room")
    editStr = "update BaseInfo_devicedeploy set device_id='%s',pnprole_id='%s',ip='%s',sn='%s',bbcode='%s',site='%s',room='%s' where id=%s" % (deviceid,pnproleid,ip,sn,bbcode,site,room,did)
    result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"result":result}))
def EditKpi(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "update BaseInfo_kpi set showname='%s',testcasename='%s',unit_id='%s',largeisbetter='%s',kpitype_id=%s,kpipriority_id=%s,`key`='%s',summary='%s',remark='%s' where id=%s" % (dataDict["showname"],dataDict["testcasename"],dataDict["unit"],dataDict["largeisbetter"],dataDict["kpitype"],dataDict["kpipriority"],dataDict["key"],dataDict["summary"],dataDict["remark"],dataDict["kid"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def EditDevice(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "update BaseInfo_device set name='%s',devicetype_id=%s,platform_id=%s,remark='%s' where id=%s" % (dataDict["name"],dataDict["devicetype"],dataDict["platform"],dataDict["remark"],dataDict["did"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def EditReleaseType(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "update BaseInfo_releasetype set name='%s',gituri='%s',branchpath='%s',ismonitor='%s' where id=%s" % (dataDict["name"],dataDict["gituri"],dataDict["branchpath"],dataDict["ismonitor"],dataDict["rtid"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def EditRelease(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "update BaseInfo_release set name='%s',releasedate='%s',pre_id=%s,remark='%s',releasetype_id=%s where id=%s" % (dataDict["name"],dataDict["releasedate"],dataDict["pre"],dataDict["remark"],dataDict["releasetype"],dataDict["rid"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def EditTestResult(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        query = "select datafrom_id from BaseInfo_testresult where id=" + dataDict["tid"]
        datafrom = dbhandlebystr(query)
        print datafrom
        if len(datafrom)>0 and datafrom[0][0] != 3:
            result = "can't edit the auto import data."
        else:            
            editStr = "update BaseInfo_testresult set device_id=%s,kpi_id=%s,release_id=%s,jobid='%s',score='%s',remark='%s' where id=%s" % (dataDict["deviceid"],dataDict["kpiid"],dataDict["releaseid"],dataDict["jobid"],dataDict["score"],dataDict["remark"],dataDict["tid"])
            result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
    
def GetPnproleById(request):
    pid = request.GET.get("pid")
    queryStr = "select name from BaseInfo_pnprole where id="+pid
    queryStr1 = "select kpi_id from BaseInfo_pnprolekpi where pnprole_id="+pid
    name = dbhandlebystr(queryStr)
    kpis = dbhandlebystr(queryStr1)
    return HttpResponse(json.dumps({"name":name,"kpis":kpis}))
def GetDomainById(request):
    did = request.GET.get("did")
    queryStr = "select name from BaseInfo_domain where id="+did
    queryStr1 = "select kpi_id from BaseInfo_kpidomain where domain_id="+did
    name = dbhandlebystr(queryStr)
    kpis = dbhandlebystr(queryStr1)
    return HttpResponse(json.dumps({"name":name,"kpis":kpis}))
    
def DeletePnproleKpi(request):
    result = "delete error!"
    pid = request.GET.get("pid")
    delStr = "delete from BaseInfo_pnprolekpi where pnprole_id="+pid
    delStr1 = "delete from BaseInfo_pnprole where id="+pid
    result = dbhandlebystr(delStr)
    result = dbhandlebystr(delStr1)
    return HttpResponse(json.dumps({"result":result}))
def DeleteDomainKpi(request):
    result = "delete error!"
    did = request.GET.get("did")
    delStr = "delete from BaseInfo_kpidomain where domain_id="+did
    delStr1 = "delete from BaseInfo_domain where id="+did
    result = dbhandlebystr(delStr)
    result = dbhandlebystr(delStr1)
    return HttpResponse(json.dumps({"result":result}))
    
def DeletePnproleKpiByPnproleId(request):
    result = "delete error!"
    pid = request.GET.get("pid")
    delStr = "delete from BaseInfo_pnprolekpi where pnprole_id="+pid
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteDomainKpiByDomainId(request):
    result = "delete error!"
    did = request.GET.get("did")
    delStr = "delete from BaseInfo_kpidomain where domain_id="+did
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteKpi(request):
    result = "delete error!"
    kid = request.GET.get("kid")
    delTarStr = "delete from BaseInfo_target where kpi_id="+kid
    result = dbhandlebystr(delTarStr)
    delStr = "delete from BaseInfo_kpi where id="+kid
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteDeploy(request):
    result = "delete error!"
    did = request.GET.get("did")
    delStr = "delete from BaseInfo_devicedeploy where id="+did
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))  
def DeleteDevice(request):
    result = "delete error!"
    did = request.GET.get("did")
    delStr = "delete from BaseInfo_device where id="+did
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteReleaseType(request):
    result = "delete error!"
    rtid = request.GET.get("rtid")
    delStr = "delete from BaseInfo_releasetype where id="+rtid
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteRelease(request):
    result = "delete error!"
    rid = request.GET.get("rid")
    queryuid = "select id from BaseInfo_release where pre_id=%s" % (rid)
    updateid = dbhandlebystr(queryuid)
    if(len(updateid) > 0):    
        querynid = "select pre_id from BaseInfo_release where id=%s" % (rid)
        newpre = dbhandlebystr(querynid)
        updatepre = "update BaseInfo_release set pre_id=%s where id=%s" % (newpre[0][0],updateid[0][0])
        update = dbhandlebystr(updatepre)
    
    delStr = "delete from BaseInfo_release where id=%s" % (rid)
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))
def DeleteTestResult(request):
    result = "insert error!"
    tid = request.GET.get("tid")
    query = "select datafrom_id from BaseInfo_testresult where id=" + tid
    datafrom = dbhandlebystr(query)
    if len(datafrom)>0 and datafrom[0][0] != 3:
        result = "can't delete the auto import data."
    else:            
        editStr = "update BaseInfo_testresult set isavailable=0 where id=%s" % (tid)
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
    
def GetMonitoeredReleaseType(request):
    rtList = ""
    queryStr = "select id,`name`,gituri,branchpath from BaseInfo_releasetype where ismonitor=1"
    result = dbhandlebystr(queryStr)
    for row in result:
        rtList += row[1].replace(" ","_") + " " + row[2] + " " + row[3] + "\n"
    return HttpResponse(rtList)
def GetMonitoeredReleaseTypeForWeb(request):
    queryStr = "select id,`name`,gituri,branchpath from BaseInfo_releasetype where ismonitor=1"
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def GetPlannedTaskForReleaseType(request):
    xmlresult = "<?xml version='1.0' encoding='utf-8'?><xml>\n"
    curTid = ""
    releasetypeid = request.GET.get("rtid")
    queryStr = """select a.id,c.`name`,d.`name`,b.ip,b.sn,f.testcasename,g.rsd from BaseInfo_plantask a 
                left join BaseInfo_devicedeploy b on a.devicedeploy_id=b.id 
                left join BaseInfo_pnprole c on b.pnprole_id=c.id 
                left join BaseInfo_device d on b.device_id=d.id
                left join BaseInfo_pnprolekpi e on e.pnprole_id=c.id
                left join BaseInfo_kpi f on e.kpi_id=f.id
                left join BaseInfo_target g on d.id=g.device_id and f.id=g.kpi_id
                where a.status='1' and a.releasetype_id=%s order by a.id""" % (releasetypeid)
    print queryStr
    result = dbhandlebystr(queryStr)
    for item in result:
        if(curTid != str(item[0])):
            if curTid != "":
                xmlresult += "</task>\n"
            xmlresult += "<task id='"+str(item[0])+"' test_set='"+item[1]+"'>\n"
            xmlresult += "    <device name='"+item[2]+"'>"+item[3]+":"+item[4]+"</device>\n"
            xmlresult += "    <KPI data_rsd='"+str(item[6])+"'>"+str(item[5])+"</KPI>\n"
            curTid = str(item[0])
        else:
            xmlresult += "    <KPI data_rsd='"+str(item[6])+"'>"+item[5]+"</KPI>\n"
    xmlresult += "</task>\n</xml>"
    #print xmlresult
    return HttpResponse(xmlresult)
    
def GetTaskList(request):
    queryStr = """select a.id,c.`name`,b.ip,b.sn,d.`name`,e.`name`,b.id,e.id,a.status from BaseInfo_plantask a left join BaseInfo_devicedeploy b on a.devicedeploy_id=b.id
                left join BaseInfo_device c on b.device_id=c.id left join BaseInfo_pnprole d on b.pnprole_id=d.id
                left join BaseInfo_releasetype e on a.releasetype_id=e.id where a.`status`='1'"""
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def NewTask(request):
    result = "insert error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "insert into BaseInfo_plantask (devicedeploy_id,releasetype_id,status) values (%s,%s,'%s')" % (dataDict["devicedeploy"],dataDict["releasetype"],dataDict["ismonitor"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def EditTask(request):
    result = "edit error!"
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        editStr = "update BaseInfo_plantask set devicedeploy_id=%s,releasetype_id=%s,status='%s' where id=%s" % (dataDict["devicedeploy"],dataDict["releasetype"],dataDict["ismonitor"],dataDict["tid"])
        result = dbhandlebystr(editStr)
    return HttpResponse(json.dumps({"message":result}))
def DeleteTask(request):
    result = "delete error!"
    tid = request.GET.get("tid")
    delStr = "delete from BaseInfo_plantask where id="+tid
    result = dbhandlebystr(delStr)
    return HttpResponse(json.dumps({"result":result}))

def GetTaskRunDevices(request):
    queryStr = "select distinct d.id,d.name from BaseInfo_plantaskrun a left join BaseInfo_plantask b on a.task_id=b.id left join BaseInfo_devicedeploy c on b.devicedeploy_id=c.id left join BaseInfo_device d on c.device_id=d.id order by a.jobid desc;"
    devices = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({ "devices":devices }))
def GetTaskRunImages(request):
    queryStr = "select distinct image from BaseInfo_plantaskrun order by jobid desc;"
    images = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({ "images":images }))
    
def GetTaskRunList(request):
    tid = request.GET.get("tid")
    device = request.GET.get("device")
    image = request.GET.get("image")
    sts = request.GET.get("status")
    con = "where 1=1"
    if tid != None:
        con += " and a.task_id="+tid
    if device != None:
        con += " and d.id="+device
    if image != None:
        con += " and a.image='"+image+"'"
    if sts != None:
        if str(sts) == "4":
            con += " and a.status_id in ('4','6')"
        else:
            con += " and a.status_id='"+str(sts)+"'"
    print con
    queryStr = "select Concat(d.`name`,' : ',c.ip,' : ',c.sn) device,a.image,a.jobid,e.`name`,a.id,c.pnprole_id,a.finishedkpinum,a.totalkpinum,f.name from BaseInfo_plantaskrun a left join BaseInfo_plantask b on a.task_id=b.id left join BaseInfo_devicedeploy c on b.devicedeploy_id=c.id left join BaseInfo_device d on c.device_id=d.id left join BaseInfo_taskrunstatus e on a.status_id=e.id left join BaseInfo_pnprole f on c.pnprole_id=f.id "+con+" order by a.jobid desc;"
    queryStatusStr = "select id,DATE_FORMAT(`timestamp`,'%Y-%m-%d %T'),run_id,status_id from BaseInfo_plantaskrunpipline where run_id in (select a.id from BaseInfo_plantaskrun a left join BaseInfo_plantask b on a.task_id=b.id left join BaseInfo_devicedeploy c on b.devicedeploy_id=c.id left join BaseInfo_device d on c.device_id=d.id "+con+")"
    taskrun = dbhandlebystr(queryStr)
    status = dbhandlebystr(queryStatusStr)
    return HttpResponse(json.dumps({ "taskrun":taskrun,"status":status }))
    
def EditComment(request):
    result = ""
    dataJsonStrUni = request.POST["record"]
    if dataJsonStrUni:
        dataDict = json.loads(dataJsonStrUni)
        queryStr = "select * from BaseInfo_testresultcomment where device_id=%s and release_id=%s and kpi_id=%s" % (dataDict["deviceid"],dataDict["releaseid"],dataDict["kpiid"])
        temp = dbhandlebystr(queryStr)
        sqlStr = ""
        if len(temp) > 0:
            sqlStr = "update BaseInfo_testresultcomment set comment='%s' where device_id=%s and release_id=%s and kpi_id=%s" % (dataDict["comment"],dataDict["deviceid"],dataDict["releaseid"],dataDict["kpiid"])
        else:
            sqlStr = "insert into BaseInfo_testresultcomment(device_id,release_id,kpi_id,comment) values(%s,%s,%s,'%s')" % (dataDict["deviceid"],dataDict["releaseid"],dataDict["kpiid"],dataDict["comment"])
        result = dbhandlebystr(sqlStr)
        return HttpResponse(json.dumps({"result":result}))
        
def GetRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    queryStr = "select count(*) from BaseInfo_plantaskrunpipline where run_id=%s and status_id=%s" % (runid,statusid)
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
def AddRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    completekpinum = request.GET.get("completekpinum")
    queryStr = "select * from BaseInfo_plantaskrunpipline where run_id=%s and status_id=%s" % (runid,statusid)
    temp = dbhandlebystr(queryStr)
    result = ""
    if len(temp) <= 0:
        addStr = "insert into BaseInfo_plantaskrunpipline(run_id,status_id,completekpinum,`timestamp`) values (%s,%s,%s,'%s')" % (runid,statusid,completekpinum,str(datetime.datetime.now()))
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
def UpdateRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    completekpinum = request.GET.get("completekpinum")
    updateStr = "update BaseInfo_plantaskrunpipline set completekpinum=%s) where run_id=%s and status_id=%s" % (completekpinum,runid,statusid)
    result = dbhandlebystr(updateStr)
    return HttpResponse(json.dumps({"result":result}))

def GetRegression(request):
    regList = []
    deviceid = request.GET.get("deviceid")
    releaseid = request.GET.get("releaseid")
    jobid = request.GET.get("jobid")
    plantaskrunid = request.GET.get("plantaskrunid")
    queryStr = """select e.id,a.jobid,CONCAT(round(avg(a.score),2),'') cur_score,CONCAT(round(avg(c.score),2),'') pre_score,CONCAT(d.regthrethold2,'') thh,e.largeisbetter,a.kpi_id,g.devicedeploy_id from BaseInfo_testresult a
            left join BaseInfo_release b on a.release_id=b.id
            left join BaseInfo_testresult c on c.release_id=b.pre_id and a.device_id=c.device_id and a.kpi_id=c.kpi_id
            left join BaseInfo_target d on a.device_id=d.device_id and a.kpi_id=c.kpi_id
            left join BaseInfo_kpi e on a.kpi_id=e.id
            left join BaseInfo_plantaskrun f on a.jobid=f.jobid
            left join BaseInfo_plantask g on f.task_id=g.id
            where a.release_id=%s and a.device_id=%s and a.jobid=%s and a.runindex<3 and c.runindex<3
            group by a.kpi_id order by e.showname""" % (releaseid,deviceid,jobid)
    records = dbhandlebystr(queryStr)
    for record in records:
        offset = (string.atof(record[2])-string.atof(record[3]))/string.atof(record[2]) if record[5] == 0 else (string.atof(record[2])-string.atof(record[3]))/string.atof(record[3])
        if offset > string.atof(record[4]):
            regList.append(record)
    if len(regList) > 0:
        addBisectTask = "insert into BaseInfo_bisecttask(taskrun_id,status) values(%s,'0')" % (plantaskrunid)
        bt_id = dbhandlebystr(addBisectTask)
        for reg in regList:
            addBisectTaskKpi = "insert into BaseInfo_bisecttaskkpi(bisecttask_id,kpi_id) values(%s,%s)" % (bt_id,reg[0])
            btk_id = dbhandlebystr(addBisectTaskKpi)
    return HttpResponse(json.dumps({"result":regList}))
def GetBisectTask(request):
    queryStr = "select * from BaseInfo_bisecttask where status='0'"
    result = dbhandlebystr(queryStr)
    return HttpResponse(result)
        
def GetXmlForBisectTask(request):
    releaseid = request.GET.get("releaseid")
    xmlresult = "<?xml version='1.0' encoding='utf-8'?><xml>\n"
    curTid = ""
    queryStr = """select a.id,e.`name`,f.`name`,d.ip,d.sn,h.testcasename,i.rsd from BaseInfo_bisecttask a 
                left join BaseInfo_plantaskrun b on a.taskrun_id=b.id
                left join BaseInfo_plantask c on b.task_id=c.id
                left join BaseInfo_devicedeploy d on c.devicedeploy_id=d.id 
                left join BaseInfo_pnprole e on d.pnprole_id=e.id 
                left join BaseInfo_device f on d.device_id=f.id
                left join BaseInfo_bisecttaskkpi g on g.bisecttask_id=a.id
                left join BaseInfo_kpi h on g.kpi_id=h.id
                left join BaseInfo_target i on d.id=i.device_id and h.id=i.kpi_id
                where a.status='0' order by a.id"""
    preIntListQuery = "select preintno from BaseInfo_preimage where release_id=" + releaseid
    result = dbhandlebystr(queryStr)
    preIntList = dbhandlebystr(preIntListQuery)
    preIntListStr = ""
    for preInt in preIntList:
        preIntListStr += str(preInt[0])+","
    for item in result:
        if(curTid != str(item[0])):
            if curTid != "":
                xmlresult += "</task>\n"
            xmlresult += "<task id='"+str(item[0])+"' test_set='"+item[1]+"' preint_no='"+preIntListStr[0:-1]+"'>\n"
            xmlresult += "    <device name='"+item[2]+"'>"+item[3]+":"+item[4]+"</device>\n"
            xmlresult += "    <KPI data_rsd='"+str(item[6])+"'>"+item[5]+"</KPI>\n"
            curTid = str(item[0])
        else:
            xmlresult += "    <KPI data_rsd='"+str(item[6])+"'>"+item[5]+"</KPI>\n"
    xmlresult += "</task>\n</xml>"
    return HttpResponse(xmlresult)

def GetBisectRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    queryStr = "select count(*) from BaseInfo_bisecttaskrunpipline where run_id=%s and status_id=%s" % (runid,statusid)
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
def AddBisectRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    completekpinum = request.GET.get("completekpinum")
    queryStr = "select * from BaseInfo_bisecttaskrunpipline where run_id=%s and status_id=%s" % (runid,statusid)
    temp = dbhandlebystr(queryStr)
    result = ""
    if len(temp) <= 0:
        addStr = "insert into BaseInfo_bisecttaskrunpipline(run_id,status_id,completekpinum,`timestamp`) values (%s,%s,%s,'%s')" % (runid,statusid,completekpinum,str(datetime.datetime.now()))
        result = dbhandlebystr(addStr)
    return HttpResponse(json.dumps({"result":result}))
def UpdateBisectRunStatus(request):
    runid = request.GET.get("runid")
    statusid = request.GET.get("statusid")
    completekpinum = request.GET.get("completekpinum")
    updateStr = "update BaseInfo_bisecttaskrunpipline set completekpinum=%s) where run_id=%s and status_id=%s" % (completekpinum,runid,statusid)
    result = dbhandlebystr(updateStr)
    return HttpResponse(json.dumps({"result":result}))
    
def GetTestresultSummary(request):
    result = []
    deviceid = request.GET.get("deviceid")
    releaseid = request.GET.get("releaseid")
    jobid = request.GET.get("jobid")
    queryStr = """select e.id,e.testcasename,CONCAT(d.target,''),CONCAT(d.margin,''),CONCAT(d.regthrethold1,'') tth1,CONCAT(d.regthrethold2,'') tth2,a.jobid,CONCAT(round(avg(a.score),2),'') cur_score,CONCAT(round(avg(c.score),2),'') pre_score,e.largeisbetter,g.devicedeploy_id,b.`name` `release`,i.`name` role,j.`name` device,e.`key`,e.summary,k.`name` priority,concat(l.`name`,'(',(case e.largeisbetter when 1 then '+' else '-' end),')') unit,m.`name` from BaseInfo_testresult a
                left join BaseInfo_release b on a.release_id=b.id
                left join BaseInfo_testresult c on c.release_id=b.pre_id and a.device_id=c.device_id and a.kpi_id=c.kpi_id
                left join BaseInfo_target d on a.device_id=d.device_id and a.kpi_id=d.kpi_id
                left join BaseInfo_kpi e on a.kpi_id=e.id
                left join BaseInfo_plantaskrun f on a.jobid=f.jobid
                left join BaseInfo_plantask g on f.task_id=g.id
                left join BaseInfo_devicedeploy h on g.devicedeploy_id=h.id
                left join BaseInfo_pnprole i on h.pnprole_id=i.id
                left join BaseInfo_device j on h.device_id=j.id
                left join BaseInfo_kpipriority k on e.kpipriority_id=k.id
                left join BaseInfo_unit l on e.unit_id=l.id
                left join BaseInfo_release m on m.id=b.pre_id
                where a.release_id=%s and a.device_id=%s and a.jobid=%s and a.runindex<3 and c.runindex<3
                group by a.kpi_id order by e.showname""" % (releaseid,deviceid,jobid)
    result = dbhandlebystr(queryStr)
    if len(result) <=0:
        queryStr = """select e.id,e.testcasename,CONCAT(d.target,''),CONCAT(d.margin,''),CONCAT(d.regthrethold1,'') tth1,CONCAT(d.regthrethold2,'') tth2,a.jobid,CONCAT(round(avg(a.score),2),'') cur_score,"0" pre_score,e.largeisbetter,g.devicedeploy_id,b.`name` `release`,i.`name` role,j.`name` device,e.`key`,e.summary,k.`name` priority,concat(l.`name`,'(',(case e.largeisbetter when 1 then '+' else '-' end),')') unit,m.`name` from BaseInfo_testresult a
                left join BaseInfo_release b on a.release_id=b.id
                left join BaseInfo_target d on a.device_id=d.device_id and a.kpi_id=d.kpi_id
                left join BaseInfo_kpi e on a.kpi_id=e.id
                left join BaseInfo_plantaskrun f on a.jobid=f.jobid
                left join BaseInfo_plantask g on f.task_id=g.id
                left join BaseInfo_devicedeploy h on g.devicedeploy_id=h.id
                left join BaseInfo_pnprole i on h.pnprole_id=i.id
                left join BaseInfo_device j on h.device_id=j.id
                left join BaseInfo_kpipriority k on e.kpipriority_id=k.id
                left join BaseInfo_unit l on e.unit_id=l.id
                left join BaseInfo_release m on m.id=b.pre_id
                where a.release_id=%s and a.device_id=%s and a.jobid=%s and a.runindex<3
                group by a.kpi_id order by e.showname""" % (releaseid,deviceid,jobid)
        result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def AddNewPreImgPullReq(request):
    result = ""
    dataList = request.POST
    devicename = request.GET.get("devicename")
    imagefolder = request.GET.get("imagefolder")
    releaseid = request.GET.get("releaseid")
    localpath = request.GET.get("localpath")
    for data in dataList:
        preimgName = imagefolder+"-flashfiles-"+devicename+"-L1p000"+data+".zip"
        downloadpath = "https://mcg-depot.intel.com/artifactory/cactus-absp-tl/llp_mr1-preintegration/"+str(data)+"/"+imagefolder+"/userdebug/"+preimgName
        insertPreImgStr = "insert into BaseInfo_preimage(name,isdownloaded,downloadpath,localpath,release_id)values('%s','%s','%s','%s',%s)" % (preimgName,"1",downloadpath,localpath,str(releaseid))
        newPreImg = dbhandlebystr(insertPreImgStr)
        temp = ''.join(map(str, dataList[data]))
        tempList = temp.replace("['", "").replace("']", "").split(',')
        for pullreq in tempList:
            print pullreq
            jiraurl = " https://jira01.devtools.intel.com/rest/api/2/issue/"+pullreq+"/comment?"
            insertPulReqStr = "insert into BaseInfo_pullrequest(name,jiraurl,remark,preimage_id,release_id)values('%s','%s','%s',%s,%s)" % (pullreq,jiraurl,"",str(newPreImg),str(releaseid))
            result = dbhandlebystr(insertPulReqStr)
    return HttpResponse(json.dumps({"result":result}))
    
def GetSourceResult(request):
    result = []
    deviceid = request.GET.get("deviceid")
    releaseid = request.GET.get("releaseid")
    kpiid = request.GET.get("kpiid")
    jobid = request.GET.get("jobid")
    queryStr = "select CONCAT(score,'') from BaseInfo_testresult where device_id=%s and release_id=%s and kpi_id=%s and jobid=%s and runindex<3" % (deviceid,releaseid,kpiid,jobid)
    result = dbhandlebystr(queryStr)
    return HttpResponse(json.dumps({"result":result}))
    
def dbhandlebystr(strsql,multi=False,args=None):
    conn=MySQLdb.connect(host=settings.DATABASES['default']['HOST'],user=settings.DATABASES['default']['USER'],passwd=settings.DATABASES['default']['PASSWORD'],db=settings.DATABASES['default']['NAME'],port=string.atoi(settings.DATABASES['default']['PORT']),charset="utf8")
    cur=conn.cursor()
    if(multi):
        cur.executemany(strsql,args)
    else:
        cur.execute(strsql)
    if(strsql.upper().startswith("INSERT")):
        results = int(conn.insert_id())
    else:
        results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return results

def dbhandlebymultistr(strsql):
    conn=MySQLdb.connect(host=settings.DATABASES['default']['HOST'],user=settings.DATABASES['default']['USER'],passwd=settings.DATABASES['default']['PASSWORD'],db=settings.DATABASES['default']['NAME'],port=string.atoi(settings.DATABASES['default']['PORT']),charset="utf8")
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    for singalstr in strsql.replace("\n","").split(";"):
        if len(singalstr)>0:
            cur.execute(singalstr)
    results = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return results