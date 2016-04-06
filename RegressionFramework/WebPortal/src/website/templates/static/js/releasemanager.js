'use strict';
var serverHost = window.location.host;
var releaseid="-1";
var releaseList = [];
$(document).ready(function(){
    initReleaseList();
    initReleasetypeList();
    $("#r_releasedate").datepicker({dateFormat:'yy-mm-dd'})
    $("#newrelease").dialog({
        width:600,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#d_name").val("");
            $("#d_remark").val("");
        }
    });
});

function initReleasetypeList(){
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
            $("#r_sltReleaseType").html(strItems);
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
            releaseList = items;
            var strTable = "";
            for(var i=0;i<items.length;i++){
                strTable += "<tr rid='"+items[i][0]+"'><td rtid='"+items[i][4]+"'>"+items[i][5]+"</td><td>"+items[i][2]+"</td><td>"+items[i][6]+"</td><td preid='"+items[i][1]+"'>"+items[i][3]+"</td><td>"+items[i][7]+"</td><td style='width:150px'><button class='btn btn-xs' onclick='EditRelease(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteRelease(this)'>Delete</button></td></tr>"
            }
            $("#releaselist").html(strTable);
        }
    });
}
function FilterRelease(obj){
    var strItems = "<option value='-1'>---------</option>";
	if($(obj).val()){
		for(var item in releaseList){
			if($(obj).val()==releaseList[item][4]){
				strItems += "<option value="+releaseList[item][0]+">"+releaseList[item][2]+"</option>";
			}
		}
	}
	$("#r_sltRelease").html(strItems);
}

function SaveRelease(){
    var name = $("#r_name").val();
    var releasetype = $("#r_sltReleaseType").val();
    var releasedate = $("#r_releasedate").val();
    var pre = $("#r_sltRelease").val();
    var remark = $("#r_remark").val();
    if(name=="" || releasetype==""){ alert("please input the requried field."); return;}
    
	var url = "";
    var record = { };
    if(releaseid == "-1"){
		url = "http://"+serverHost+"/rest/newreleasebyweb";
		record = { "name":name,"releasetype":releasetype,"releasedate":releasedate,"pre":pre,"remark":remark };
	}else{
		url = "http://"+serverHost+"/rest/editrelease";
		record = { "rid":releaseid,"name":name,"releasetype":releasetype,"releasedate":releasedate,"pre":pre,"remark":remark };
	}
    $.ajax({
        type: 'POST',
		data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            initReleaseList();
            CloseReleaseWindow();
        }
    });
}

function AddNewRelease(){
    releaseid = "-1";
    $("#newrelease").dialog("open");
}

function EditRelease(obj){
    releaseid = $(obj).parent().parent().attr("rid");
    $("#r_name").val($(obj).parent().parent().find("td:eq(1)").html());
    $("#r_sltReleaseType").val($(obj).parent().parent().find("td:eq(0)").attr("rtid"));
    FilterRelease($("#r_sltReleaseType"));
    $("#r_releasedate").val($(obj).parent().parent().find("td:eq(2)").html());
    $("#r_sltRelease").val($(obj).parent().parent().find("td:eq(3)").attr("preid"));
    $("#r_remark").val($(obj).parent().parent().find("td:eq(4)").html());
    $("#newrelease").dialog("open");
}
function DeleteRelease(obj){
	if(confirm('Are you sure to delete it?')){
        var rid = $(obj).parent().parent().attr("rid");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deleterelease?rid="+rid,
            success: function(data) {
                initReleaseList();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function CloseReleaseWindow(){
    $("#newrelease").dialog("close");
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
