import urllib2
import sys
import json
import re
import os

def exec_cmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

def get_pre_int_build_from_json(jira_no,folder_jira_json):
	f=open(folder_jira_json+'/GMINL-'+jira_no+'.json')
	data_json=f.read()
	addr_PreIntBuild=''
	data_string=json.loads(data_json)
	for string in data_string[u'comments']:
		#m=re.search('gmin_l_mr1-preintegration', string[u'body'])
		#m=re.search('llp_mr1_r1-preintegration', string[u'body'])
		#m=re.findall(r'https://buildbot.tl.intel.com/absp/builders/llp_mr1_r1-preintegration/builds/\d{1,5}',string[u'body'])
		m=re.findall(r'https://buildbot.tl.intel.com/absp/builders/llp_mr1-preintegration/builds/\d{1,5}',string[u'body'])
        #if m is not None:
			#print('******************************')	
			#addr_PreIntBuild=string[u'body'].split('https://')[1]
		if m != []:
			addr_PreIntBuild=m[0]
	return addr_PreIntBuild

def main():
	if len(sys.argv)!=3:
		print("please enter pull request no!!!")
		return 1;
	print get_pre_int_build_from_json(JIRA_NO,FOLDER_JIRA_JSON)

if __name__=='__main__':
	JIRA_NO=sys.argv[1]
	FOLDER_JIRA_JSON=sys.argv[2]
	sys.exit(main())

