# -*- coding: utf8 -*-
import os
import sys
import time
import ftplib
import serial
import urllib2
import smtplib
import logging
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

curPath = os.path.split(os.path.realpath(__file__))[0]
acsPath = "C:/Users/buildbot/Intel/ACS/acs_fwk/src"
acsCmd_template = """C:/Python27/python.exe "C:/Users/buildbot/Intel/ACS/acs_fwk/src/ACS.py" -c "%s" -d %s -b "%s" %s"""
logging.basicConfig(level=logging.DEBUG,filename='bisect.log', filemode='w')

caseType = "power"
deviceType = "trekstor"
#caseType = "perf"
#deviceType = "lte"
#deviceType = "3gr"

serialcode = {
    "power":{"lte":"COM12","3gr":"COM12","trekstor":"COM10"},
    "perf":{"lte":"COM3","3gr":"COM3","trekstor":"COM10"}
}
compain = {
    "power":{
        "lte":".\FT\pnp\CAMPAIGN\SH_PNP_POWER_IOCARD_SLTE.xml",
        "3gr":".\FT\pnp\CAMPAIGN\SH_PNP_POWER_IOCARD_SLTE.xml",
        "trekstor":".\FT\pnp\CAMPAIGN\SH_PNP_POWER_IOCARD_SOFIA3GR.xml"
    },
    "perf":{
        "lte":".\SI\pnp\perf\CAMPAIGN\SH_PNP_PERF_IOCARD_SOFIALTE.xml",
        "3gr":".\FT\pnp\CAMPAIGN\SH_PNP_POWER_IOCARD_SLTE.xml",
        "trekstor":".\FT\pnp\CAMPAIGN\SH_PNP_POWER_IOCARD_SOFIA3GR.xml"
    }
}
device = {
    "power":{
        "lte":"SLTI20MR6-Android-M",
        "3gr":"SLTI20MR6-Android-M",
        "trekstor":"S3GR10M6S-Android-LLP"
    },
    "perf":{
        "lte":"SLTI20MR6-Android-M",
        "3gr":"SLTI20MR6-Android-M",
        "trekstor":"S3GR10M6S-Android-LLP"
    }
}
benchcfg = {
    "power":{
        "lte":".\FT\pnp\BENCHCFG\Bench_Config_Pnp_slte.xml",
        "3gr":".\FT\pnp\BENCHCFG\Bench_Config_Pnp_slte.xml",
        "trekstor":".\FT\pnp\BENCHCFG\Bench_Config_Pnp_s3gr.xml"
    },
    "perf":{
        "lte":".\SI\pnp\perf\BENCHCFG\Bench_Config_Pnp_slte.xml",
        "3gr":".\SI\pnp\perf\BENCHCFG\Bench_Config_Pnp_slte.xml",
        "trekstor":".\FT\pnp\BENCHCFG\Bench_Config_Pnp_s3gr.xml"
    }
}
arg_cr = "'--cr lab_acspnp:gtysu38/'"
versionUrl = {
    "lte":"https://mcg-depot.intel.com/artifactory/cactus-absp-jf/build/eng-builds/master/PSI/daily/",
    "3gr":"https://mcg-depot.intel.com/artifactory/cactus-absp-jf/build/eng-builds/llp_mr1/PSI/daily/",
}
template_url = {
    "lte":"https://mcg-depot.intel.com/artifactory/cactus-absp-jf/build/eng-builds/master/PSI/daily/%s/r2_sltmrdV34/userdebug/r2_sltmrdV34-flashfiles-M0l%s.zip",
    "3gr":"https://mcg-depot.intel.com/artifactory/cactus-absp-jf/build/eng-builds/llp_mr1/PSI/daily/%s/r2_s3gr10m6s/userdebug/r2_s3gr10m6s-flashfiles-L1l%s.zip"
}

def checkADB(casetype,deviceType):
    while 1:
        if os.system("adb root")==0:
            print "root success!"
        time.sleep(1)
        devices = os.popen("adb devices")
        if len(devices.readlines()) > 2:
            break
        else:
            ser = serial.Serial(serialcode[casetype][deviceType], 19200, timeout=1)
            ser.write("j")
            ser.close()
    print "adb ok!"

def unzipImage(imageName):
    print "unzip image..."
    import zipfile
    os.chdir(curPath)
    if not os.path.exists("C:/Temp/flashimage"):
        os.mkdir("C:/Temp/flashimage")
    for flsFile in os.listdir("C:/Temp/flashimage"):
        if os.path.isfile(flsFile):
            try:
                os.remove(flsFile)
            except:
                pass
    zfile = zipfile.ZipFile(imageName,'r')
    for filename in zfile.namelist():
        zfile.extract(filename,"C:/Temp/flashimage")
            
def flashImage(casetype,deviceType,imageName):
    print "flash image..."
    logging.info("flash image: " + imageName)
    if not os.path.exists(imageName):
        print "Image File : %s not exists." % (imageName)
        return False
    checkADB(casetype,deviceType)
    cmd = 'adb reboot & C:/"Program Files (x86)"/Intel/"Phone Flash Tool"/DownloadTool.exe --verbose 4 -c USB1 "C:/Temp/flashimage/psi_flash_signed.fls" "C:/Temp/flashimage/slb_signed.fls" "C:/Temp/flashimage/mobilevisor_signed.fls" "C:/Temp/flashimage/oem_signed.fls" "C:/Temp/flashimage/boot_signed.fls" "C:/Temp/flashimage/cache_signed.fls" "C:/Temp/flashimage/secvm_signed.fls" "C:/Temp/flashimage/splash_img_signed.fls" "C:/Temp/flashimage/system_signed.fls" "C:/Temp/flashimage/userdata_signed.fls" "C:/Temp/flashimage/recovery_signed.fls" "C:/Temp/flashimage/fwu_image_signed.fls" "C:/Temp/flashimage/mvconfig_smp_signed.fls" "C:/Temp/flashimage/ucode_patch_signed.fls"'
    if os.system(cmd) == 0:
        time.sleep(600)
        return True
    return False
def runACS(casetype,deviceType):
    print "run acs..."
    acsCmd = acsCmd_template % (campaign[casetype][deviceType],device[casetype][deviceType],benchcfg[casetype][deviceType],arg_cr)
    os.chdir(acsPath)
    print acsCmd
    os.system(acsCmd)
def getPerformance(xmlfile):
    from xml.etree import ElementTree
    with open(xmlfile,'r') as f:
        root = ElementTree.fromstring(f.read())
        sub_nodes = root.findall("Test_Result")
        for sub_node in sub_nodes:
            lst_node = sub_node.findall("Test")
            for node in lst_node:
                score = node.find("Test_Comment").text.split("-")[2].split(":")[1].split(" ")[1]
                return float(score)
def getResult():
    rPath = "C:/Users/buildbot/Intel/ACS/acs_fwk/src/_Reports"
    curReport = [p for p in os.listdir(rPath) if os.path.isdir(os.path.join(rPath,p))][-1]
    rFile = os.path.join(rPath,curReport,"extTestResult.xml")
    if os.path.exists(rFile):
        return getPerformance(rFile)
    return 0

def UpdateReleaseInfo(newversion):
    releases = map(lambda x:x.strip()+'\n',open("logs/release_info.log",'r').readlines())
    releases.append(newversion)    
    open("logs/release_info.log",'w').writelines(releases)

def SendEmail(msgTo,mailContent):
    msg = MIMEMultipart()
    msg['From'] = 'zhaowangx.liang@intel.com'
    msg['To'] = msgTo
    msg['Cc'] = 'zhaowangx.liang@intel.com'
    msg['Subject'],content = "Auto run ACS failed",mailContent
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    try:
        smtp = smtplib.SMTP('OutlookSH.intel.com', 25)
        smtp.starttls()
        smtp.login(msg['From'], 'lzw,123,1')
        smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
    except Exception,e:
        print e
        
def Start(casetype,deviceType):
    try:
        imageList = ["coho-flashfiles-MMR100540.zip","coho-flashfiles-MMR100550.zip","coho-flashfiles-MMR100560.zip","coho-flashfiles-MMR100570.zip","coho-flashfiles-MMR100590.zip","coho-flashfiles-MMR100520.zip"]
        for imageName in imageList:
            unzipImage("images/" +imageName)
            if flashImage(casetype,deviceType,imageName):
                runACS(casetype,deviceType)
            else:
                print("Flash Image failed: %s" % (imageName))
                logging.info("Flash Image failed: %s" % (imageName))
    except Exception as e:
        import traceback
        print traceback.format_exc()
        SendEmail("zhaowangx.liang@intel.com","<label>Auto Run ACS failed!!!!</label><br/><br/><pre>%s</pre>"%(traceback.format_exc()))
        
if __name__=='__main__':
    Start(caseType,deviceType)
    #flashImage(caseType,deviceType,"images/r2_s3gr10m6s-flashfiles-L1l000283.zip")
    #unzipImage("r2_s3gr10m6s-flashfiles-L1l000215.zip")
    #print flashImage("r2_s3gr10m6s-flashfiles-L1l000215.zip")
    #checkNewVersion()
    #runACS("power",)
    #getResult()
