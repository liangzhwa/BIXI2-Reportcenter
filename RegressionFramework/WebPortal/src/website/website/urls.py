from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('rest.urls')),

    url(r'^$', views.index),
	url(r'^kpireleaseview$', views.kpireleaseview),
    url(r'^kpideviceview$', views.kpideviceview),
    url(r'^devicereleaseview$', views.devicereleaseview),
    url(r'^importresult$', views.importresult),
    url(r'^devicemanager$', views.devicemanager),
    url(r'^deployeddevicemanager$', views.deployeddevicemanager),
    url(r'^pnprolekpimanager$', views.pnprolekpimanager),
    url(r'^kpimanager$', views.kpimanager),
    url(r'^kpitargetmanager$', views.kpitargetmanager),
    url(r'^recipemonitormanager$', views.recipemonitormanager),
    url(r'^testdataresultmanager$', views.testdataresultmanager),
    url(r'^monitortaskmanager$', views.monitortaskmanager),
    url(r'^releasemanager$', views.releasemanager),
    url(r'^releasetypemanager$', views.releasetypemanager),
    url(r'^domainmanager$', views.domainmanager),
    url(r'^taskrunmonitor$', views.taskrunmonitor),
)
