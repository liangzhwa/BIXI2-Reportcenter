#!/bin/bash


user_name=`head -1 ./settings/user_info_wiki.txt`
pass_word=`tail -1 ./settings/user_info_wiki.txt`

http_address=$1
save_files_to=$2
echo $http_address
if [ -f $save_files_to/$image_name ];then
	echo "file ready exsist no need download"
else
	wget -P $save_files_to $http_address --http-user $user_name --http-passwd $pass_word
	wget_ret_value=$?	
	if [ $wget_ret_value -eq 0 ];then
		echo "download OK"
	else
		echo "download ERROR wget_ret_value=$wget_ret_value"
		exit 1
	fi
fi


