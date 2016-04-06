from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    return render_to_response('index.html')

def importresult(request):
    return render_to_response('importresult.html')
def devicemanager(request):
    return render_to_response('devicemanager.html')
def deployeddevicemanager(request):
    return render_to_response('deployeddevicemanager.html')
def pnprolekpimanager(request):
    return render_to_response('pnprolekpimanager.html')
    
def kpireleaseview(request):
    return render_to_response('kpireleaseview.html')
def kpideviceview(request):
    return render_to_response('kpideviceview.html')
def devicereleaseview(request):
    return render_to_response('devicereleaseview.html')
def kpimanager(request):
    return render_to_response('kpimanager.html')
def kpitargetmanager(request):
    return render_to_response('kpitargetmanager.html')
def recipemonitormanager(request):
    return render_to_response('recipemonitormanager.html')
def testdataresultmanager(request):
    return render_to_response('testdataresultmanager.html')
def monitortaskmanager(request):
    return render_to_response('monitortaskmanager.html')
def releasemanager(request):
    return render_to_response('releasemanager.html')
def releasetypemanager(request):
    return render_to_response('releasetypemanager.html')
def domainmanager(request):
    return render_to_response('domainmanager.html')
def taskrunmonitor(request):
    return render_to_response('taskrunmonitor.html')