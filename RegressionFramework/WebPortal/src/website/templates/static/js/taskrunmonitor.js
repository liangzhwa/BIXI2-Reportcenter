'use strict';
var serverHost = window.location.host;
var domainid = -1;
var tid = GetQueryString("tid");
$(document).ready(function(){
    initTaskRunDevicesList();
    initTaskRunImagesList();
    initTaskRunList();
});

function initTaskRunDevicesList(){
    var url = "http://"+serverHost+"/rest/gettaskrundevices";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var sltStr = "<option value='-1'>---Select Device---</option>"
            var devices = JSON.parse(data)["devices"];
            for(var index in devices){
                sltStr += "<option value='"+devices[index][0]+"'>" + devices[index][1] + "</option>";
            }
            $("#sltDevice").html(sltStr);
        }
    });
}
function initTaskRunImagesList(){
    var url = "http://"+serverHost+"/rest/gettaskrunimages";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var images = JSON.parse(data)["images"];
            var sltStr = "<option value='-1'>---Select Image---</option>"
            for(var index in images){
                sltStr += "<option>" + images[index] + "</option>";
            }
            $("#sltImage").html(sltStr);
        }
    });
}
function initTaskRunList(){
    var url = "http://"+serverHost+"/rest/gettaskrunlist?1=1";
    if(tid != null){ url += "&tid=" + tid; }
    if($("#sltDevice").val() != null && $("#sltDevice").val() != "-1"){ url += "&device=" + $("#sltDevice").val(); }
    if($("#sltImage").val() != null && $("#sltImage").val() != "-1"){ url += "&image=" + $("#sltImage option:selected").text(); }
    if($("input[name='rgFilter']:checked").val() != "-1"){ url += "&status=" + $("input[name='rgFilter']:checked").val(); }
    
    console.log(url);
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["taskrun"];
            var status = JSON.parse(data)["status"];
            var strItems = "";
            var statusObj = {};
            
            for(var j=0;j<status.length;j++){
                statusObj[status[j][2]] += "<status"+status[j][3]+">"+status[j][1]+"</status"+status[j][3]+">";
            }
            for(var i=0;i<items.length;i++){
                var statusStr = "";
                var tmpStr = "";
                var runimg = "";
                var tIndex = items[i][0].indexOf(":");
                var device = items[i][0].substr(0,tIndex);
                var deploy = items[i][0].substr(tIndex+1);
                var tempStatus = statusObj[items[i][4]];
                var finishedKpiNum = items[i][6];
                var totalKpiNum = items[i][7];
                var pnprolename = items[i][8];
                if(tempStatus){
                    statusStr = "<div id='process' style='width:706px;'>"
                    if(tempStatus.indexOf("<status1>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status1").text();
                        statusStr += "<div class='node ready'><ul><li class='tx1'> </li><li class='tx2'>Trigged</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else{
                        statusStr += "<div class='node unready'><ul><li class='tx1'> </li></ul></div>";
                    }
                    
                    if(tempStatus.indexOf("<status2>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status2").text();
                        tmpStr = "Running";
                        runimg = "process";
                        statusStr += "<div class='proce ready'><ul><li class='tx4'>Queuing To Testbot</li></ul></div>";
                        statusStr += "<div class='node ready'><ul><li class='tx1'> </li><li class='tx2'>Started</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else{
                        tmpStr = "Waiting";
                        runimg = "unready";
                        statusStr += "<div class='proce unready'><ul><li class='tx4'>Queuing To Testbot</li></ul></div>";
                        statusStr += "<div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Started</li></ul></div>";
                    }
                    if(tempStatus.indexOf("<status3>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status3").text();
                        statusStr += "<div class='proce ready'><ul><li class='tx1'>Breaked("+finishedKpiNum+"/"+totalKpiNum+")</li></ul></div>";
                        statusStr += "<div class='node failed'><ul><li class='tx1'> </li><li class='tx2'>Run Failed</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else if(tempStatus.indexOf("<status4>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status4").text();
                        statusStr += "<div class='proce ready'><ul><li class='tx1'>Finished("+finishedKpiNum+"/"+totalKpiNum+")</li></ul></div>";
                        statusStr += "<div class='node ready'><ul><li class='tx1'> </li><li class='tx2'>Finished</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else{
                        statusStr += "<div class='proce "+runimg+"'><ul><li class='tx1'>"+tmpStr+"("+finishedKpiNum+"/"+totalKpiNum+")</li></ul></div>";
                        statusStr += "<div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Finished</li></ul></div>";
                    }
                    if(tempStatus.indexOf("<status6>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status6").text();
                        statusStr += "<div class='proce ready'><ul><li class='tx4'>Queuing To DB</li></ul></div>";
                        statusStr += "<div class='node ready'><ul><li class='tx1'> </li><li class='tx2'>Saved To DB</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else if(tempStatus.indexOf("<status5>") > -1){
                        var datestamp = $("<root>"+tempStatus.replace(/undefined/g,'')+"</root>").find("status5").text();
                        statusStr += "<div class='proce ready'><ul><li class='tx4'>Queuing To DB</li></ul></div>";
                        statusStr += "<div class='node failed'><ul><li class='tx1'> </li><li class='tx2'>Get Data Failed</li><li class='tx3'>"+datestamp.split(' ')[0]+"<br/>"+datestamp.split(' ')[1]+"</li></ul></div>";
                    }else{
                        statusStr += "<div class='proce unready'><ul><li class='tx4'>Queuing To DB</li></ul></div>";
                        statusStr += "<div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Saved To DB</li></ul></div>";
                    }
                    statusStr += "</div>";
                }else{
                    statusStr = "<div id='process' style='width:706px;'><div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Trigged</li></ul></div><div class='proce unready'></div><div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Started</li></ul></div><div class='proce unready'></div><div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Finished</li></ul></div><div class='proce unready'></div><div class='node unready'><ul><li class='tx1'> </li><li class='tx2'>Saved To DB</li></ul></div></div>"
                }
                strItems += "<tr tid='"+items[i][4]+"' pid='"+items[i][5]+"'><td>"+items[i][1]+"</td><td>"+device+"</td><td>"+pnprolename+"<br/><button class='btn btn-xs' onclick='ShowKPI(this)'>Show KPI</button></td><td>"+deploy+"</td><td>"+items[i][2]+"</td><td>"+statusStr+"</td></tr>";
            }
            if(tid != null){
                $("#title").html("Task Run List: " + items[0][0])
            }
            $("#taskrunlist").html(strItems);
        }
    });
}

function ShowKPI(obj){
    if($(obj).html() == "Show KPI"){
        var pnprole = $(obj).parent().parent().attr("pid");
        var url = "http://"+serverHost+"/rest/getkpilistbypnprole?pnprole="+pnprole
        $(obj).html("Hide KPI");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                var items = JSON.parse(data)["result"];
                var strKpis = "<tr><td colspan=6>";
                for(var i=0;i<items.length;i++){
                    strKpis += "<label style='margin-left:15px;'><input type='checkbox' value='"+items[i][0]+"' checked/>"+items[i][1].split("#")[2]+"</label>"
                }
                strKpis += "</td></tr>"
                $(obj).parent().parent().after(strKpis);
            }
        });        
    }else{
        $(obj).html("Show KPI");
        $(obj).parent().parent().next().remove();
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
function GetDatetime(content,status){
    alert(content);
    var pattern = /<status1>(.+)<status1>/ig;
    var result = pattern.exec(content);
    alert(result);
        return result;
   
}