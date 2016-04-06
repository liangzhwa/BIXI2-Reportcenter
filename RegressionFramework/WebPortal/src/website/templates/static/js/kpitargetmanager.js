'use strict';
var serverHost = window.location.host;
var currentFeature = "All";
$(document).ready(function(){
    initDeviceList();
    initKpiList();
    $("#newtarget").dialog({
        width:450,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#d_name").val("");
            $("#d_remark").val("");
        }
    });
});

function initDeviceList(){
    var url = "http://"+serverHost+"/rest/getdevicelistwithtarget";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>-----------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#sltDevice").html(strItems);
        }
    });
}
function initDeviceWithTargetList(){
    var url = "http://"+serverHost+"/rest/getdevicelistwithtarget";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>-----------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#t_sltSourceDevice").html(strItems);
        }
    });
}
function initDeviceWithoutTargetList(){
    var url = "http://"+serverHost+"/rest/getdevicelistwithouttarget";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>-----------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#t_sltTargetDevice").html(strItems);
        }
    });
}
function initKpiList(){
    var url = "http://"+serverHost+"/rest/getkpilist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>-----------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#sltKpi").html(strItems);
        }
    });
}

function ShowTargetByDeviceKpi(){
    var con = "";
    if($("#sltDevice").val() == "-1"){
        alert("Please select the device!");
        return
    }else{
        $("#devicetitle").html("KPI Target List: "+$("#sltDevice option:selected").text())
        con += "?device=" + $("#sltDevice").val();
    }
    if($("#sltKpi").val() != "-1"){ con += "&kpi=" + $("#sltKpi").val(); }
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/gettargetlist"+con,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<tr tid='"+items[i][0]+"'><td testcasename='"+items[i][8]+"'>"+items[i][1]+"</td><td>"+items[i][2]+"</td><td><input value='"+items[i][3]+"'/></td><td><input value='"+items[i][4]+"' /></td><td><input value='"+items[i][5]+"' /></td><td><input value='"+items[i][6]+"' /></td><td><input value='"+items[i][7]+"' /></td><td><input value='"+items[i][8]+"' /></td><td><button class='btn btn-xs' onclick='SaveKPITarget(this)'>Save</button></td></tr>";
            }
            $("#targetlist").html(strItems);
            $("#targetlist input").css("width",100);
            FilterFeature(currentFeature);
        }
    });
}

function SaveTarget(){
    var sourceDevice = $("#t_sltSourceDevice").val();
    var targetDevice = $("#t_sltTargetDevice").val();

    if(sourceDevice=="-1" || targetDevice=="-1"){ alert("please input the requried field."); return; }
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/copytarget?sourcedevice="+sourceDevice+"&targetdevice="+targetDevice,
        success: function(data) {
            CloseTargetWindow();
        }
    });
}

function SaveKPITarget(obj){
    var tid = $(obj).parent().parent().attr("tid");
    var target = $(obj).parent().parent().find("input:eq(0)").val().replace(/,/g,"");
    var margin = $(obj).parent().parent().find("input:eq(1)").val().replace(/,/g,"");
    var rsd = $(obj).parent().parent().find("input:eq(2)").val().replace(/,/g,"");
    var tt1 = $(obj).parent().parent().find("input:eq(3)").val().replace(/,/g,"");
    var tt2 = $(obj).parent().parent().find("input:eq(4)").val().replace(/,/g,"");
    var tt3 = $(obj).parent().parent().find("input:eq(5)").val().replace(/,/g,"");
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/edittarget?tid="+tid+"&target="+target+"&margin="+margin+"&rsd="+rsd+"&tt1="+tt1+"&tt2="+tt2+"&tt3="+tt3,
        success: function(data) {
            CloseTargetWindow();
        }
    });
}

function AddTargetForDevice(){
    initDeviceWithTargetList();
    initDeviceWithoutTargetList();
    $("#newtarget").dialog("open");
}
function CloseTargetWindow(){
    $("#newtarget").dialog("close");
}

function FilterFeature(featurename){
    currentFeature = featurename;
    FilterData();
}
function FilterData(){
    $("#targetlist tr td:nth-child(1)").each(function(i){
        if(currentFeature != "All" && $(this).attr("testcasename").split("#")[0] != currentFeature){
            $(this).parent().hide();
        }else{
            $(this).parent().show();
        }
    });
}

function removeBlank(str){
    str=str.replace(/(\s+$)|(^\s+)/g,"");
    str=str.replace(/\s+/g," ");
    return str;
}
