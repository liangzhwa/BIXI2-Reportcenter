#!/usr/bin/env python
import sys
import os
import re
import pexpect
import time
import StringIO
import ConfigParser
from optparse import make_option, OptionParser
from os.path import expanduser

CUR_PATH = os.path.dirname(__file__)

class config_reform:
    def __init__(self,ini_src,dest_ini='/tmp/dest.ini'):
        self._config = ConfigParser.RawConfigParser()
        self._src_ini = ini_src
        self._dest_ini = dest_ini
        self._reform_flag = 0

    def reform(self):
        if self._reform_flag:
            pass
        else:
            _sn = 0
            _fp = ''
            if os.path.isfile(self._src_ini):
                _fp = open(self._src_ini)
            else:
                _fp = self._src_ini.split("\n")
            for line in _fp:
                line = re.sub(' += +','=',line)
                if '' == line.strip():
                    continue
                elif '[INFO]' in line.strip():
                    continue
                elif '[DEVICE]' == line.strip():
                    _sect = 'DEVICE_' + str(_sn)
                    self._config.add_section(_sect)
                    _sn += 1
                    continue
                _key,_txt = line.strip().split('=')
                self._config.set(_sect,_key,_txt)
            with open(self._dest_ini, 'wb') as configfile:
                self._config.write(configfile)
            self._reform_flag = 1

    def get_key_list(self,key,key_name):
        self.reform()
        _sn = 0
        _arr = []
        while 1:
            _sect = 'DEVICE_'+str(_sn)
            if self._config.has_section(_sect):
                if self._config.get(_sect,key) == key_name:
                    if _sect not in _arr:
                        _arr.append(_sect)
                _sn += 1
            else:
                break
        return _arr

    def list_key_product(self,key,product_name):
        _arr = self.get_key_list(key,product_name)
        for _s in _arr:
            #print "\n[" + _s + "]"
            print "\n[DEVICE]"
            for _k in self._config.options(_s):
                print _k + '=' + self._config.get(_s,_k)

    def list_all_product(self):
        self.reform()
        _sn = 0
        while 1:
            _sect = 'DEVICE_' + str(_sn)
            if self._config.has_section(_sect):
                print "\n[" + _sect + "]"
                for _k in self._config.options(_sect):
                    print _k + '=' + self._config.get(_sect,_k)
                _sn += 1
            else:
                break

class Remotor:
    def __init__(self):
        self._rid = 'Y2F0c0B0ZXN0Ym90LXNlcnZlci5zaC5pbnRlbC5jb20lJWNhdHM=\n'
        #self._rid = 'dGVzdGJvdC1zZXJ2ZXIuc2guaW50ZWwuY29t\n'

    def _ssh_cmd(self, cmd, timeout=1800):
        """run ssh cmd"""
        _ssh = pexpect.spawn("ssh %s %s" % (self._rid.decode('base64','strict').split('%%')[0], cmd), timeout=timeout)
        _result = ''
        try:
            i = _ssh.expect(['password: ', 'continue connecting (yes/no)?'], timeout=timeout)
            if i == 0 :
                _ssh.sendline(self._rid.decode('base64','strict').split('%%')[1])
            elif i == 1:
                _ssh.sendline('yes')
                j = _ssh.expect(['assword: '], timeout=timeout)
                if j == 0:
                    _ssh.sendline(self._rid.decode('base64','strict').split('%%')[1])
                else:
                    print "did not expect password"
                    sys.exit(1)
        except pexpect.EOF:
            _ssh.close()
        except pexpect.TIMEOUT:
            print "cmd has timeout, timeout=%d" % timeout
            _ssh.close()
        else:
            _result = _ssh.read()
            _ssh.expect(pexpect.EOF, timeout=timeout)
            _ssh.close()
        return _result.strip()
    
    def _scp_file(self, src_file, dst_file, timeout=1800):
        """run scp cmd"""
        _ssh = pexpect.spawn("scp %s %s:%s" % (src_file, self._rid.decode('base64','strict').split('%%')[0], dst_file), timeout=timeout)
        _result = ''
        try:
            i = _ssh.expect(['password: ', 'continue connecting (yes/no)?'], timeout=timeout)
            if i == 0 :
                _ssh.sendline(self._rid.decode('base64','strict').split('%%')[1])
            elif i == 1:
                _ssh.sendline('yes')
                j = _ssh.expect(['assword: '], timeout=timeout)
                if j == 0:
                    _ssh.sendline(self._rid.decode('base64','strict').split('%%')[-1])
                else:
                    print "did not expect password"
                    sys.exit(1)
        except pexpect.EOF:
            _ssh.close()
        except pexpect.TIMEOUT:
            print "cmd has timeout, timeout=%d" % timeout
            _ssh.close()
        else:
            _result = _ssh.read()
            _ssh.expect(pexpect.EOF, timeout=timeout)
            _ssh.close()
        return _result.strip()

class TestService(Remotor):
    def __init__(self):
        Remotor.__init__(self)
        self._version = "\nAuto Test Service\nVersion: 1.1\n"

    def version(self):
        print self._version
    
    def list_template(self):
        """list template"""
        template_path = os.path.join(CUR_PATH, 'template')
        print "----------------Avaliable Template List---------------------"
        for _, _, files in os.walk(template_path, True):
            for name in files:
                print(os.path.join(name))
    
    def update_template(self):
        """update template"""
        _template_loc = 'http://pnp.sh.intel.com/ATS/template/'
        template_path = os.path.join(CUR_PATH, 'template')
        os.system('rm -rf %s/*' % template_path)
        if not os.path.isdir(template_path):
            os.system('mkdir -p %s' % template_path)
        cmd = 'wget --no-proxy -c -r -A template*.xml -l 1 -P %s -np -nd %s && echo \'success\' || echo \'fail\'' % (template_path,_template_loc)
        f = os.popen(cmd, 'r')
        msg = f.read()
        if msg.find('success') < 0:
            print 'update template failed'
            print msg
            return 1
        return 0
    
    def trig_test(self,xml_path):
        """trig test by xml"""
        xml_name = os.path.basename(xml_path)
        dst_name = '/tmp/%s' % xml_name
        usrhome = expanduser("~")
        _known_hosts = '%s/.ssh/known_hosts' % usrhome
        _ip = self._rid.decode('base64','strict').split('%%')[0].split('@')[-1]
        if os.path.exists(_known_hosts):
            rm_key_cmd = 'ssh-keygen -f %s/.ssh/known_hosts -R %s >/dev/null 2>&1' % (usrhome,_ip)
            os.popen(rm_key_cmd)
        Remotor._scp_file(self, xml_path, dst_name)
        cmd = 'python /home/cats/pnp/ats/cats_commit.py %s' % dst_name
        msg = Remotor._ssh_cmd(self, cmd)
        print msg
    
    def get_recipe_state(self,recipe_id):
        """get recipe state"""
        cmd = "cats-client get_recipe_status " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        elif 'UNKNOWN_RECIPE_STATUS' in msg:
            print 'UNKNOWN_RECIPE_STATUS'
        else:
            print msg

    def get_pend_tasks(self):
        """Get pending tasks"""
        cmd = "cats-client get_pending_list"
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            print msg
    
    def cancel_recipe(self,recipe_id):
        """cancel recipe"""
        cmd = "cats-client cancel_recipe " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            print msg
    
    def get_recipe_progress(self,recipe_id):
        """get recipe state"""
        cmd = "cats-client get_testing_progress " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            arr = re.split(r'\r\n',msg)
            length = len(arr)
            template = "{CaseName:80}{Progress:5}"
            print template.format(CaseName="Case Name",Progress="Progress")
            for i in range(1,length):
                line = arr[i].strip()
                if 30 <= len(line.split()[0]): 
                    print template.format(CaseName=line.split()[0][0:-10],Progress=line.split()[-1])
                else:
                    print template.format(CaseName=line.split()[0],Progress=line.split()[-1])
    
    def get_device_ip(self,recipe_id):
        '''get test device ip by specified recipe id'''
        cmd = "cats-client get_device_ip " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            print msg
    
    def get_device_state(self,device_ip):
        '''get device state by specified device_ip'''
        cmd = "cats-client get_device_status " + device_ip
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            print msg
    
    def get_product(self,product):
        '''get device list by product'''
        cmd = "cats-client get_device" 
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            if 'ALL' == product.upper():
                print msg
            else:
                tmp = '/tmp/cats-device-list.ini'
                cr = config_reform(msg,tmp)
                cr.list_key_product('product',product)
    
    def get_product_byname(self,product_name):
        '''get device list by name'''
        cmd = "cats-client get_device" 
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            tmp = '/tmp/cats-device-list.ini'
            cr = config_reform(msg,tmp)
            cr.list_key_product('name',product_name)
    
    def get_product_bysn(self,product_spn):
        '''get device list by serial port number'''
        cmd = "cats-client get_device" 
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            tmp = '/tmp/cats-device-list.ini'
            cr = config_reform(msg,tmp)
            cr.list_key_product('serial',product_spn)
    
    def get_product_byip(self,product_ip):
        '''get device list by ip'''
        cmd = "cats-client get_device" 
        msg = Remotor._ssh_cmd(self, cmd)
        if 'Unknown syntax' in msg:
            print 'Unknown syntax'
        else:
            tmp = '/tmp/cats-device-list.ini'
            cr = config_reform(msg,tmp)
            cr.list_key_product('ip',product_ip)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    option_list = [
                   make_option("-l", "--list-template", dest="list_template", action="store_true", help="List all aviliable template"),
                   make_option("-u", "--update-temp", dest="update_temp", action="store_true", help="Update templates"),
                   make_option("-t", "--trig-test", dest="test_xml", action="store", help="Trig test by xml file"),
                   make_option("-s", "--get-state", dest="task", action="store", help="Get state of task id"),
                   make_option("-c", "--cancel-task", dest="cancel_task", action="store", help="Cancel task by task id"),
                   make_option("-i", "--get-ip", dest="task_id", action="store", help="Get device ip for task id"),
                   make_option("-P", "--get_product", dest="product_name", action="store", help="Get device list for product_name"),
                   make_option("-I", "--get-product-byIP", dest="host_ip", action="store", help="Get device list by HOST_IP"),
                   make_option("-n", "--get-product-byName", dest="name", action="store", help="Get device by NAME"),
                   make_option("-p", "--get-product-bySPN", dest="product_spn", action="store", help="Get device by device SPN(serial port number)"),
                   make_option("-d", "--get-device-stat", dest="device_ip", action="store", help="Get device state by device_ip(HOST_IP:DEVICE_SPN)"),
                   make_option("-w", "--get-wait-task", dest="wait_task", action="store_true", help="List waiting tasks"),
                   make_option("-v", "--version", dest="version", action="store_true", help="Show version"),
                  ]
    # create help doc
    usage = "%prog [options]"

    # exit and print help doc when no option is found
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    parser = OptionParser(option_list=option_list, usage=usage)
    (options, args) = parser.parse_args()

    testservice = TestService()

    if options.list_template:
        testservice.list_template()
        sys.exit(0)
    if options.task:
        recipe_id = options.task
        testservice.get_recipe_state(recipe_id)
        testservice.get_recipe_progress(recipe_id)
        sys.exit(0)
    if options.wait_task:
        testservice.get_pend_tasks()
        sys.exit(0)
    if options.cancel_task:
        recipe_id = options.cancel_task
        testservice.cancel_recipe(recipe_id)
        sys.exit(0)
    if options.device_ip:
        device_ip = options.device_ip
        testservice.get_device_state(device_ip)
        sys.exit(0)
    if options.product_name:
        product = options.product_name
        testservice.get_product(product)
        sys.exit(0)
    if options.host_ip:
        productIP = options.host_ip
        testservice.get_product_byip(productIP)
        sys.exit(0)
    if options.name:
        device_name = options.name
        testservice.get_product_byname(device_name)
        sys.exit(0)
    if options.product_spn:
        product_spn = options.product_spn
        testservice.get_product_bysn(product_spn)
        sys.exit(0)
    if options.task_id:
        recipe_id = options.task_id
        testservice.get_device_ip(recipe_id)
        sys.exit(0)
    if options.update_temp:
        sys.exit(testservice.update_template())
    if options.test_xml:
        xml_file = options.test_xml
        testservice.trig_test(xml_file)
    if options.version:
        testservice.version()
        sys.exit(0)
