'use strict';
var serverHost = window.location.host;
var testresultid="-1";
$(document).ready(function(){
    initDeviceList();
    initReleaseList();
    initKpiList();
    $("#newtestresult").dialog({
        width:600,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#t_jobid").val("");
            $("#t_score").val("");
            $("#t_remark").val("");
        }
    });
});

function initDeviceList(){
    var url = "http://"+serverHost+"/rest/getdevicelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#t_sltDevice").html(strItems);
        }
    });
}
function initReleaseList(){
    var url = "http://"+serverHost+"/rest/getreleaselist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][2]+"</option>";
            }
            $("#t_sltRelease").html(strItems);
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
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#t_sltKpi").html(strItems);
        }
    });
}

function SearchTestResultByJobid(){
    var jobid = $("#jobid").val();
    var url = "http://"+serverHost+"/rest/gettestresultbyjobid?jobid=" + jobid;
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                strItems += "<tr tid='"+items[i][0]+"'><td did='"+items[i][2]+"'>"+items[i][7]+"</td><td kid='"+items[i][3]+"'>"+items[i][8]+"</td><td rid='"+items[i][4]+"'>"+items[i][9]+"</td><td>"+items[i][1]+"</td><td>"+items[i][6]+"</td><td style='width:150px'><button class='btn btn-xs' onclick='EditTestResult(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteTestResult(this)'>Delete</button></td></tr>";
            }
            $("#testresultlist").html(strItems);
        }
    });
}

function SaveTestResult(){
    var jobid = $("#jobid").val();
    var deviceid = $("#t_sltDevice").val();
    var kpiid = $("#t_sltKpi").val();
    var releaseid = $("#t_sltRelease").val();
    var score = $("#t_score").val();
    var remark = $("#t_remark").val();
    
    if(jobid=="" || deviceid=="" || kpiid=="" || releaseid=="" || score==""){ alert("please input the requried field."); return;}
    
	var url = "";
    var record = { };
    if(testresultid == "-1"){
		url = "http://"+serverHost+"/rest/newtestresult";
		record = { "deviceid":deviceid,"kpiid":kpiid,"releaseid":releaseid,"score":score,"jobid":jobid,"remark":remark };
	}else{
		url = "http://"+serverHost+"/rest/edittestresult";
		record = { "tid":testresultid,"deviceid":deviceid,"kpiid":kpiid,"releaseid":releaseid,"score":score,"jobid":jobid,"remark":remark };
	}
    $.ajax({
        type: 'POST',
		data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            var result = JSON.parse(data)["message"];
            if(result.length > 10){
                alert(result);
            }else{
                SearchTestResultByJobid();
            }
            CloseTestResultWindow();
        }
    });
}

function AddNewTestResult(){
    testresultid="-1";
    $("#t_jobid").val($("#jobid").val());
    $("#newtestresult").dialog("open");
}
function EditTestResult(obj){
    testresultid = $(obj).parent().parent().attr("tid");
    $("#t_jobid").val($("#jobid").val());
    $("#t_sltDevice").val($(obj).parent().parent().find("td:eq(0)").attr("did"));
    $("#t_sltKpi").val($(obj).parent().parent().find("td:eq(1)").attr("kid"));
    $("#t_sltRelease").val($(obj).parent().parent().find("td:eq(2)").attr("rid"));
    $("#t_score").val($(obj).parent().parent().find("td:eq(3)").html());
    $("#t_remark").val($(obj).parent().parent().find("td:eq(4)").html());
    $("#newtestresult").dialog("open");
}
function DeleteTestResult(obj){
	if(confirm('Are you sure to delete it?')){
        var tid = $(obj).parent().parent().attr("tid");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletetestresult?tid="+tid,
            success: function(data) {
                var result = JSON.parse(data)["message"];
                if(result.length > 10){
                    alert(result);
                }else{
                    SearchTestResultByJobid();
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function CloseTestResultWindow(){
    $("#newtestresult").dialog("close");
}

function removeBlank(str){
    str=str.replace(/(\s+$)|(^\s+)/g,"");
    str=str.replace(/\s+/g," ");
    return str;
}
