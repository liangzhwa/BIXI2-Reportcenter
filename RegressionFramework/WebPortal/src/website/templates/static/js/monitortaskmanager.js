'use strict';
var serverHost = window.location.host;
var taskid="-1";
$(document).ready(function(){
    initTaskList();
    initReleasetypeList();
    initDeployedDeviceList();
    $("#newtask").dialog({
        width:400,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            
        }
    });
});

function initReleasetypeList(){
    var url = "http://"+serverHost+"/rest/getmonitoeredreleasetypeforweb";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#t_sltReleasetype").html(strItems);
        }
    });
}
function initDeployedDeviceList(){
    var url = "http://"+serverHost+"/rest/getdeployeddevicelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][9]+">"+items[i][0] +" - "+items[i][1] +" - "+items[i][2] +" - "+items[i][3] +"</option>";
            }
            $("#t_sltDeployedDevice").html(strItems);
        }
    });
}
function initTaskList(){
    var url = "http://"+serverHost+"/rest/gettasklist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                var ismonitor = items[i][8] == "1" ? "True":"False";
                strItems += "<tr tid='"+items[i][0]+"'><td ddid='"+items[i][6]+"'>"+items[i][1]+"</td><td>"+items[i][2]+"</td><td>"+items[i][3]+"</td><td>"+items[i][4]+"</td><td rtid='"+items[i][7]+"'>"+items[i][5]+"</td><td>"+ismonitor+"</td><td style='width:150px'><a class='btn btn-xs' href='http://"+serverHost+"/taskrunmonitor?tid="+items[i][0]+"' target='_blank'>Show History</a><button class='btn btn-xs' style='margin-left:10px;' onclick='EditTask(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteTask(this)'>Delete</button></td></tr>";
            }
            $("#tasklist").html(strItems);
        }
    });
}

function SaveTask(){
    var devicedeployid = $("#t_sltDeployedDevice").val();
    var releasetypeid = $("#t_sltReleasetype").val();
    var ismonitor = $("#t_ismonitor").prop("checked") ? "1":"0";
    if(devicedeployid=="" || releasetypeid==""){ alert("please input the requried field."); return;}
    
	var url = "";
    var record = { };
    if(taskid == "-1"){
		url = "http://"+serverHost+"/rest/newtask";
		record = { "devicedeploy":devicedeployid,"releasetype":releasetypeid,"ismonitor":ismonitor };
	}else{
		url = "http://"+serverHost+"/rest/edittask";
		record = { "tid":taskid,"devicedeploy":devicedeployid,"releasetype":releasetypeid,"ismonitor":ismonitor };
	}
    $.ajax({
        type: 'POST',
		data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            initTaskList();
            CloseTaskWindow();
        }
    });
}

function AddNewTask(){
    taskid="-1";
    $("#newtask").dialog("open");
}

function ShowHistory(obj){
    taskid = $(obj).parent().parent().attr("tid");
    //self.location = "http://10.239.93.157:9900/taskrunmonitor?tid=";
    //window.navigate("http://10.239.93.157:9900/taskrunmonitor?tid="); 
}
function EditTask(obj){
    taskid = $(obj).parent().parent().attr("tid");
    $("#t_sltDeployedDevice").val($(obj).parent().parent().find("td:eq(0)").attr("ddid"));
    $("#t_sltReleasetype").val($(obj).parent().parent().find("td:eq(4)").attr("rtid"));
    $(obj).parent().parent().find("td:eq(5)").html() == "True" ? $("#t_ismonitor").prop("checked",true):("#t_ismonitor").prop("checked",false);
    $("#newtask").dialog("open");
}
function DeleteTask(obj){
	if(confirm('Are you sure to delete it?')){
        var tid = $(obj).parent().parent().attr("tid");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletetask?tid="+tid,
            success: function(data) {
                initTaskList();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function CloseTaskWindow(){
    $("#newtask").dialog("close");
}

function checkall(obj){
    if($(obj).prop("checked")){
        $("#tbTestData tr td input").prop("checked",true);
    }else{
        $("#tbTestData tr td input").prop("checked",false);
    }
}
function removeBlank(str){
    str=str.replace(/(\s+$)|(^\s+)/g,"");
    str=str.replace(/\s+/g," ");
    return str;
}
function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}