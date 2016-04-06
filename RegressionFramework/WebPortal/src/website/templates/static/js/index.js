'use strict';
var serverHost = window.location.host;

$(document).ready(function(){
    initDeviceList();
    initKpiList();
});

function ShowDeviceView(){
    $("#releaseview").hide();
    $("#kpiview").hide();
    $("#deviceview").show();
    initDeviceList();
    initKpiList();
}
function ShowReleaseView(){
    $("#deviceview").hide();
    $("#kpiview").hide();
    $("#releaseview").show();
    //initDeviceList();
    //initKpiList();
}
function ShowKpiView(){
    $("#deviceview").hide();
    $("#releaseview").hide();
    $("#kpiview").show();
    //initDeviceList();
    //initKpiList();
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
                strItems += "<label class='radio-inline' style='margin-right:20px;'><input type='radio' name='device' value='"+items[i][0]+"' style='margin-top:1px;'>"+items[i][1]+"</label>";
            }
            $("#tbDeviceList").html(strItems);
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
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<label class='checkbox-inline'><input type='checkbox' name='kpi' value='"+items[i][0]+" checked'>"+items[i][1]+"</label>";
            }
            $("#tbKpiList").html(strItems);
        }
    });
}