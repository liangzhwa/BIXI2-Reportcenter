from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
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

def request_version(url):
	from base64 import encodestring
	req = urllib2.Request(url)
	b64str = encodestring('%s:%s' % (LOGIN,PASSWD))[:-1]
	req.add_header("Authorization","Basic %s" % b64str)
	return req

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
		#m=re.search('GMINL-', data)
		m=re.findall(r'GMINL-\d{1,5}',data)
		#if m is not None:
		if m!= []:
			#print('%s' % data)
			print(m[0])
			fp = open("./logs/"+ReleaseNo+"_PullRequests/"+ReleaseNo+"_PullRequest_List.info", 'a')
			#fp.write(('%s\n' % data))
		    	fp.write(m[0]+'\n')
			fp.close()
			#exec_cmd("echo "+('%s' % data)+" >>"+ReleaseNo+"_PullRequest_List.info")	

def get_pull_request_from_wiki(release_no):
	parser = MyHTMLParser()
	WIKI_URL = 'https://securewiki.ith.intel.com/display/GMIN/L-MR1+Release+'+release_no
	exec_cmd("bash ./bin/download_wiki.sh "+WIKI_URL+" "+"./logs/"+release_no+"_PullRequests")
	exec_cmd("rm "+"./logs/"+release_no+"_PullRequests/"+release_no+"_PullRequest_List.info")
	f = file("./logs/"+release_no+"_PullRequests/L-MR1+Release+"+release_no,"r")
	parser.feed(f.read())
	parser.close()
	f.close()

def main():
	get_pull_request_from_wiki(ReleaseNo)

if __name__=='__main__':
	ReleaseNo = sys.argv[1]
	sys.exit(main())

