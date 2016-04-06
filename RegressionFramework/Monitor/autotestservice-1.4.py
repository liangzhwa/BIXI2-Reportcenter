#!/usr/bin/env python
import sys
import os
import re
import pexpect
import time
import urllib2
import getpass
import StringIO
import ConfigParser
import xml.etree.ElementTree as xmlet
from optparse import make_option, OptionParser
from os.path import expanduser

CUR_PATH = os.path.dirname(__file__)
SRLOC = 'aHR0cDovL3BucC5zaC5pbnRlbC5jb20vYXRzX3YyL2FuZHJvaWQvc3Jj\n'
HAS = SRLOC.strip() + 'L2NvbmZpZy91c2Vycw==\n'

def webreader(url):
    #print 'def',sys._getframe().f_code.co_name
    #no proxies
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    data = urllib2.urlopen(url)
    page_content = data.read()
    return page_content

class xml_formator:
    def __init__(self,xml_path):
        self.xml_path = xml_path

    def pretty_xml(self):
        xmltree = xmlet.parse(self.xml_path)
        root = xmltree.getroot()
        self.indent(root)
        #xmlet.dump(root)
        xmltree.write(self.xml_path)
    
    def indent(self, elem, level=0, more_sibs=False):
        i = "\n"
        if level:
            i += (level-1) * '  '
        num_kids = len(elem)
        if num_kids:
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
                if level:
                    elem.text += '  '
            count = 0
            for kid in elem:
                self.indent(kid, level+1, count < num_kids - 1)
                count += 1
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
                if more_sibs:
                    elem.tail += '  '
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
                if more_sibs:
                    elem.tail += '  '

class ats_templ_scrapor:
    def __init__(self,templ_xml_path='/tmp/ats_tmpl.xml'):
        self.templ_xml_path = templ_xml_path
        self.branch_url = SRLOC.decode('base64','strict') + '/config/branch.conf'
        self.pnp_case_url = SRLOC.decode('base64','strict') + '/case_xml/ats-pnp-cases.xml'

    def get_branch_config(self):
        txt = webreader(self.branch_url)
        lines = txt.split("\n")
        _index = 0
        branch_list = []
        branch_ver_list = []
        device_list = []
        for line in lines:
            #print line
            _index += 1
            if 1 < _index:
                line = line.replace(" ", "").strip()
                if '' == line:
                    continue
                _list = line.split("|")
                _branch = _list[0]
                _branch_ver = _list[1]
                _device = _list[2]
                if _branch not in branch_list:
                    branch_list.append(_branch)
                if _branch_ver not in branch_ver_list:
                    branch_ver_list.append(_branch_ver)
                if _device not in device_list:
                    device_list.append(_device)
            else:
                pass
        #print branch_list,branch_ver_list,device_list
        return branch_list,branch_ver_list,device_list
    
    def get_raw_case_list_from_xml(self):
        txt = webreader(self.pnp_case_url)
        casexmlroot = xmlet.fromstring(txt)
        xml_case_list = []
        for casenode in casexmlroot.iter('case'):
            #print xmlet.dump(casenode)
            #print xmlet.tostring(casenode)
            for child in casenode:
                child.clear()
                #casenode.remove(child)
            n_case_node_str = xmlet.tostring(casenode).split("\n")[0] + "</case>"
            xml_case_list.append(n_case_node_str)
        #print xml_case_list
        return xml_case_list

    def get_revise_case_list_from_xml(self):
        txt = webreader(self.pnp_case_url)
        casexmlroot = xmlet.fromstring(txt)
        xml_case_list = []
        for featnode in casexmlroot.iter('feature'):
            feature_name = featnode.attrib['name']
            casenode = featnode.find('case')
            casenode.set('name',feature_name)
            for child in casenode:
                child.clear()
            n_case_node_str = xmlet.tostring(casenode).split("\n")[0] + "</case>"
            xml_case_list.append(n_case_node_str)
        return xml_case_list
    
    def mk_templ_xml(self):
        branch_list,branch_ver_list,device_list = self.get_branch_config()
        #print branch_list,branch_ver_list,device_list
        #xml_case_list = self.get_case_list_from_xml()
        xml_case_list = self.get_revise_case_list_from_xml()
        root = xmlet.Element('PnPATS')
        essential_node = xmlet.SubElement(root,'Essentials')
        project_node = xmlet.SubElement(essential_node,'Project')
        project_node.text = 'IRDA'
        android_branch_node = xmlet.SubElement(essential_node,'AndroidBranch')
        _index = 0
        for branch in branch_list:
            opt_node = xmlet.SubElement(android_branch_node,'option')
            opt_node.text = branch
            if 0 == _index:
                opt_node.set('enable','Y')
                _index += 1
            else:
                opt_node.set('enable','N')
        android_ver_node = xmlet.SubElement(essential_node,'AndroidVersion')
        _index = 0
        for branch_ver in branch_ver_list:
            opt_node = xmlet.SubElement(android_ver_node,'option')
            opt_node.text = branch_ver
            if 0 == _index:
                opt_node.set('enable','Y')
                _index += 1
            else:
                opt_node.set('enable','N')
        device_node = xmlet.SubElement(essential_node,'Device')
        _index = 0
        for dev in device_list:
            opt_node = xmlet.SubElement(device_node,'option')
            opt_node.text = dev
            if 0 == _index:
                opt_node.set('enable','Y')
                _index += 1
            else:
                opt_node.set('enable','N')
    
        testmode_node = xmlet.SubElement(essential_node,'TestMode')
        opt_node = xmlet.SubElement(testmode_node,'option')
        opt_node.text = "Daily"
        opt_node.set('enable','N')
        opt_node = xmlet.SubElement(testmode_node,'option')
        opt_node.text = "DevTest"
        opt_node.set('enable','Y')
        opt_node = xmlet.SubElement(testmode_node,'option')
        opt_node.text = "Weekly"
        opt_node.set('enable','N')

        test_imginfo_node = xmlet.SubElement(essential_node,'TestImage')
        xmlet.SubElement(test_imginfo_node,'BuildName')
        xmlet.SubElement(test_imginfo_node,'BuildNumber')
        xmlet.SubElement(test_imginfo_node,'ImageLink')
        #xmlet.SubElement(test_imginfo_node,'ImageMD5Sum')
        email_node = xmlet.SubElement(essential_node,'Emails')
        
        optional_node = xmlet.SubElement(root,'OPTIONALS')
        fwinfo_node = xmlet.SubElement(optional_node,'FirmwareInfo')
        xmlet.SubElement(fwinfo_node,'FirmwareLink')
        #xmlet.SubElement(fwinfo_node,'FirmwareMD5Sum')
        compare_img_node = xmlet.SubElement(optional_node,'CompareImage')
        xmlet.SubElement(compare_img_node,'BuildName')
        bisechome_node = xmlet.SubElement(optional_node,'BiSectHome')
        debug_node = xmlet.SubElement(optional_node,'Debug')
        debug_node.set('enable','N')
        #CaseList
        caselist_node = xmlet.SubElement(root,'CaseList')
        for case in xml_case_list:
            #print case
            casenode = xmlet.fromstring(case)
            casenode.set('enable','Y')
            casenode.set('rsd','10%')
            casenode.set('regression','10%')
            caselist_node.append(casenode)
        xmltree = xmlet.ElementTree(root) 
        xmltree.write(self.templ_xml_path)

def login_validate(user_email,passwd):
    #print 'def',sys._getframe().f_code.co_name
    txt = webreader(HAS.decode('base64','strict'))
    valid = False
    for line in txt.split("\n"):
        if user_email in line:
            passcode = line.split('|')[1].strip()
            p = passcode.decode('base64','strict').strip('\"')
            if p == passwd:
               #print 'Pass: ',user_email,passwd,p
               valid = True
            else:
               #print 'Wrong user email or password' 
               pass
    return valid

def get_req_from(login_user_mail):
    #print 'def',sys._getframe().f_code.co_name
    txt = webreader(HAS.decode('base64','strict'))
    #print txt
    req_from = ''
    for line in txt.split("\n"):
        if login_user_mail in line:
            req_from = line.split('|')[-1].strip()
            print 'req_from:',req_from
    return req_from

def get_device_label(user_mail):
    #print 'def',sys._getframe().f_code.co_name
    user_devicelabel_map_url = SRLOC.decode('base64','strict') + '/config/user-devicelabel-map'
    txt = webreader(HAS.decode('base64','strict'))
    #print txt
    user_group = ''
    for line in txt.split("\n"):
        if user_mail in line:
            user_group = line.split('|')[-1].strip()
    if '' == user_group:
        print 'EXIT: Not find group for',user_mail
        sys.exit(1)
    txt = webreader(user_devicelabel_map_url)
    device_label = ''
    for linee in txt.split("\n"):
        if user_group in linee:
            device_label = linee.split("::")[-1].strip()
    if '' == device_label:
        print 'EXIT: Not find device_label for',user_mail
        sys.exit(1)
    return device_label

def gen_combine_xml(dashboard_xml_path,combxml_path):
    #print 'def',sys._getframe().f_code.co_name
    print dashboard_xml_path,combxml_path
    combxml_root = xmlet.Element('xml')
    xmltree = xmlet.parse(dashboard_xml_path)
    xmlroot = xmltree.getroot()
    enabled_case_list = {}
    caselist_node = xmlroot.find('CaseList')
    for case_node in caselist_node.iter('case'):
        _case_attrs = {}
        if 'Y' == case_node.attrib['enable'].strip().upper():
            #_case_name = case_node.attrib['name'].strip()
            _feat_name = case_node.attrib['name'].strip()
            _case_attrs['duration'] = case_node.attrib['duration'].strip()
            _case_attrs['enable'] = 'Y'
            _case_attrs['monitor'] = case_node.attrib['monitor'].strip()
            _case_attrs['regression'] = case_node.attrib['regression'].strip()
            _case_attrs['round'] = case_node.attrib['round'].strip()
            _case_attrs['rsd'] = case_node.attrib['rsd'].strip()
            _case_attrs['timeout'] = case_node.attrib['timeout'].strip()
            #enabled_case_list[_case_name] = (_case_attrs)
            enabled_case_list[_feat_name] = (_case_attrs)
    #print 'enabled_case_list:',enabled_case_list
    valid_login = False
    essential_node = xmlroot.find('Essentials')
    node = essential_node.find('Login')
    submitter = ''
    passwd = ''
    if node is None:
        #print 'Submitter does not defined'
        submitter = raw_input('Enter user email: ')
        passwd = getpass.getpass('Enter password: ')
    else:
        child = node.find('user_email')
        if child is None or '' == child.text.strip():
            #print 'user_email does not defined'
            #submitter = getpass.getuser('Enter user email: ')
            submitter = raw_input('Enter user email: ')
            passwd = getpass.getpass('Enter password: ')
        else:
            submitter = child.text
            child = node.find('password')
            if child is None or '' == child.text.strip():
                #print 'password does not defined'
                passwd = getpass.getpass('Enter password: ')
            else:
                passwd = child.text
    valid = login_validate(submitter,passwd)
    if not valid:
        print 'EXIT: Wrong email or password'
        sys.exit(1)
    global req_from
    req_from = get_req_from(submitter)
    node = essential_node.find('Project')
    if node is None or '' == node.text.strip():
        print 'EXIT: Project does not defined'
        sys.exit(1)
    else:
        project = node.text.strip()
    device_label = get_device_label(submitter)
    #print device_label
    device = ''
    node = essential_node.find('Device')
    for child in node.findall('option'):
        if 'Y' == child.attrib['enable']:
            device = child.text.strip()
            break
    if '' == device:
        print 'EXIT: Not find enabled device'
        sys.exit(1)
    node = essential_node.find('AndroidBranch')
    for child in node.findall('option'):
        if 'Y' == child.attrib['enable']:
            android_branch = child.text.strip()
            break
    if '' == android_branch:
        print 'EXIT: Not find enabled AndroidBranch'
        sys.exit(1)
    node = essential_node.find('AndroidVersion')
    for child in node.findall('option'):
        if 'Y' == child.attrib['enable']:
            android_ver = child.text.strip()
            break
    if '' == android_ver:
        print 'EXIT: Not find enabled AndroidVersion'
        sys.exit(1)
    dist = ''
    build_name = ''
    build_number = ''
    image_link = ''
    image_md5sum = ''
    flash_image_flag = "N"
    flash_firmware_flag = "N"
    dist = android_branch + ' ' + android_ver
    node = essential_node.find('TestMode')
    pick_testmode = []
    for child in node.findall('option'):
        if 'Y' == child.attrib['enable']:
            pick_testmode.append(child.text.strip())
    if 0 == len(pick_testmode):
        print 'EXIT: At least one test mode should be picked'
        sys.exit(1)
    testmode = "|".join(pick_testmode)
    node = essential_node.find('TestImage')
    child = node.find('BuildName')
    build_name = child.text
    if build_name is None or '' == build_name.strip():
        print 'EXIT: BuildName is must'
        sys.exit(1)
    child = node.find('BuildNumber')
    build_number = child.text
    if build_number is None or '' == build_number.strip():
        print 'EXIT: BuildNumber is must'
        sys.exit(1)
    child = node.find('ImageLink')
    image_link = child.text
    #child = node.find('ImageMD5Sum')
    #image_md5sum = child.text
    node = essential_node.find('Emails')
    emails = node.text
    if emails is None or '' == emails.strip():
        print 'EXIT: Emails is must'
        sys.exit(1)
    if image_link is None or '' == image_link.strip():
        flash_image_flag = "N"
    else:
        flash_image_flag = "Y"
    optional_node = xmlroot.find('OPTIONALS')
    fwinfo_node = optional_node.find('FirmwareInfo')
    node = fwinfo_node.find('FirmwareLink')
    fw_link = node.text
    if fw_link is None or '' == fw_link.strip():
        flash_firmware_flag = "N"
    else:
        flash_firmware_flag = "Y"
    #node = fwinfo_node.find('FirmwareMD5Sum')
    #fw_md5sum = node.text
    node = optional_node.find('CompareImage')
    compare_build = node.find('BuildName').text
    node = optional_node.find('BiSectHome')
    bisechome = node.text
    node = optional_node.find('Debug')
    node.attrib['enable']
    debug_flag = node.attrib['enable']
    # start to create combine xml
    device_node = xmlet.SubElement(combxml_root,'device')
    label_node = xmlet.SubElement(device_node,'label')
    label_node.text = device_label
    label_node = xmlet.SubElement(device_node,'platform')
    label_node.text = device
    options_node = xmlet.SubElement(combxml_root,'options')
    sub_node = xmlet.SubElement(options_node,'receiver')
    sub_node.text = emails
    sub_node = xmlet.SubElement(options_node,'project')
    sub_node.text = project
    sub_node = xmlet.SubElement(options_node,'distro')
    sub_node.text = dist
    sub_node = xmlet.SubElement(options_node,'device')
    sub_node.text = device
    sub_node = xmlet.SubElement(options_node,'test_freq')
    sub_node.text = testmode
    sub_node = xmlet.SubElement(options_node,'req_from')
    sub_node.text = req_from
    sub_node = xmlet.SubElement(options_node,'build_name')
    #sub_node.text = image_uri.split('/')[-1].strip() if '/' in image_uri else image_uri
    sub_node.text = build_name
    sub_node = xmlet.SubElement(options_node,'build_number')
    sub_node.text = build_number
    sub_node = xmlet.SubElement(options_node,'build_date')
    sub_node.text = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    sub_node = xmlet.SubElement(options_node,'flash_image_flag')
    sub_node.text = flash_image_flag
    sub_node = xmlet.SubElement(options_node,'image_uri')
    sub_node.text = image_link
    #sub_node = xmlet.SubElement(options_node,'image_md5sum')
    #sub_node.text = image_md5sum
    sub_node = xmlet.SubElement(options_node,'compare_build')
    sub_node.text = compare_build
    sub_node = xmlet.SubElement(options_node,'flash_firmware_flag')
    sub_node.text = flash_firmware_flag
    sub_node = xmlet.SubElement(options_node,'firmware_uri')
    sub_node.text = fw_link
    #sub_node = xmlet.SubElement(options_node,'firmware_md5sum')
    #sub_node.text = fw_md5sum
    sub_node = xmlet.SubElement(options_node,'bisec_home')
    sub_node.text = bisechome
    sub_node = xmlet.SubElement(options_node,'debug')
    sub_node.text = debug_flag
    # Parse platform xml
    branch_url = SRLOC.decode('base64','strict') + '/config/branch.conf'
    txt = webreader(branch_url)
    dist_device = ''
    chk = device.lower()
    for line in txt.split("\n"):
        if('' == line.strip()):
            continue
        else:
            arr = line.split('|')
            find_dist = arr[0].strip() + ' ' + arr[1].strip()
            find_device = arr[2].strip().replace('_',' ')
            if find_device.upper() == device.upper() and find_dist.upper() == dist.upper():
                platform_xml = arr[3].strip()
    platformxml_url = SRLOC.decode('base64','strict') + '/platform_xml/%s' % platform_xml 
    txt = webreader(platformxml_url)
    #print 'platform txt:',txt
    platformxml_root = xmlet.fromstring(txt)
    platf_opt_node = platformxml_root.find('options')
    for child in platf_opt_node:
        options_node.append(child)
    platf_setup_node = platformxml_root.find('setup')
    combxml_root.append(platf_setup_node)
    platf_teardown_node = platformxml_root.find('teardown')
    combxml_root.append(platf_teardown_node)
    # Parse case xml
    casexml_url = SRLOC.decode('base64','strict') + '/case_xml/ats-pnp-cases.xml'
    txt = webreader(casexml_url)
    #print 'case txt:',txt
    casexml_root = xmlet.fromstring(txt)
    for feature_node in casexml_root.iter('feature'):
        find_featname = feature_node.attrib['name']
        if find_featname in enabled_case_list.keys():
            feat_attribs = feature_node.attrib
            _case_node = feature_node.find('case')
            n_feature_node = xmlet.SubElement(combxml_root,'feature')
            for k, value in feat_attribs.iteritems():
                n_feature_node.set(k, value)
            for child in feature_node:
                if 'case' == child.tag:
                    _case_attr = enabled_case_list[find_featname]
                    child.set('duration',_case_attr['duration'])
                    child.set('enable',_case_attr['enable'])
                    child.set('monitor',_case_attr['monitor'])
                    child.set('regression',_case_attr['regression'])
                    child.set('round',_case_attr['round'])
                    child.set('rsd',_case_attr['rsd'])
                    child.set('timeout',_case_attr['timeout'])
                    n_feature_node.append(child)
                else:
                    n_feature_node.append(child)
        else:
            pass
    combxmltree = xmlet.ElementTree(combxml_root) 
    combxmltree.write(combxml_path)

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
        #self._rid = 'dGVzdGJvdEBjdGktbWFzdGVyLnNoLmludGVsLmNvbSUldGVzdGJvdA==\n'
        self._rid = 'cG5wQHBucC5zaC5pbnRlbC5jb20lJXBucDEyMzQ1Ng==\n'

    def _ssh_cmd(self, cmd, timeout=1800):
        """run ssh cmd"""
        _cmd = "ssh %s %s" % (self._rid.decode('base64','strict').split('%%')[0], cmd)
        _ssh = pexpect.spawn(_cmd, timeout=timeout)
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
            _result = pexpect.run(_cmd) # if no password is needed
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
        self._version = "\nAuto Test Service\nVersion: 1.3\n"
        self._pnpats = "python /home/data2/www/AutoTestServicePy/ats_apis/trig_test.py" 

    def version(self):
        print self._version
    
    def list_template(self):
        """list template"""
        template_path = os.path.join(CUR_PATH, 'template')
        print "---------------- Avaliable Template List ---------------------"
        for _, _, files in os.walk(template_path, True):
            for name in files:
                print(os.path.join(name))
    
    def update_template(self):
        """update template"""
        templ_path = os.path.join(CUR_PATH, 'template')
        templ_xml_path = os.path.join(CUR_PATH, 'template/pnp-ats-template.xml')
        os.system('rm -f %s' % templ_xml_path)
        if not os.path.isdir(templ_path):
            os.system('mkdir -p %s' % templ_path)
        if os.path.isfile(templ_xml_path):
            print 'EXIT:',templ_xml_path,'exists'
            pass
        else:
            ats_tmpl = ats_templ_scrapor(templ_xml_path)
            ats_tmpl.mk_templ_xml()
            pretty_xml = xml_formator(templ_xml_path)
            pretty_xml.pretty_xml()
        print '--------------- Template Updated ---------------\n',templ_xml_path

    def submit_task(self,xml_path): 
        """submit test xml to PnP server"""
        xml_name = os.path.basename(xml_path)
        _randn = time.strftime("%Y%m%d%H%M%S")
        print "xml id:",_randn
        xml_name = xml_name.split("xml")[0] + _randn + ".xml"
        dst_name = '/tmp/%s' % xml_name
        usrhome = expanduser("~")
        _known_hosts = '%s/.ssh/known_hosts' % usrhome
        _ip = self._rid.decode('base64','strict').split('%%')[0].split('@')[-1]
        if os.path.exists(_known_hosts):
            rm_key_cmd = 'ssh-keygen -f %s/.ssh/known_hosts -R %s >/dev/null 2>&1' % (usrhome,_ip)
            #print 'rm_key_cmd:',rm_key_cmd
            os.popen(rm_key_cmd)
        Remotor._scp_file(self, xml_path, dst_name)
        return dst_name

    def trig_test(self,xml_path): 
        """submit and trig test by xml"""
        dst_name = self.submit_task(xml_path)
        cmd = self._pnpats + " -t " + dst_name
        msg = Remotor._ssh_cmd(self, cmd)
        print msg

    def cancel_recipe(self,recipe_id):
        """cancel recipe"""
        cmd = self._pnpats + " -c " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        print msg

    def get_recipe_state(self,recipe_id):
        """get recipe state"""
        cmd = self._pnpats + " -s " + recipe_id
        msg = Remotor._ssh_cmd(self, cmd)
        print msg

    def get_run_tasks(self):
        """get pending list"""
        cmd = self._pnpats + " -r " 
        msg = Remotor._ssh_cmd(self, cmd)
        print msg

    def get_pend_tasks(self):
        """get pending list"""
        cmd = self._pnpats + " -w " 
        msg = Remotor._ssh_cmd(self, cmd)
        print msg
    
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    option_list = [
                   make_option("-l", "--list-template", dest="list_template", action="store_true", help="List all aviliable template"),
                   make_option("-u", "--update-temp", dest="update_temp", action="store_true", help="Update templates"),
                   make_option("-t", "--trig-test", dest="test_xml", action="store", help="Trig test by xml file"),
                   make_option("-s", "--get-state", dest="state", action="store", help="Get state of task id"),
                   make_option("-c", "--cancel-task", dest="cancel_task", action="store", help="Cancel task by task id"),
                   make_option("-r", "--get-running-task", dest="run_task", action="store_true", help="List running tasks"),
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
    if options.update_temp:
        sys.exit(testservice.update_template())
    if options.test_xml:
        xml_file = options.test_xml
        testservice.trig_test(xml_file)
    if options.state:
        recipe_id = options.state
        testservice.get_recipe_state(recipe_id)
        sys.exit(0)
    if options.cancel_task:
        recipe_id = options.cancel_task
        testservice.cancel_recipe(recipe_id)
        sys.exit(0)
    if options.run_task:
        testservice.get_run_tasks()
        sys.exit(0)
    if options.wait_task:
        testservice.get_pend_tasks()
        sys.exit(0)
    if options.version:
        testservice.version()
        sys.exit(0)
