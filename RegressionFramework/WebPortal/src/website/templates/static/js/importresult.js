'use strict';
var serverHost = window.location.host;
var logserver = "http://pnp.sh.intel.com/automation-logs/";
var kpilist = {};
var releaseList = [];
$(document).ready(function(){
    initDeviceList();
    initReleaseList();
    initReleaseTypeList();
    $("#releasedate_n").datepicker({dateFormat:'yy-mm-dd'})
    $("#newrelease").dialog({
        width:700,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            
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
            $("#sltDevice").html(strItems);
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
			releaseList = items;
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][2]+"</option>";
            }
            //$("#sltRelease").html(strItems);
        }
    });
}
function initReleaseTypeList(){
    var url = "http://"+serverHost+"/rest/getreleasetypelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {   
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>---------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#sltReleaseType_n").html(strItems);
            $("#sltReleaseType").html(strItems);
        }
    });
}
function FilterRelease(obj){
	var strItems = "<option value='-1'>---------</option>";
	console.log($(obj).val());
	if($(obj).val()){
		for(var item in releaseList){
			if($(obj).val()==releaseList[item][4]){
				strItems += "<option value="+releaseList[item][0]+">"+releaseList[item][2]+"</option>";
			}
		}
	}
	$("#sltRelease_n").html(strItems);
}
function FilterMainRelease(obj){
	var strItems = "<option value='-1'>---------</option>";
	console.log($(obj).val());
	if($(obj).val()){
		for(var item in releaseList){
			if($(obj).val()==releaseList[item][4]){
				strItems += "<option value="+releaseList[item][0]+">"+releaseList[item][2]+"</option>";
			}
		}
	}
    $("#sltRelease").html(strItems);
}
function initKpiList(){
    var url = "http://"+serverHost+"/rest/getkpilist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            kpilist = {};
            var items = JSON.parse(data)["result"];
            for(var i=0;i<items.length;i++){
                kpilist[items[i][1].replace(" ","_")] = items[i][0];
            }
        }
    });
}
function GetTestData(){
    if($("#jobid").val().length <= 0){ alert("Please input the job id!"); return; }

    var url = "http://"+serverHost+"/rest/gettestdata?jobid="+$("#jobid").val();
    var strItems = "";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            console.log(items);
            for(var i=0;i<items.length;i++){
                strItems += "<tr><td><input type='checkbox' /></td><td>"+items[i][2]+"</td><td>"+items[i][0]+"</td><td>"+items[i][1]+"</td><td>"+logserver + $("#jobid").val() + "/127.0.0.1_" + items[i][2] + "/" + items[i][0] +"</td></tr>";
            }
            $("#tbTestData").html(strItems);
            alert("load complete!")
        }
    });

    initKpiList();
}

function AddNewRelease(){
    $("#newrelease").dialog("open");
}
function CloseReleaseWindow(){
    $("#newrelease").dialog("close");
}

function SaveToDB(){
    var failedKPI = "";
    $("#tbTestData tr").each(function(){
        if($(this).find("td input").prop("checked")){
            var kpiid = kpilist[$(this).find("td:eq(2)").html()];
            if(kpiid){
                var deviceid = $("#sltDevice").val();
                var releaseid = $("#sltRelease").val();
				var jobid = $(this).find("td:eq(1)").html();
                var remark = $(this).find("td:eq(4)").html();
                var scores = JSON.parse($(this).find("td:eq(3)").html());
                for(var score in scores){
                    var url = "http://"+serverHost+"/rest/savetestdata?deviceid="+deviceid+"&releaseid="+releaseid+"&kpiid="+kpiid+"&remark="+escape(remark)+"&score=" + scores[score]+"&jobid=" + jobid+"&datafrom=3";
                    $.ajax({
                        type: 'GET',
                        url: url,
                        success: function(data) {
                            console.log(data);
                        }
                    });
                }
            }else{
                failedKPI += $(this).find("td:eq(2)").html() + ";  ";
            }
        }
    });
    if(failedKPI.length > 0){ alert("some kpi did not exist: " + failedKPI); return; }
    alert("Save Complete!");
}

function SaveRelease(){
    $("#pullrequest_n tr").each(function(index){
        if($(this).find("input:eq(0)").val().length <= 0){
            $(this).remove();
        }
    });
    var preid=$("#sltRelease_n").val() == -1 ? "NULL":$("#sltRelease_n").val();
    var r_record = { "name":$("#name_n").val(),"releasedate":$("#releasedate_n").val(),"pre":preid,"releasetype":$("#sltReleaseType_n").val(),"remark":$("#remark_n").val() };
    $.ajax({
        type: 'POST',
        url: "http://" + serverHost + "/rest/addnewrelease",
        data: { "record": JSON.stringify(r_record) },
        dataType: "json",
        success: function(releasedata) {
            var releaseid = releasedata["result"];
            var releaseid=15;
            var pullrequests = $("#pullrequest_n").val().split("\n");
            var needAddPr = false;
            $("#pullrequest_n tr").each(function(index){
                var name = $(this).find("input:eq(0)").val();
                var pullurl = "http://pnp/" + name;
                var preingname = $(this).find("input:eq(1)").val();
                var preingurl = "http://preintegration/" + preingname;
                var remark = $(this).find("input:eq(2)").val();
                if(name.length > 0){
                    var pr_record = { "name":name,"pullurl":pullurl,"preingration":preingname,"ingrationurl":preingurl,"remark":remark };
                    needAddPr = true;
                    $.ajax({
                        type: 'POST',
                        url: "http://" + serverHost + "/rest/addnewpullrequest",
                        data: { "record": JSON.stringify(pr_record) },
                        dataType: "json",
                        success: function(pullrequestdata) {
                            var pullrequestid = pullrequestdata["result"];
                            var rpr_record = { "pullrequestid":pullrequestid,"releaseid":releaseid };
                            $.ajax({
                                type: 'POST',
                                url: "http://" + serverHost + "/rest/addreleasepullrequest",
                                data: { "record": JSON.stringify(rpr_record) },
                                dataType: "json",
                                success: function(data) {
                                    console.log(data);
                                    initReleaseList();
                                    if(index == ($("#pullrequest_n tr").length-1)){
                                        alert("Save Complete!");
                                        $("#newrelease table input").val("");
                                        $("#newrelease").dialog("close");
                                    }
                                }
                            });
                        }
                    });
                }
                if(!needAddPr && index == ($("#pullrequest_n tr").length-1)){
                    alert("Save Complete!");
                    $("#newrelease table input").val("");
                    $("#newrelease").dialog("close");
                }
            });
            
        }
    });
}

function checkall(obj){
    if($(obj).prop("checked")){
        $("#tbTestData tr td input").prop("checked",true);
    }else{
        $("#tbTestData tr td input").prop("checked",false);
    }
}
function AddNewRow(obj){
    $("#pullrequest_n").append('<tr><td ><input style="width:150px;" /></td><td><input style="width:150px;"/></td><td colspan=2><input style="width:150px;"/></td></tr>');
}
function removeBlank(str){
    str=str.replace(/(\s+$)|(^\s+)/g,"");
    str=str.replace(/\s+/g," ");
    return str;
}
