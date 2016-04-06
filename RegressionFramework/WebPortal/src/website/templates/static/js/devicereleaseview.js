'use strict';
var serverHost = window.location.host;
var kpiid = GetQueryString("kpiid");
var strResult = "";
var kpiIndexList = [];
var startKpiIndex = 1;
var endKpiIndex = 1;
var isShowRegression = false;
$(document).ready(function(){
    initPlatformList();
    initDeviceList();
    initReleaseTypeList();
    initTestData();
    $("#regDetail").dialog({
        position: [(document.documentElement.clientWidth-800)/2,180],
        autoOpen:false,
        width:800
    });
});
function initPlatformList(){
    var url = "http://"+serverHost+"/rest/getplatformlist";
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {   
            var items = JSON.parse(data)["result"];
            var strItems = "<option value='-1'>---------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#platform").html(strItems);
        }
    });
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
                strItems += "<label style='margin-right:15px;'><input type='checkbox' value="+items[i][0]+" device='"+items[i][1]+"' onclick='SelectDevice(this)' disabled />"+items[i][1]+"</label>";
            }
            $("#device").html(strItems);
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
            $("#releasetype").html(strItems);
        }
    });
}
function initTestData(){
    var url = "http://"+serverHost+"/rest/getdevicereleaseview?kpiid=" + kpiid;
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items,true);
        }
    });
}

function showView(items,isFirst){
    $("#r_content").html("");
    if(isFirst){ kpiIndexList = []; }
    var strRelease = "";
    var content = "<thead><tr style='background-color:#FFDEAD;'>";
    if(items.length<=0){return;}
    var cols = [];
    for(var key in items[0]){
        if(key != "device_id" && key != "release_id" && key != "pre_id"){
            cols.push(key); 
        }
    }
    cols.sort();
    
    ////////head////////
    for(var col in cols){
        if(col ==0){
            content += "<th style='width:500px;' class='tHead'>Device</th><th style='width:50px;' class='tHead'>T/M/THD</th><th style='width:40px;' class='tHead'>Unit</th>";
        }else if(col%2 !=0){
            content += "<th style='width:800px;' class='tHead'>"+cols[col]+"</th>";
            strRelease += "<option value='"+col+"'>"+cols[col]+"</option>";
            kpiIndexList.push(col);
        }
    }
    $("#release_s").html(strRelease);
    $("#release_e").html(strRelease);
    content += "</tr></thead><tbody>";
    ////////head////////
    ////////body////////
    for(var i=0;i<items.length;i++){
        $("#device label input[device='"+items[i]["Device"].split("*_*")[0]+"']").prop("disabled","");
        $("#device label input[device='"+items[i]["Device"].split("*_*")[0]+"']").prop("checked",true);
        content += "<tr>";
        var temp = "";
		var f_target = parseFloat(items[i]["Device"].split("*_*")[3].replace(/,/g,""));
		var largeisbetter = items[i]["Device"].split("*_*")[2];
		var f_margin = parseFloat(items[i]["Device"].split("*_*")[4].replace(/,/g,""))*100;
		var f_tth1 = parseFloat(items[i]["Device"].split("*_*")[5].replace(/,/g,""))*100;
		var f_tth2 = parseFloat(items[i]["Device"].split("*_*")[6].replace(/,/g,""))*100;
        for(var col in cols){
            if(col == 0){
                var symbol = largeisbetter == "0" ? "-":"+";
                var devicestyle = " background-color: #8ca9cf;background-image: -webkit-gradient( linear, left top, left bottom, color-stop(0%,rgba(255,255,255,0.4)), color-stop(50%,rgba(255,255,255,0.2)), color-stop(51%,rgba(255,255,255,0.1)), color-stop(100%,rgba(255,255,255,0.0))); font-size:10pt;text-shadow: 0 1px 1px #e8ebee;color: #121517;font-weight: bold;"
                content += "<td style='vertical-align:middle;"+devicestyle+"'>"+items[i][cols[col]].split("*_*")[0]+"</td><td><div class='tmDiv' style='background-color:inherit;'><font class='mTitle'>T/M&nbsp;:&nbsp;</font>"+f_target+"/"+f_margin+"%<br/><font class='mTitle'>THD:&nbsp;</font><span class='ttWarning'>"+f_tth1+"%</span><span class='ttDanger'>"+f_tth2+"%</span></div></td><td style='vertical-align:middle'>"+items[i][cols[col]].split("*_*")[1] +"("+symbol+")</td>";            
            }else if(col%2 !=0){
                var pre = parseFloat(items[i][cols[col-(-1)]].replace(/,/g,""));
                var cur = parseFloat(items[i][cols[col]].replace(/,/g,""));
                var offsetText = GetThreshold(cur,pre,largeisbetter);
                var cls_tt = GetThresholdClass(cur,pre,f_tth1,f_tth2,largeisbetter);
				var cls_m = GetMarginClass(cur,f_target,f_margin,largeisbetter);
                var text = items[i][cols[col]].split("*_*")[0] == "0" ? "":items[i][cols[col]].split("*_*")[0];
				var releaseid = items[i][cols[col]].split("*_*")[1];
				var preid = items[i][cols[col]].split("*_*")[2];
                content += "<td class='"+cls_m+"' deviceid='"+items[i]["device_id"]+"' releaseid='"+releaseid+"' preid='"+preid+"' style='font-size:14pt; width:100px; text-align:center; vertical-align:middle;'>"
                        + "<span class='"+cls_tt+" floatMarginSpan'>"+offsetText+"</span>"
                        + "<a style='cursor:pointer;' onclick='ShowDetail(this)'>" + text + "</a></td>";
            }
        }
        content += "</tr>";
    }
    content += "</tbody>";
    ////////body////////
    $("#div_content").html('<table id="r_content" class="table table-bordered table-striped vMiddle fancyTable"></table>');
    $("#r_content").html(content);
    strResult = content;
    _w_table_rowspan("#r_content",1,1);
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true });
    
    if(isFirst){
        startKpiIndex = 1;
        endKpiIndex = kpiIndexList[kpiIndexList.length-1];
    }else{
        FilterData();
    }
    $("#release_s").val(startKpiIndex);
    $("#release_e").val(endKpiIndex);
}
function ShowDetail(obj){
    var deviceid= $(obj).parent().attr("deviceid");
    var releaseid= $(obj).parent().attr("releaseid");
    var pre_releaseid= $(obj).parent().attr("preid");
    $("#regDetail").dialog("open");
    var cur_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=9&releaseid=" + releaseid;
    var pre_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=9&releaseid=" + pre_releaseid;
    $.ajax({
        type: 'GET',
        url: cur_url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strValues = "";
            var values = [];
            if(items.length<=0){return;}
            $("#d_kpiinfo").html(items[0][3] + "&nbsp;&nbsp;&nbsp;&nbsp;" + items[0][4]);
            for(var item in items){ 
                strValues += "<tr><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2].replace(/#/g,"%23") +"' target='_blank'>Goto>></a></td></tr>"; 
                values.push(parseFloat(items[item][0].replace(/,/g,"")));
            }            
            $("#curRelease").html(items[0][1]);
			$("#curValueInfo").html(strValues);
			$("#curTimes").html(items.length);
            $("#curMid").html(getMidValue(values).toString());
            $("#curAvg").html(getAvgValue(values).toString());
            $("#curStd").html(getStdDevValue(values).toString());
        }
    });
    $.ajax({
        type: 'GET',
        url: pre_url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var strValues = "";
            var values = [];
            if(items.length<=0){return;}
            for(var item in items){
                strValues += "<tr><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2].replace(/#/g,"%23") +"' target='_blank'>Goto>></a></td></tr>"; 
                values.push(parseFloat(items[item][0].replace(/,/g,"")));
            }
			$("#preValueInfo").html(strValues);
			$("#preTimes").html(items.length);
			
            $("#preRelease").html(items[0][1]);
            $("#preValues").html(strValues);
            $("#preMid").html(getMidValue(values).toString());
            $("#preAvg").html(getAvgValue(values).toString());
            $("#preStd").html(getStdDevValue(values).toString());
        }
    });
}
function CloseDetailWindow(){
    $("#regDetail").dialog("close");
}

function ChangePlatform(obj){
    var url = "http://"+serverHost+"/rest/getdevicereleaseview?platform=" + $(obj).val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items,false);
        }
    });
}
function SelectDevice(obj){
    if(!$(obj).prop("checked")){
        $("#r_content tr").each(function(){
            if($(this).find("td:eq(0)").html() == $(obj).attr("device")){
                $(this).hide();
            }            
        });
    }else{
        $("#r_content tr").each(function(){
            if($(this).find("td:eq(0)").html() == $(obj).attr("device")){
                $(this).show();
            }            
        });
    }
}
function ChangeReleaseType(obj){
    var url = "http://"+serverHost+"/rest/getdevicereleaseview?releasetype=" + $(obj).val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items,true);
        }
    });
}
function ChangeStartRelease(obj){
    startKpiIndex = parseInt($(obj).val());
    FilterData();    
}
function ChangeEndRelease(obj){
    endKpiIndex = parseInt($(obj).val());
    FilterData();
}
function ShowRegression(obj){
    if($(obj).prop("checked")){
        isShowRegression = true;
    }else{
        isShowRegression = false;
    }
    FilterData();
}
function FilterData(){
    $("#div_content").html('<table id="r_content" class="table table-bordered table-striped vMiddle fancyTable"></table>');
    $("#r_content").html(strResult);
    
    //filter by release
    var colIndex = 0;
    for(var i in kpiIndexList){
        var curIndex = parseInt(kpiIndexList[i]);
        colIndex = (curIndex-1)/2 + 4;
        if(curIndex < startKpiIndex || curIndex > endKpiIndex){
            console.log(colIndex);
            $("#r_content tr td:nth-child("+colIndex+")").each(function(){ $(this).attr("isdel",1); });
            $("#r_content tr th:nth-child("+colIndex+")").each(function(){ $(this).attr("isdel",1); });
        }
    }
    $("#r_content tr td[isdel=1]").each(function(){ $(this).remove(); });
    $("#r_content tr th[isdel=1]").each(function(){ $(this).remove(); });
    
    //filter by regression
    if(isShowRegression == true){
        $("#r_content tr:gt(0)").each(function(i){
            var isShow = false;
            $(this).find("td span:gt(2)").each(function(){
                console.log($(this).html());
                if(parseFloat($(this).html().replace(/%/g,"")) > 5){
                    isShow = true;
                    return false;
                }
            });
            if(!isShow){ $(this).remove(); }
        });
    }
    
    _w_table_rowspan("#r_content",1,1);
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true, });
}

/////////////  tool function  ////////////////////////
function GetMarginClass(score,target,margin,largeisbetter){
    if(score==0 || target==0 || margin==0) { return ""; }
    var offset = largeisbetter == "0" ? (score-target)/score:(target-score)/target;
    if(offset*100>margin){ return "mDanger"; }else{ return "mNormal"; }
}
function GetThresholdClass(cur_score,pre_score,tth1,tth2,largeisbetter){
    if(cur_score==0 || pre_score==0 || tth1==0 || tth2==0) { return ""; }
    var offset = largeisbetter == "0" ? (cur_score-pre_score)/cur_score:(pre_score-cur_score)/pre_score;
    if((offset*100)>tth2){
        return "ttDanger"; 
    }else if(offset*100>tth1){
        return "ttWarning"; 
    }else if(offset*100<-tth1){
        return "ttGood"; 
    }else{
        return "";
    }
}
function GetThreshold(cur_score,pre_score,largeisbetter){
    if(cur_score==0 || pre_score==0){ return ""; }
    var offset = largeisbetter == "0" ? (cur_score-pre_score)/cur_score:(cur_score-pre_score)/pre_score;
    return (offset*100).toFixed(2).toString() + "%";
}

function floatToPercent(fStr){
    var f = parseFloat(fStr);
    if(isNaN(f) || f == 0){ return ""; }
    return (f * 100).toString() + "%"
}
function getAvgValue(values){
    if(values.length==0){ return 0; }
    var sum = 0;
    for(var value in values){
        if(isNaN(values[value])){ continue; }
        sum += values[value];
    }
    return (sum/values.length).toFixed(2)
}
function getStdDevValue(values){
    if(values.length==0){ return 0; }
    
    var avg = getAvgValue(values);
    var temp = 0;
    for(var value in values){
        if(isNaN(values[value])){ continue; }
        temp += Math.pow(values[value]-avg,2);
    }
    return Math.sqrt(temp/(values.length)).toFixed(2)
}
function getMidValue(values){
    var result = 0;
    var temp = [];
    values.sort(function compare(a,b){return a-b>0;});
    if(values.length%2 == 0){
        temp.push(values[Math.floor(values.length/2)]);
        temp.push(values[Math.floor(values.length/2) - 1]);
        result = getAvgValue(temp);
    }
    else{
        result = values[Math.floor(values.length/2)];
    }
    return result;
}

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}
function _w_table_rowspan(_w_table_id,_w_table_colnum,count){
    var _w_table_firsttd = "";
    var _w_table_currenttd = "";
    var _w_table_SpanNum = 0;
    var _w_table_Obj = $(_w_table_id + " tr td:nth-child(" + _w_table_colnum + ")");
    _w_table_Obj.each(function(i){
        if(i==0){
            _w_table_firsttd = $(this);
            _w_table_SpanNum = 1;
        }else{
            _w_table_currenttd = $(this);
            if(_w_table_firsttd.text() ==_w_table_currenttd.text()){
                _w_table_SpanNum++;
                _w_table_currenttd.nextAll(":lt("+(count-1)+")").andSelf().remove();
                _w_table_firsttd.nextAll(":lt("+(count-1)+")").andSelf().attr("rowSpan",_w_table_SpanNum);
            }else{
                _w_table_firsttd = $(this);
                _w_table_SpanNum = 1;
            }
        }
    });
    $(_w_table_id).fixedHeaderTable('show');
}