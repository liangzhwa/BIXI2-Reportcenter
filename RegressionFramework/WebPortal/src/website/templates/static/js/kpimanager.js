'use strict';
var serverHost = window.location.host;
var kpiid = "-1";
var largeisbetterList = ["fps","score"]
$(document).ready(function(){
    initKpiList();
    initKpiTypeList();
    initUnitList();
    initPriorityList();
    $("#newkpi").dialog({
        width:600,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#k_showname").val("");
            $("#k_testcasename").val("");
            $("#k_key").val("");
            $("#k_summary").val("");
            $("#k_remark").val("");
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

function initUnitList(){
    var url = "http://"+serverHost+"/rest/getunitlist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#k_sltUnit").html(strItems);
        }
    });
}
function initPriorityList(){
    var url = "http://"+serverHost+"/rest/getprioritylist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#k_sltPriority").html(strItems);
        }
    });
}
function initKpiTypeList(){
    var url = "http://"+serverHost+"/rest/getkpitypelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#k_sltKpitype").html(strItems);
        }
    });
}
function initKpiList(){
    var url = "http://"+serverHost+"/rest/getkpitable";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                var key = items[i][5].substr(items[i][5].lastIndexOf("/")+1);
                var summary = items[i][6] == "" ? "":"summary"
                strItems += "<tr kId='"+items[i][0]+"' testcasename='"+items[i][8]+"'><td typeid='"+items[i][11]+"'>"+items[i][3]+"</td><td>"+items[i][1]+"</td><td uid='"+items[i][9]+"' largeisbetter='"+items[i][10]+"'>"+items[i][2]+"</td><td priorityid='"+items[i][12]+"'>"+items[i][4]+"</td><td><a href='"+items[i][5]+"' target='_blank'>"+key+"</a></td><td><a href='"+items[i][6]+"' target='_blank'>"+summary+"</a></td><td>"+items[i][7]+"</td><td style='width:150px'><button class='btn btn-xs' onclick='EditKpi(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteKpi(this)'>Delete</button></td></tr>";
            }
            $("#kpilist").html(strItems);
        }
    });
}

function SaveKpi(){
    var showname = $("#k_showname").val();
    var testcasename = $("#k_testcasename").val();
    var unit = $("#k_sltUnit").val();
    var largeisbetter = $("#k_largeisbetter").prop("checked") ? "1":"0";
    var kpitype = $("#k_sltKpitype").val();
    var kpipriority = $("#k_sltPriority").val();
    var key = $("#k_key").val();
    var summary = $("#k_summary").val();
    var remark = $("#k_remark").val();
    if(showname=="" || testcasename==""){ alert("please input the requried field."); return; }
    var url = "";
    var record = { };
    var msg = "";
    if(kpiid == "-1"){
        record = { "showname":showname,"testcasename":testcasename,"unit":unit,"largeisbetter":largeisbetter,"kpitype":kpitype,"kpipriority":kpipriority,"key":key,"summary":summary,"remark":remark };
        url = "http://"+serverHost+"/rest/newkpi";
        msg = "Add KPI Success!";
    }else{
        record = { "kid":kpiid,"showname":showname,"testcasename":testcasename,"unit":unit,"largeisbetter":largeisbetter,"kpitype":kpitype,"kpipriority":kpipriority,"key":key,"summary":summary,"remark":remark };
        url = "http://"+serverHost+"/rest/editkpi";
        msg = "Edit KPI Success!";
    }
    $.ajax({
        type: 'POST',
        data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            initKpiList();
            CloseKpiWindow();
            alert(msg);
        }
    });
}

function AddNewKpi(){
    kpiid = "-1";
    $("#newkpi").dialog("open");
}
function CloseKpiWindow(){
    $("#newkpi").dialog("close");
}

function EditKpi(obj){
    kpiid = $(obj).parent().parent().attr("kid");

    $("#k_showname").val($(obj).parent().parent().find("td:eq(1)").html());
    $("#k_testcasename").val($(obj).parent().parent().attr("testcasename"));
    $("#k_sltUnit").val($(obj).parent().parent().find("td:eq(2)").attr("uid"));
    $(obj).parent().parent().find("td:eq(2)").attr("largeisbetter") == "1" ? $("#k_largeisbetter").prop("checked",true) : $("#k_largeisbetter").prop("checked",false);
    $("#k_sltKpitype").val($(obj).parent().parent().find("td:eq(0)").attr("typeid"));
    $("#k_sltPriority").val($(obj).parent().parent().find("td:eq(3)").attr("priorityid"));
    $("#k_key").val($(obj).parent().parent().find("td:eq(4) a").attr("href"));
    $("#k_summary").val($(obj).parent().parent().find("td:eq(5) a").attr("href"));
    $("#k_remark").val($(obj).parent().parent().find("td:eq(6)").html());
    $("#newkpi").dialog("open");
}
function DeleteKpi(obj){
    if(confirm('Are you sure to delete it?')){
        var kid = $(obj).parent().parent().attr("kid");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletekpi?kid="+kid,
            success: function(data) {
                initKpiList();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function GetShowName(obj){
    $("#k_showname").val($(obj).val().split("#")[2]);
}
function SetLargeisbetter(obj){
    if(largeisbetterList.indexOf($(obj).find("option:selected").text()) > -1){
        $(obj).next().find("input").prop("checked",true);
    }else{
        $(obj).next().find("input").prop("checked",false);
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
