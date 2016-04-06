'''
Created on Dec 10, 2014

@author: sxy
'''
import xml.dom.minidom as minidom
import sys
import os
import time

def print_perf_case():
        features = dom_perf.getElementsByTagName("Feature")
        print("There are %d features in xml" % features.length )
        for feature in features:
            print(feature.attributes["name"].value)
            cases = feature.getElementsByTagName("Case")
            #print("There are %d cases in feature %s" %(cases.length, feature.getAttribute("name")))    
            for case in cases:
                print("name = " + case.getAttribute("name"))
                print("enble = " + case.getAttribute("enable"))

def print_pwr_case():
        features = dom_pnp.getElementsByTagName("Feature")
        print("There are %d features in xml" % features.length )
        for feature in features:
            print(feature.attributes["name"].value)
            cases = feature.getElementsByTagName("Case")
            #print("There are %d cases in feature %s" %(cases.length, feature.getAttribute("name")))    
            for case in cases:
                print("name = " + case.getAttribute("name"))
                print("enble = " + case.getAttribute("enable"))

def exec_cmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

release_no=sys.argv[1]
preInt_release=sys.argv[2]
pnp_device_name=sys.argv[3]
pnp_task_id=sys.argv[4]
log_xml4testbot=sys.argv[5]
	
dom = minidom.parse("./task_info_list_preInt.xml")

tasks = dom.getElementsByTagName("task")
task_idTuple=()
for task in tasks:
	task_id=task.getAttribute("id")
	task_idTuple=task_idTuple+(task_id,)
	test_set=task.getAttribute("test_set")
	print("task_id= "+task_id+" "+"test_set= " +test_set)
	device_name=task.getElementsByTagName("device")[0].getAttribute("name")
	device_sn=task.getElementsByTagName("device")[0].childNodes[0].nodeValue[-8:]
	device_addr=task.getElementsByTagName("device")[0].childNodes[0].nodeValue[:-9]
	print("		devicesinfo: "+" "+device_name+" "+device_addr+" "+device_sn)
	KPIs=task.getElementsByTagName("KPI")
	for KPI in KPIs:
		print("			KPI= "+KPI.childNodes[0].nodeValue)
print task_idTuple
#dict_task_id ={}.fromkeys(task_idTuple,{'test_set': '', 'device_name': '', 'device_sn': '', 'device_addr': '', 'KPIs': []})
dict_task_id ={}.fromkeys(task_idTuple)

for task in tasks:
	task_id=task.getAttribute("id")
	test_set=task.getAttribute("test_set")
	device_name=task.getElementsByTagName("device")[0].getAttribute("name")
	device_sn=task.getElementsByTagName("device")[0].childNodes[0].nodeValue[-8:]
	device_addr=task.getElementsByTagName("device")[0].childNodes[0].nodeValue[:-9]
	list_KPIs=[]
	KPIs=task.getElementsByTagName("KPI")	
	for KPI in KPIs:
		list_KPIs.append(KPI.childNodes[0].nodeValue)
	dict_task_id[task_id]={'test_set': test_set, 'device_name': device_name, 'device_sn': device_sn, 'device_addr': device_addr, 'KPIs': list_KPIs}
print dict_task_id


for key in dict_task_id.keys():
	print("id="+key)
	exec_cmd("echo "+ key + " >> task_list.txt")
	print("	test_set= "+dict_task_id[key]['test_set'])
	print("	device_name= "+dict_task_id[key]['device_name'])
	print("	device_sn= "+dict_task_id[key]['device_sn'])
	print("	device_addr= "+dict_task_id[key]['device_addr'])
	for KPI in dict_task_id[key]['KPIs']:
		print("	KPI= "+KPI)
	
pnp_test_set=dict_task_id[pnp_task_id]['test_set']
pnp_device_sn=dict_task_id[pnp_task_id]['device_sn']
pnp_device_addr=dict_task_id[pnp_task_id]['device_addr']
pnp_KPIs=dict_task_id[pnp_task_id]['KPIs']

if pnp_device_name != dict_task_id[pnp_task_id]['device_name']:
	print "ERROR device_name is not correct"
	exit(1)
	
print(time.asctime()+' get image and firmware info.....................................................')
print("preInt_release = " + preInt_release)
print("device_name = " + pnp_device_name)
print("pnp_test_set = " + pnp_test_set)
print("pnp_device_sn = " + pnp_device_sn)
print("pnp_device_addr = " + pnp_device_addr)
print("pnp_task_id = " + pnp_task_id)

#L_buildinfo=exec_cmd("./bin/getImage_preInt.sh --preInt_release "+ preInt_release + " --device " + pnp_device_name).split()
L_buildinfo=["NULL","NULL","NULL","NULL","NULL"]
L_buildinfo[0]="OK"
L_buildinfo[1]="http://10.239.93.157:9900/static/preInt_build/"+"coho"+"-"+"flashfiles"+"-"+pnp_device_name+"-"+"L1p000"+preInt_release+".zip"
L_buildinfo[2]=exec_cmd("curl "+L_buildinfo[1]+".md5"+" | awk '{print $1}'")
L_buildinfo[3]="http://10.239.93.157:9900/static/preInt_build/"+"coho"+"-"+"flashfiles"+"-"+pnp_device_name+"-"+"L1p000"+preInt_release+".zip"
L_buildinfo[4]=exec_cmd("curl "+L_buildinfo[1]+".md5"+" | awk '{print $1}'")

if L_buildinfo[0] !="OK":
		print(time.asctime()+" ERROR!!! can not get img")
		sys.exit(-1)
else:
	j=0			
	for buildinfo in L_buildinfo:
		print( "L_buildinfo[%d] = %s"%(j,buildinfo))
		j=j+1	
							   					
D_pnp_sample_files={'power-speaker':'./template/tb_pwr_sample_speaker.xml','power-headset':'./template/tb_pwr_sample_headset.xml','performance':'./template/tb_perf_sample.xml'}
dom_pnp = minidom.parse(D_pnp_sample_files[pnp_test_set])
print(test_set+" test build info..........................................................................")		
if len(L_buildinfo) == 5 and L_buildinfo[0] == "OK":
	device = dom_pnp.getElementsByTagName("Device")[0]
	device.getElementsByTagName("ip")[0].childNodes[0].nodeValue=pnp_device_addr
	device.getElementsByTagName("serial")[0].childNodes[0].nodeValue=pnp_device_sn
		
	options = dom_pnp.getElementsByTagName("Options")[0]
	options.getElementsByTagName("image_uri")[0].childNodes[0].nodeValue=L_buildinfo[1]
	options.getElementsByTagName("image_md5sum")[0].childNodes[0].nodeValue=L_buildinfo[2]
	options.getElementsByTagName("firmware_uri")[0].childNodes[0].nodeValue=L_buildinfo[3]
	options.getElementsByTagName("firmware_md5sum")[0].childNodes[0].nodeValue=L_buildinfo[4]
	options.getElementsByTagName("build_number")[0].childNodes[0].nodeValue=preInt_release
	options.getElementsByTagName("build_name")[0].childNodes[0].nodeValue=L_buildinfo[1].split('/')[-1]
	if pnp_device_name == "ECS210A":
		options.getElementsByTagName("device")[0].childNodes[0].nodeValue="ECS2 10A"
	else:
		options.getElementsByTagName("device")[0].childNodes[0].nodeValue=pnp_device_name
	print(time.asctime()+' get image and firmware OK!!!')
else:
	print(time.asctime()+' get image and firmware ERROR!!!')
	sys.exit(-1)
	
features = dom_pnp.getElementsByTagName("Feature")
for feature in features:
	cases = feature.getElementsByTagName("Case")
	for case in cases:
		case.setAttribute("enable","N")
		case.setAttribute("monitor","N")
		case.setAttribute("round","%d"%(3) )
for feature in features:
	if feature.getAttribute("name") in pnp_KPIs or feature.getAttribute("name")=="test_env":
		cases = feature.getElementsByTagName("Case")
		for case in cases:
			case.setAttribute("enable","Y")
					
	#print_pwr_case()
pnp_xml_name='preInt_'+preInt_release+'_'+pnp_device_name+'_id-'+pnp_task_id+'_'+pnp_test_set+'.xml'
f =  open("./logs/"+release_no+"_PullRequests/"+pnp_xml_name,  'w')
dom_pnp.writexml(f,encoding = 'utf-8')
f.close()
print(time.asctime()+' '+ pnp_xml_name +' for testbot is generated successfully!!!')                                
exec_cmd("echo "+ pnp_xml_name + " >>"+ log_xml4testbot)
                             
