'use strict';
var serverHost = window.location.host;
var releasetypeid="-1";
$(document).ready(function(){
    initReleaseTypeList();
    $("#newreleasetype").dialog({
        width:450,
        maxHeight:800,
        autoOpen:false,
        close:function(event,ui){
            $("#r_name").val("");
            $("#r_gituri").val("");
            $("#r_branchpath").val("");
        }
    });
});

function initReleaseTypeList(){
    var url = "http://"+serverHost+"/rest/getreleasetypelist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strItems = "";
            for(var i=0;i<items.length;i++){
                var ismonitor = items[i][4] == "1" ? "True":"False";
                strItems += "<tr rtid='"+items[i][0]+"'><td>"+items[i][1]+"</td><td>"+items[i][2]+"</td><td>"+items[i][3]+"</td><td>"+ismonitor+"</td><td style='width:150px'><button class='btn btn-xs' onclick='EditReleaseType(this)'>Edit</button><button class='btn btn-xs' style='margin-left:10px;' onclick='DeleteReleaseType(this)'>Delete</button></td></tr>";
            }
            $("#releasetypelist").html(strItems);
        }
    });
}

function SaveReleaseType(){
    var name = $("#r_name").val();
    var gituri = $("#r_gituri").val();
    var branchpath = $("#r_branchpath").val();
    var ismonitor = $("#r_ismonitor").prop("checked") ? "1":"0";
    if(name==""){ alert("please input the requried field."); return;}
    
	var url = "";
    var record = { };
    if(releasetypeid == "-1"){
		url = "http://"+serverHost+"/rest/newreleasetype";
		record = { "name":name,"gituri":gituri,"branchpath":branchpath,"ismonitor":ismonitor };
	}else{
		url = "http://"+serverHost+"/rest/editreleasetype";
		record = { "rtid":releasetypeid,"name":name,"gituri":gituri,"branchpath":branchpath,"ismonitor":ismonitor };
	}
    $.ajax({
        type: 'POST',
		data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            initReleaseTypeList();
            CloseReleaseTypeWindow();
        }
    });
}

function AddNewReleaseType(){
    releasetypeid="-1";
    $("#newreleasetype").dialog("open");
}
function EditReleaseType(obj){
    releasetypeid = $(obj).parent().parent().attr("rtid");
    $("#r_name").val($(obj).parent().parent().find("td:eq(0)").html());
    $("#r_gituri").val($(obj).parent().parent().find("td:eq(1)").html());
    $("#r_branchpath").val($(obj).parent().parent().find("td:eq(2)").html());
    $(obj).parent().parent().find("td:eq(3)").html() == "True" ? $("#r_ismonitor").prop("checked",true):$("#r_ismonitor").prop("checked",false);
    $("#newreleasetype").dialog("open");
}
function DeleteReleaseType(obj){
	if(confirm('Are you sure to delete it?')){
        var rtid = $(obj).parent().parent().attr("rtid");
        $.ajax({
            type: 'GET',
            url: "http://"+serverHost+"/rest/deletereleasetype?rtid="+rtid,
            success: function(data) {
                initReleaseTypeList();
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Can't delete, because somewhere refrence it!");
            }
        });
    }
}

function CloseReleaseTypeWindow(){
    $("#newreleasetype").dialog("close");
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
