'use strict';
var serverHost = window.location.host;
var pnproleid = -1;
$(document).ready(function(){
    initPnpRoleList();
    initKpiList();
    $("#newpnprole").dialog({
        position: [(document.documentElement.clientWidth-1200)/2,100],
        width:1200,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#p_name").val("");
            $("#p_kpis input").prop("checked",false);
        }
    });
});

function initPnpRoleList(){
    var url = "http://"+serverHost+"/rest/getpnprolelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<tr pid='"+items[i][0]+"'><td>"+items[i][1]+"</td><td style='width:200px;'><button class='btn btn-xs' onclick='ShowKPI(this)'>Show KPI</button><button class='btn btn-xs' style='margin-left:10px;' onclick='EditPnpRole(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeletePnpRole(this)'>Delete</button></td></tr>";
            }
            $("#pnprolelist").html(strItems);
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
			var casename = "";
            for(var i=0;i<items.length;i++){
                if(kpitype != items[i][1].split("#")[0]){
                    
					if(items[i][1].split("#").length > 1){
						kpitype = items[i][1].split("#")[0];
					}else{
						kpitype = "Other";
					}
                    strItems += "<p style='background-color:#ABABAB;color:white;font-size:12pt;font-wight:bolder;'>"+kpitype+"</p>";
                }
				if(items[i][1].split("#").length > 1){
					casename = items[i][1].split("#")[2];
				}else{
					casename = items[i][1].split("#")[0];
				}
				strItems += "<label style='margin-left:15px;'><input type='checkbox' value='"+items[i][0]+"' />"+casename+"</label>";
            }
            $("#p_kpis").html(strItems);
        }
    });
}

function SavePnpRole(){
    var name = $("#p_name").val();
    if(pnproleid == -1){
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/newpnprole?name="+name,
            success: function(data) {
                var newpnproleid = JSON.parse(data)["message"];
                $("#p_kpis input:checked").each(function(){
                    $.ajax({
                        type: 'GET',
                        url: "http://"+serverHost+"/rest/newpnprolekpi?pnprole="+newpnproleid+"&kpi="+$(this).val(),
                        success: function(data) {
                            console.log(data);
                        }
                    });
                });
                ClosePnpRoleWindow();
                initPnpRoleList();
            }
        });
    }else{
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/editpnprole?pid="+pnproleid+"&name="+name,
            success: function(data) {
                console.log(data);
            }
        });
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletepnprolekpibypnproleId?pid="+pnproleid,
            success: function(data) {
                $("#p_kpis input:checked").each(function(){
                    $.ajax({
                        type: 'GET',
                        url: "http://"+serverHost+"/rest/newpnprolekpi?pnprole="+pnproleid+"&kpi="+$(this).val(),
                        success: function(data) {
                            console.log(data);
                        }
                    });
                });
                ClosePnpRoleWindow();
                initPnpRoleList();
            }
        });
    }
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
                var strKpis = "<tr><td colspan=2>";
                for(var i=0;i<items.length;i++){
                    var casename = items[i][1];
                    if(items[i][1].indexOf("#") > 0){
                        casename = items[i][1].split("#")[2];
                    }
                    strKpis += "<label style='margin-left:15px;'><input type='checkbox' value='"+items[i][0]+"' checked/>"+casename+"</label>"
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

function AddNewPnpRole(){
    pnproleid = -1;
    $("#newpnprole").dialog("open");
}
function EditPnpRole(obj){
    pnproleid = $(obj).parent().parent().attr("pid");
    $.ajax({
        type: 'GET',
        url: "http://"+serverHost+"/rest/getpnprolebyid?pid="+pnproleid,
        success: function(data) {
            var result = JSON.parse(data);
            $("#p_name").val(result["name"][0][0]);
            $("#p_kpis input").prop("checked",false);
            for(var i=0;i<result["kpis"].length;i++){
                $("#p_kpis input[value='"+result["kpis"][i][0]+"']").prop("checked",true);
            }
        }
    });
    $("#newpnprole").dialog("open");
}
function DeletePnpRole(obj){
    if(confirm('Are you sure to delete it?')){
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletepnprolekpi?pid="+$(obj).parent().parent().attr("pid"),
            success: function(data) {
                $(obj).parent().parent().remove();
            }
        });
    }
}
function ClosePnpRoleWindow(){
    $("#newpnprole").dialog("close");
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
