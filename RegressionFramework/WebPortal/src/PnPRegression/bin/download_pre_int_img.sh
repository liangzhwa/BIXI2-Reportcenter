#!/bin/bash

pre_int_no=$1
device=$2
save_files_to=`head -1 ./settings/image_config.txt`
user_name=`head -1 ./settings/user_info.txt`
pass_word=`tail -1 ./settings/user_info.txt`
echo "pre_int_no=$pre_int_no"
echo "device=$device"
case $device in
"TREKSTOR" | "CLOUDFONE")
	#echo "COHO is selected"
	image_folder="coho";;
"ECS27B" | "ECS210A" | "ECS28A" | "CHIPHD8" | "MALATA8")
	#echo "COHOL is selected"
	image_folder="cohol";;
*) 
	echo "ERROR!!! no such deivces"
	exit 1;;
esac

#image_name="$image_folder-flashfiles-$device-llp_mr1_r1-prei-$pre_int_no.zip"
#image_address="https://jfstor001.jf.intel.com/artifactory/simple/otc-jf/cactus/gmin_l_mr1/gmin_l_mr1-preintegration/$pre_int_no/$image_folder/userdebug/$image_name"
image_name="$image_folder-flashfiles-$device-L1p000$pre_int_no.zip"
image_address="https://mcg-depot.intel.com/artifactory/cactus-absp-tl/llp_mr1-preintegration/$pre_int_no/$image_folder/userdebug/$image_name"
echo $image_name
echo $image_address
if [ -f $save_files_to/$image_name ];then
	echo "file ready exsist no need download"
else
	wget -P $save_files_to $image_address --http-user $user_name --http-passwd $pass_word --no-check-certificate
	wget_ret_value=$?	
	if [ $wget_ret_value -eq 0 ];then
		echo "download OK"
	else
		echo "download ERROR wget_ret_value=$wget_ret_value"
		exit 1
	fi
fi

md5sum $save_files_to/$image_name > $save_files_to/$image_name.md5
if [ $? -eq 0 ];then
	echo "MD5 OK"
else
	echo "MD5 ERROR"
	exit 1
fi


