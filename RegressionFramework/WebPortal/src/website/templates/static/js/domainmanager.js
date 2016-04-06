'use strict';
var serverHost = window.location.host;
var domainid = -1;
$(document).ready(function(){
    initDomainList();
    initKpiList();
    $("#newdomain").dialog({
        position: [(document.documentElement.clientWidth-1200)/2,100],
        width:1200,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#d_name").val("");
            $("#d_kpis input").prop("checked",false);
        }
    });
});

function initDomainList(){
    var url = "http://"+serverHost+"/rest/getdomainlist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<tr did='"+items[i][0]+"'><td>"+items[i][1]+"</td><td style='width:200px;'><button class='btn btn-xs' onclick='ShowKPI(this)'>Show KPI</button><button class='btn btn-xs' style='margin-left:10px;' onclick='EditDomain(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteDomain(this)'>Delete</button></td></tr>";
            }
            $("#domainlist").html(strItems);
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
            var kpitype = "";
            var strItems = "";
            for(var i=0;i<items.length;i++){
                if(kpitype != items[i][1].split("#")[0]){
                    kpitype = items[i][1].split("#")[0];
                    strItems += "<p style='background-color:#ABABAB;color:white;font-size:12pt;font-wight:bolder;'>"+kpitype+"</p>";
                }
                strItems += "<label style='margin-left:15px;'><input type='checkbox' value='"+items[i][0]+"' />"+items[i][1].split("#")[2]+"</label>";
            }
            $("#d_kpis").html(strItems);
        }
    });
}

function SaveDomain(){
    var name = $("#d_name").val();
    if(domainid == -1){
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/newdomain?name="+name,
            success: function(data) {
                var newdomainid = JSON.parse(data)["message"];
                $("#d_kpis input:checked").each(function(){
                    $.ajax({
                        type: 'GET',
                        url: "http://"+serverHost+"/rest/newdomainkpi?domain="+newdomainid+"&kpi="+$(this).val(),
                        success: function(data) {
                            console.log(data);
                        }
                    });
                });
                CloseDomainWindow();
                initDomainList();
            }
        });
    }else{
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/editdomain?did="+domainid+"&name="+name,
            success: function(data) {
                console.log(data);
            }
        });
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletedomainkpibydomainId?did="+domainid,
            success: function(data) {
                $("#d_kpis input:checked").each(function(){
                    $.ajax({
                        type: 'GET',
                        url: "http://"+serverHost+"/rest/newdomainkpi?domain="+domainid+"&kpi="+$(this).val(),
                        success: function(data) {
                            console.log(data);
                        }
                    });
                });
                CloseDomainWindow();
                initDomainList();
            }
        });
    }
}

function ShowKPI(obj){
    if($(obj).html() == "Show KPI"){
        var domain = $(obj).parent().parent().attr("did");
        var url = "http://"+serverHost+"/rest/getkpilistbydomain?domain="+domain
        $(obj).html("Hide KPI");
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data) {
                var items = JSON.parse(data)["result"];
                var strKpis = "<tr><td colspan=2>";
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

function AddNewDomain(){
    domainid = -1;
    $("#newdomain").dialog("open");
}
function EditDomain(obj){
    domainid = $(obj).parent().parent().attr("did");
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/getdomainbyid?did="+domainid,
        success: function(data) {
            var result = JSON.parse(data);
            $("#d_name").val(result["name"][0][0]);
            $("#d_kpis input").prop("checked",false);
            for(var i=0;i<result["kpis"].length;i++){
                $("#d_kpis input[value='"+result["kpis"][i][0]+"']").prop("checked",true);
            }
        }
    });
    $("#newdomain").dialog("open");
}
function DeleteDomain(obj){
    if(confirm('Are you sure to delete it?')){
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletedomainkpi?did="+$(obj).parent().parent().attr("did"),
            success: function(data) {
                $(obj).parent().parent().remove();
            }
        });
    }
}
function CloseDomainWindow(){
    $("#newdomain").dialog("close");
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
