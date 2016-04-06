#coding=utf8
import httplib
import string
import sys
import os
reload(sys) 
sys.setdefaultencoding('utf-8')
httpClient = None

def RunBisect(releaseno,devicename,releaseid):
    os.system("../WebPortal/src/PnPRegression/feed2testbot % % %" % (releaseno,devicename,releaseid))

if __name__=='__main__':
    #RunBisect()
    test = "q" if 1==1 else "w"