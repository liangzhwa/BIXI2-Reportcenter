'use strict';
var serverHost = window.location.host;
var deviceid="-1";
$(document).ready(function(){
    initDeviceList();
    initPlatformList();
    initDeviceTypeList();
    $("#newdevice").dialog({
        width:400,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#d_name").val("");
            $("#d_remark").val("");
        }
    });
    $("#newplatform").dialog({
        width:400,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#p_name").val("");
        }
    });
});

function initPlatformList(){
    var url = "http://"+serverHost+"/rest/getplatformlist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#d_sltPlatform").html(strItems);
        }
    });
}
function initDeviceTypeList(){
    var url = "http://"+serverHost+"/rest/getdevicetypelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#d_sltDeviceType").html(strItems);
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
                strItems += "<tr dId='"+items[i][0]+"'><td>"+items[i][1]+"</td><td pid='"+items[i][6]+"'>"+items[i][3]+"</td><td tid='"+items[i][5]+"'>"+items[i][2]+"</td><td>"+items[i][4]+"</td><td style='width:150px'><button class='btn btn-xs' onclick='EditDevice(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteDevice(this)'>Delete</button></td></tr>";
            }
            $("#devicelist").html(strItems);
        }
    });
}

function SaveDevice(){
    var name = $("#d_name").val();
    var devicetypeid = $("#d_sltDeviceType").val();
    var platformid = $("#d_sltPlatform").val();
    var remark = $("#d_remark").val();
    if(name=="" || devicetypeid=="" || platformid==""){ alert("please input the requried field."); return;}
    
	var url = "";
    var record = { };
    if(deviceid == "-1"){
		url = "http://"+serverHost+"/rest/newdevice";
		record = { "name":name,"devicetype":devicetypeid,"platform":platformid,"remark":remark };
	}else{
		url = "http://"+serverHost+"/rest/editdevice";
		record = { "did":deviceid,"name":name,"devicetype":devicetypeid,"platform":platformid,"remark":remark };
	}
    $.ajax({
        type: 'POST',
		data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            initDeviceList();
            CloseDeviceWindow();
        }
    });
}
function SavePlatform(){
    var name = $("#p_name").val();
    var url = "http://"+serverHost+"/rest/newplatform?name="+name
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            ClosePlatformWindow();
        }
    });
}

function AddNewDevice(){
    deviceid="-1";
    $("#newdevice").dialog("open");
}
function AddNewPlatform(){
    $("#newplatform").dialog("open");
}
function EditDevice(obj){
    deviceid = $(obj).parent().parent().attr("did");
    $("#d_name").val($(obj).parent().parent().find("td:eq(0)").html());
    $("#d_sltDeviceType").val($(obj).parent().parent().find("td:eq(2)").attr("tid"));
    $("#d_sltPlatform").val($(obj).parent().parent().find("td:eq(1)").attr("pid"));
    $("#d_remark").val($(obj).parent().parent().find("td:eq(3)").html());
     $("#newdevice").dialog("open");
}
function DeleteDevice(obj){
	if(confirm('Are you sure to delete it?')){
        var did = $(obj).parent().parent().attr("did");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletedevice?did="+did,
            success: function(data) {
                initDeviceList();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function CloseDeviceWindow(){
    $("#newdevice").dialog("close");
}
function ClosePlatformWindow(){
    $("#newplatform").dialog("close");
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
