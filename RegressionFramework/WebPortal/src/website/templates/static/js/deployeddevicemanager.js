'use strict';
var serverHost = window.location.host;
var deployid = -1;
$(document).ready(function(){
    initDeployedDeviceList();
    initPnpRoleList();
    initDeviceList();
    $("#newdeploydevice").dialog({
        width:400,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#d_ip").val("");
            $("#d_sn").val("");
            $("#d_bbcode").val("");
            $("#d_site").val("");
            $("#d_room").val("");
        }
    });
});

function initDeployedDeviceList(){
    var url = "http://"+serverHost+"/rest/getdeployeddevicelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<tr did='"+items[i][9]+"'><td deviceid='"+items[i][7]+"'>"+items[i][0]+"</td><td pnproleid='"+items[i][8]+"'>"+items[i][1]+"</td><td>"+items[i][2]+"</td><td>"+items[i][3]+"</td><td>"+items[i][4]+"</td><td>"+items[i][5]+"</td><td>"+items[i][6]+"</td><td style='width:150px;'><button class='btn btn-xs' onclick='EditDeploy(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteDeploy(this)'>Delete</button></td></tr>";
            }
            $("#deployeddevicelist").html(strItems);
        }
    });
}

function initDeviceList(){
    var url = "http://"+serverHost+"/rest/getdevicelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value='"+items[i][0]+"'>"+items[i][1]+"</option>";
            }
            $("#d_sltDevice").html(strItems);
        }
    });
}
function initPnpRoleList(){
    var url = "http://"+serverHost+"/rest/getpnprolelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#d_sltPnpRole").html(strItems);
        }
    });
}

function SaveDeployDevice(){
    var deviceid = $("#d_sltDevice").val();
    var pnproleid = $("#d_sltPnpRole").val();
    var ip = $("#d_ip").val();
    var sn = $("#d_sn").val();
    var bbcode = $("#d_bbcode").val();
    var site = $("#d_site").val();
    var room = $("#d_room").val();
    if(deviceid=="" || pnproleid==""){ alert("please input the requried field."); return;}
    if(deployid == "-1"){
        var url = "http://"+serverHost+"/rest/newdeploydevice?deviceid="+deviceid+"&pnproleid="+pnproleid+"&ip="+ip+"&sn="+sn+"&bbcode="+bbcode+"&site="+site+"&room="+room
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                CloseDeployDeviceWindow();
                initDeployedDeviceList();
            }
        });
    }else{
        var url = "http://"+serverHost+"/rest/editdeploy?did="+deployid+"&deviceid="+deviceid+"&pnproleid="+pnproleid+"&ip="+ip+"&sn="+sn+"&bbcode="+bbcode+"&site="+site+"&room="+room
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                CloseDeployDeviceWindow();
                initDeployedDeviceList();
            }
        });
    }
}
function SavePlatform(){
    var name = $("#p_name").val();
    var url = "http://"+serverHost+"/rest/newplatform?name="+name
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            console.log(data);
        }
    });
}

function AddNewDeployDevice(){
    deployid = "-1";
    $("#newdeploydevice").dialog("open");
}
function CloseDeployDeviceWindow(){
    $("#newdeploydevice").dialog("close");
}

function EditDeploy(obj){
    deployid = $(obj).parent().parent().attr("did");
    $("#d_sltDevice").val($(obj).parent().parent().find("td:eq(0)").attr("deviceid"));
    $("#d_sltPnpRole").val($(obj).parent().parent().find("td:eq(1)").attr("pnproleid"));
    $("#d_ip").val($(obj).parent().parent().find("td:eq(2)").html());
    $("#d_sn").val($(obj).parent().parent().find("td:eq(3)").html());
    $("#d_bbcode").val($(obj).parent().parent().find("td:eq(4)").html());
    $("#d_site").val($(obj).parent().parent().find("td:eq(5)").html());
    $("#d_room").val($(obj).parent().parent().find("td:eq(6)").html());
    $("#newdeploydevice").dialog("open");
}
function DeleteDeploy(obj){
    if(confirm('Are you sure to delete it?')){
        var did = $(obj).parent().parent().attr("did");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletedeploy?did="+did,
            success: function(data) {
                $(obj).parent().parent().remove();
            }
        });
    }
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
