from django.db import models
from datetime import datetime

class Flag(models.Model):
    name = models.CharField(max_length=100)

class PlatForm(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class DeviceType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    platform = models.ForeignKey(PlatForm, related_name='platform_device')
    devicetype = models.ForeignKey(DeviceType, related_name='devicetype_device')
    sn = models.CharField(max_length=100,blank=True,default='')
    intelno = models.CharField(max_length=100,blank=True)
    remark = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class ReleaseType(models.Model):
    name = models.CharField(max_length=100)
    gituri = models.CharField(max_length=500,default='')
    branchpath = models.CharField(max_length=500,default='')
    ismonitor = models.NullBooleanField(default=True)
    def __unicode__(self):
        return self.name

class Release(models.Model):
    name = models.CharField(max_length=100,unique=True)
    pre = models.ForeignKey('self',null=True,blank=True,related_name='release_release')
    releasetype = models.ForeignKey(ReleaseType,null=True,default=None,related_name='releasetype_release')
    releasedate = models.DateField(null=True,blank=True)
    remark = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class KpiType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class KpiPriority(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Domain(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class KPI(models.Model):
    testcasename = models.CharField(max_length=200)
    showname = models.CharField(max_length=100)
    kpitype = models.ForeignKey(KpiType, related_name='kpitype_kpi', default=1)
    kpipriority = models.ForeignKey(KpiPriority, related_name='kpipriority_kpi', default=1)
    unit = models.ForeignKey(Unit, related_name='unit_kpi', default=2)
    largeisbetter = models.NullBooleanField(default=True)
    summary = models.TextField(blank=True,default="",max_length=500)
    key = models.TextField(blank=True,default="",max_length=500)
    isassist = models.NullBooleanField(default=False)
    flag = models.ForeignKey(Flag, related_name='flag_kpi', default=None)
    remark = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.showname

class KpiDomain(models.Model):
    kpi = models.ForeignKey(KPI, related_name='kpi_Kpidomain')
    domain = models.ForeignKey(Domain, related_name='domain_Kpidomain')

class TestResultFrom(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
class TestResult(models.Model):
    device = models.ForeignKey(Device, related_name='device_testresult')
    release = models.ForeignKey(Release, related_name='release_testresult')
    kpi = models.ForeignKey(KPI, related_name='kpi_testresult')
    score = models.DecimalField(max_digits=10, decimal_places=2)
    jobid = models.CharField(blank=True,default="",max_length=100)
    remark = models.TextField(blank=True)
    datafrom = models.ForeignKey(TestResultFrom, related_name='testresultfrom_testresult',default=1)
    runindex = models.IntegerField(blank=True, default=0)
    isavailable = models.NullBooleanField(default=True)
class TestResultComment(models.Model):
    device = models.ForeignKey(Device, related_name='device_testresultcomment')
    release = models.ForeignKey(Release, related_name='release_testresultcomment')
    kpi = models.ForeignKey(KPI, related_name='kpi_testresultcomment')
    comment = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    isavailable = models.NullBooleanField(default=True)

class Target(models.Model):
    kpi = models.ForeignKey(KPI, related_name='kpi_target')
    device = models.ForeignKey(Device, related_name='device_target')
    target = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=0)
    margin = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=0)
    rsd = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=10)
    regthrethold1 = models.DecimalField(max_digits=3, decimal_places=2,blank=True,default=0)
    regthrethold2 = models.DecimalField(max_digits=3, decimal_places=2,blank=True,default=0)
    regthrethold3 = models.DecimalField(max_digits=3, decimal_places=2,blank=True,default=0)
    
    def __unicode__(self):
        return str(self.target)
        
class PNPRole(models.Model):
    name = models.CharField(max_length=100)

class PNPRoleKPI(models.Model):
    pnprole = models.ForeignKey(PNPRole, related_name='pnprole_pnprolekpi')
    kpi = models.ForeignKey(KPI, related_name='kpi_pnprolekpi')

class DeviceDeploy(models.Model):
    device = models.ForeignKey(Device, related_name='device_devicedeploy')
    pnprole = models.ForeignKey(PNPRole, related_name='pnprole_devicedeploy')
    ip = models.CharField(max_length=100)
    sn = models.CharField(max_length=100)
    bbcode = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    
class TaskRunStatus(models.Model):
    name = models.CharField(blank=True,default="",max_length=100)

class PlanTask(models.Model):
    devicedeploy = models.ForeignKey(DeviceDeploy, related_name='devicedeploy_plantask',default=1)
    releasetype = models.ForeignKey(ReleaseType, related_name='releasetype_plantask',default=1)
    status = models.CharField(blank=True,default="",max_length=10)
class PlanTaskRun(models.Model):
    plantask = models.ForeignKey(PlanTask, related_name='plantask_taskrun')
    image = models.CharField(blank=True,default="",max_length=100)
    jobid = models.CharField(blank=True,default="",max_length=100)
    status = models.ForeignKey(TaskRunStatus, related_name='taskrunstatus_plantaskrun',default=None)
    finishedkpinum = models.IntegerField(blank=True, default=0)
    totalkpinum = models.IntegerField(blank=True, default=0)
    totalestimatetime = models.IntegerField(blank=True, default=0)
class PlanTaskRunPipline(models.Model):
    run = models.ForeignKey(PlanTaskRun, related_name='plantaskrun_plantaskrunpipline',blank=True,default=1)
    status = models.ForeignKey(TaskRunStatus, related_name='taskrunstatus_plantaskrunpipline',default=None)
    timestamp = models.DateTimeField(null=True,blank=True,default=datetime.now)
    completekpinum = models.IntegerField(blank=True, default=0)

class PreImage(models.Model):
    name = models.CharField(max_length=100)
    release = models.ForeignKey(Release, related_name='release_preimage',default=None)
    priIntNo = models.CharField(max_length=1024,default="")
    downloadpath = models.CharField(max_length=1024,default="")
    localpath = models.CharField(max_length=1024,default="")
    isdownloaded = models.NullBooleanField(default=True)
class PullRequest(models.Model):
    name = models.CharField(max_length=100)
    jiraurl = models.CharField(max_length=500)
    release = models.ForeignKey(Release, related_name='release_pullrequest',null=True)
    preimage = models.ForeignKey(PreImage, related_name='preimage_pullrequest',null=True)
    remark = models.TextField(blank=True)
class BisectTask(models.Model):
    plantaskrun = models.ForeignKey(PlanTaskRun, related_name='plantaskrun_bisecttask',null=True)
    status = models.CharField(blank=True,default="",max_length=10)
class BisectTaskKpi(models.Model):
    bisecttask = models.ForeignKey(BisectTask, related_name='bisecttask_bisecttaskkpi')
    kpi = models.ForeignKey(KPI, related_name='kpi_bisecttaskkpi')
class BisectTaskRun(models.Model):
    bisecttask = models.ForeignKey(BisectTask, related_name='bisecttask_bisecttaskrun')
    preimage = models.ForeignKey(PreImage, related_name='preimage_bisecttaskrun')
    jobid = models.CharField(blank=True,default="",max_length=100)
    status = models.ForeignKey(TaskRunStatus, related_name='taskrunstatus_bisecttaskrun',default=None)
    finishedkpinum = models.IntegerField(blank=True, default=0)
    totalkpinum = models.IntegerField(blank=True, default=0)
    totalestimatetime = models.IntegerField(blank=True, default=0)
class BisectTaskRunPipline(models.Model):
    run = models.ForeignKey(BisectTaskRun, related_name='bisecttaskrun_bisecttaskrunpipline',blank=True,default=1)
    status = models.ForeignKey(TaskRunStatus, related_name='taskrunstatus_bisecttaskrunpipline',default=None)
    timestamp = models.DateTimeField(null=True,blank=True,default=datetime.now)
    completekpinum = models.IntegerField(blank=True, default=0)

class BisectResult(models.Model):
    baserelease = models.ForeignKey(Release, related_name='baserelease_bisectresult')
    targetrelease = models.ForeignKey(Release, related_name='targetrelease_bisectresult')
    preimage = models.ForeignKey(PreImage, related_name='preimage_bisectresult',null=True)
    kpi = models.ForeignKey(KPI, related_name='kpi_bisectresult')
    device = models.ForeignKey(Device, related_name='device_bisectresult')
    jobid = models.CharField(blank=True,default="",max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.TextField(blank=True)

    def __unicode__(self):
        return self.remark

class RecipeMonitor(models.Model):
    run = models.ForeignKey(PlanTaskRun, related_name='plantaskrun_recipemonitor',blank=True,default=1)
    device = models.ForeignKey(Device, related_name='device_recipemonitor')
    release = models.ForeignKey(Release, related_name='release_recipemonitor')
    recipe = models.CharField(blank=True,default="",max_length=100)
    isbisect = models.NullBooleanField(default=False)
    status = models.CharField(default=0,max_length=1)
    failecount = models.CharField(default=0,max_length=100)
