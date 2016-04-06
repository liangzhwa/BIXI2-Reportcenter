#!/bin/bash
#
# Fetch job from Web Portal and Feed to TestBot
#

release_no=$1
device_name=$2
release_id=$3 
folder_pull_requests="./logs/$release_no""_PullRequests"
folder_jira_json="./logs/$release_no""_PullRequests/log_jira_json"
log_xml4testbot="$folder_pull_requests/preInt_xml4testbot.log"
log_recipe_pnp="$folder_pull_requests/preInt_recipe_pnp.log"
user_name=`head -1 ./settings/user_info.txt`
pass_word=`tail -1 ./settings/user_info.txt`
task_info_list="$folder_pull_requests/task_info_list.xml"
task_id_device_set_list="$folder_pull_requests/task_id_device_set_list.txt"

echo "PnP Regression info: $release_no $device_name"
date +%Y-%m-%d-%H:%M:%S

case $device_name in
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

rm $task_id_device_set_list
wget -O ./$task_info_list --no-proxy  http://10.239.93.157:9900/rest/getxmlforbisecttask?releaseid=$release_id
if [ $? -eq 0 ];then
	echo "$task_info_list download success"
	python ./bin/gen_id_device_set_list.py $task_info_list $task_id_device_set_list && echo "list task_id_device_set_list..." && cat $task_id_device_set_list
	cat $task_id_device_set_list | while task_id_device_set_list_line=$(line)
	do
		task_id=`echo $task_id_device_set_list_line |awk -F ' ' '{print $1}'`
		device_name=`echo $task_id_device_set_list_line |awk -F ' ' '{print $2}'`
		test_set=`echo $task_id_device_set_list_line |awk -F ' ' '{print $3}'`
        preint_no=`echo $task_id_device_set_list_line |awk -F ' ' '{print $4}'`
		python ./bin/gen_xml4testbot_preInt.py $release_no $preint_no $device_name $task_id $log_xml4testbot
    done
else
	echo "ERROR cannot download task_info_list!!! "
fi

#exit 1

cat $log_xml4testbot | sort | uniq > $folder_pull_requests/regression_test_$release_no.list
echo "Finished!!!"
#exit 1
echo "feeding PnP xml to TestBot"

cat $folder_pull_requests/regression_test_$release_no.list | while myline=$(line)
do
	echo "LINE:"$myline
	recipe_id=`python ats.py -t $folder_pull_requests/$myline | grep recipe_id | awk '{print $3}'`
	if [ "$recipe_id" == "" ];then 
		echo "ERROR: can not start testbot!!! $myline"
		echo "$myline NONE" >> $log_recipe_pnp
	else
		echo "Testbot start success $myline recipe_id = $recipe_id"
		echo "$myline $recipe_id" >> $log_recipe_pnp
		wget -P ./logs/$current_release --no-proxy http://10.239.93.157:9900/rest/newrecipemonitor?release=$current_release\&device=$device_name\&recipeid=$recipe_id\&taskid=$task_id\&isbisect=1
	fi
done
