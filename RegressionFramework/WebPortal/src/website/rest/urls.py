from django.conf.urls import patterns, url
from rest import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^gettestresultbyjobid$', views.GetTestResultByJobid),
    url(r'^getdomainlist$', views.GetDomainList),
    url(r'^getplatformlist$', views.GetPlatformList),
    url(r'^getdevicetypelist$', views.GetDeviceTypeList),
    url(r'^getdevicelist$', views.GetDeviceList),
    url(r'^getdevicelistwithtarget$', views.GetDeviceListWithTarget),
    url(r'^getdevicelistwithouttarget$', views.GetDeviceListWithoutTarget),
    url(r'^getdeployeddevicelist$', views.GetDeployedDeviceList),
    url(r'^getpnprolelist$', views.GetPnpRoleList),
    url(r'^getreleaselist$', views.GetReleaseList),
    url(r'^getreleasetypelist$', views.GetReleaseTypeList),
    url(r'^getkpilist$', views.GetKpiList),
    url(r'^getkpitable$', views.GetKpiTable),
    url(r'^getflaglist$', views.GetFlagList),
    url(r'^getkpitypelist$', views.GetKpiTypeList),
    url(r'^getunitlist$', views.GetUnitList),
    url(r'^getprioritylist$', views.GetPriorityList),
    url(r'^getrecipemonitor$', views.GetRecipeMonitor),
    url(r'^gettestdata$', views.GetTestData),
    url(r'^getscoredetail$', views.GetScoreDetail),
    url(r'^getkpilistbypnprole$', views.GetKpiListByPnprole),
    url(r'^getkpilistbydomain$', views.GetKpiListByDomain),
    url(r'^gettargetlist$', views.GetTargetList),
    url(r'^getrecipemonitorlist$', views.getRecipeMonitorList),
    
    url(r'^newplatform$', views.NewPlatform),
    url(r'^newdevice$', views.NewDevice),
    url(r'^newdeploydevice$', views.NewDeployDevice),
    url(r'^newpnprole$', views.NewPnprole),
    url(r'^newdomain$', views.NewDomain),
    url(r'^newpnprolekpi$', views.NewPnproleKpi),
    url(r'^newdomainkpi$', views.NewDomainKpi),
    url(r'^newkpi$', views.NewKpi),
    url(r'^copytarget$', views.CopyTarget),
    url(r'^autoimporttestdata$', views.AutoImportTestData),
    url(r'^savetestdata$', views.SaveTestData),
    url(r'^newtestresult$', views.NewTestResult),
    
    url(r'^newrelease$', views.NewRelease),
    url(r'^newreleasebyweb$', views.NewReleaseByWeb),
    url(r'^newreleasetype$', views.NewReleaseType),
    url(r'^addnewrelease$', views.AddNewRelease),
    url(r'^addnewpullrequest$', views.AddNewPullrequest),
    url(r'^addreleasepullrequest$', views.AddReleasePullrequest),
    
    url(r'^editpnprole$', views.EditPnprole),
    url(r'^editdomain$', views.EditDomain),
    url(r'^edittarget$', views.EditTarget),
    url(r'^editdeploy$', views.EditDeploy),
    url(r'^editkpi$', views.EditKpi),
    url(r'^editdevice$', views.EditDevice),
    url(r'^editreleasetype$', views.EditReleaseType),
    url(r'^editrelease$', views.EditRelease),
    url(r'^edittestresult$', views.EditTestResult),
        
    url(r'^getpnprolebyid$', views.GetPnproleById),
    url(r'^getdomainbyid$', views.GetDomainById),
    url(r'^deletepnprolekpi$', views.DeletePnproleKpi),
    url(r'^deletedomainkpi$', views.DeleteDomainKpi),
    url(r'^deletepnprolekpibypnproleId$', views.DeletePnproleKpiByPnproleId),
    url(r'^deletedomainkpibydomainId$', views.DeleteDomainKpiByDomainId),
    url(r'^deletekpi$', views.DeleteKpi),
    url(r'^deletedeploy$', views.DeleteDeploy),
    url(r'^deletedevice$', views.DeleteDevice),
    url(r'^deletereleasetype$', views.DeleteReleaseType),
    url(r'^deleterelease$', views.DeleteRelease),
    url(r'^deletetestresult$', views.DeleteTestResult),
    
    url(r'^getkpireleaseview$', views.GetKpiReleaseView),
    url(r'^getkpideviceview$', views.GetKpiDeviceView),
    url(r'^getdevicereleaseview$', views.GetDeviceReleaseView),
    
    url(r'^newrecipemonitor$', views.NewRecipeMonitor),
    url(r'^updaterecipemonitor$', views.UpdateRecipeMonitor),
    url(r'^updatetaskrunstatus$', views.UpdateTaskRunStatus),
    url(r'^getmonitoeredreleasetype$', views.GetMonitoeredReleaseType),
    url(r'^getmonitoeredreleasetypeforweb$', views.GetMonitoeredReleaseTypeForWeb),
    url(r'^getplannedtaskforreleasetype$', views.GetPlannedTaskForReleaseType),
    url(r'^gettasklist$', views.GetTaskList),
    url(r'^newtask$', views.NewTask),
    url(r'^edittask$', views.EditTask),
    url(r'^deletetask$', views.DeleteTask),
    url(r'^gettaskrundevices$', views.GetTaskRunDevices),
    url(r'^gettaskrunimages$', views.GetTaskRunImages),
    url(r'^gettaskrunlist$', views.GetTaskRunList),
    url(r'^editcomment$', views.EditComment),
    url(r'^getrunstatus$', views.GetRunStatus),
    url(r'^addrunstatus$', views.AddRunStatus),
    url(r'^updaterunstatus$', views.UpdateRunStatus),
    
    url(r'^getregression$', views.GetRegression),
    url(r'^getbisecttask$', views.GetBisectTask),
    url(r'^getxmlforbisecttask$', views.GetXmlForBisectTask),
    
    url(r'^gettestresultsummary$', views.GetTestresultSummary),
    url(r'^addnewpreimgpullreq$', views.AddNewPreImgPullReq),
    url(r'^getsourceresult$', views.GetSourceResult),
)