'''
Created on Dec 10, 2014

@author: sxy
'''
import xml.dom.minidom as minidom
import sys
import os
import time
import copy

def exec_cmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

dom = minidom.parse(sys.argv[1])
tasks = dom.getElementsByTagName("task")
task_idTuple=()
for task in tasks:
	task_id=task.getAttribute("id")
	task_idTuple=task_idTuple+(task_id,)
	test_set=task.getAttribute("test_set")
	preint_nos=task.getAttribute("preint_no")
	device_name=task.getElementsByTagName("device")[0].getAttribute("name")
	preint_noList=preint_nos.split(",")
	for preint_no in preint_noList:
		exec_cmd("echo "+task_id+" "+device_name+" "+test_set+" "+preint_no+" >>"+sys.argv[2])
print sys.argv[2]+" is generated successfully"
