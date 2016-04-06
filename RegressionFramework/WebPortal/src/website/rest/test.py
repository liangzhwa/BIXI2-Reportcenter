import subprocess
import os

curWorkPath = os.getcwd()
print curWorkPath
os.chdir("../../PnPRegression")
subprocess.Popen(["sh","start_regression_test","L1R101280","TREKSTOR","176"])
os.chdir(curWorkPath)
print os.getcwd()
print "----------------no block-------------------"