#!/bin/bash

pre_int_no=$2
device=$4
#save_files_to="/var/lib/tomcat7/webapps/ROOT/preInt_build/"
save_files_to=`head -1 ./settings/image_config.txt`
#image_addr="http://sxy-precision-t1700.sh.intel.com:8080/preInt_build"
image_addr=`tail -1 ./settings/image_config.txt`
case $device in
"TREKSTOR" | "CLOUDFONE")
	#echo "COHO is selected"
	image_folder="coho";;
"ECS27B" | "ECS210A" | "ECS28A" | "CHIPHD8" | "MALATA8")
	#echo "COHOL is selected"
	image_folder="cohol";;
*) 
	echo "ERROR"
	echo "no such deivces"
	exit 1;;
esac

#image_name="$image_folder-flashfiles-$device-$systembase.zip"
#image_name="$image_folder-flashfiles-$device-gmin_l_mr1-prei-$pre_int_no.zip"
image_name="$image_folder-flashfiles-$device-llp_mr1_r1-prei-$pre_int_no.zip"
echo $image_address
if [ -f $save_files_to/$image_name ];then
	echo "OK"
	echo "$image_addr/$image_name"
	echo `cat $save_files_to/$image_name.md5 | awk '{print $1}'`
	if [ $device == "TREKSTOR" ];then
		echo "http://chuzhul-ubuntu.sh.intel.com:8080/GMIN/factory/gminL100790/L100790_TREKSTOR/trekstor_ifwi.bin"
		echo "4078c552735afb8d07a2f05925665c30"
	else
		echo "http://chuzhul-ubuntu.sh.intel.com:8080/GMIN/factory/gminL100790/L100790_ECS210A/ecs210a_ifwi.bin"
		echo "bde7bd7dd7c8076bf4f7a9743b1df846"
	fi
else
	echo "ERROR"
	echo "can not get Image"
	exit 1
fi

