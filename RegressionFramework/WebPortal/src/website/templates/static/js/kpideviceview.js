'use strict';
var serverHost = window.location.host;
var releaseid = GetQueryString("releaseid");
var strResult = "";
var kpiIndexList = [];
var cur_releaseid=13;
var pre_releaseid=12;
var currentFeature = "All";
var isShowRegression = false;
$(document).ready(function(){
    initDomainList();
    initPlatformList();
    initDeviceList();
    initTestData();
    $("#regDetail").dialog({
        position: [(document.documentElement.clientWidth-800)/2,200],
        width:800,
        autoOpen:false,
        close:function(event,ui){
            
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
            var strItems = "<option value='-1'>---------</option>";
            for(var i=0;i<items.length;i++){
                strItems += "<option value="+items[i][0]+">"+items[i][1]+"</option>";
            }
            $("#domain").html(strItems);
        }
    });
}
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
                strItems += "<label style='margin-right:15px;'><input type='checkbox' value="+items[i][0]+" device='"+items[i][1]+"' onclick='SelectDevice(this)' />"+items[i][1]+"</label>";
            }
            $("#device").html(strItems);
        }
    });
}
function initTestData(){
    var url = "http://"+serverHost+"/rest/getkpideviceview?releaseid=" + releaseid;
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items);
        }
    });
}

function showView(items){
    $("#r_content").html("");
    kpiIndexList = [];
    var strStartRelease = "";
    var strEndRelease = "";
    var content = "<thead><tr style='background-color:#FFDEAD;'>";
    if(items.length<=0){return;}
    var cols = [];
    for(var key in items[0]){
        if(key.indexOf("*_*") > 0){
            cols.push(key.split("*_*")[0]);
        }
    }

    cols = unique(cols);
    cols.splice(0,0,"KPI"); 
    //cols.sort(function compare(a,b){return b>a;});
    ////////head////////
    $("#device label input").each(function(){
        if(cols.indexOf($(this).attr("device")) > -1){
            $(this).prop("checked",true);
        }else{
            $(this).attr("disabled","disabled");
        }
    });
    for(var col in cols){
        if(col ==0){
            content += "<th style='width:80px;'></th><th style='width:280px;' class='tHead'>KPI</th><th style='width:40px;' class='tHead'>Unit</th>";
        }else{
            content += "<th style='width:800px;' class='tHead' device='"+cols[col]+"'>"+cols[col]+"</th>";
        }
    }
    content += "</tr></thead><body>";
    ////////head////////
    ////////body////////
    for(var i=0;i<items.length;i++){
        content += "<tr>";
        var temp = "";
        var largeisbetter = items[i]["KPI"].split("*_*")[3];
        var symbol = largeisbetter == "0" ? "-":"+";
        for(var col in cols){
            if(col == 0){
                var kpistyle = " background-color: #8ca9cf;background-image: -webkit-gradient( linear, left top, left bottom, color-stop(0%,rgba(255,255,255,0.4)), color-stop(50%,rgba(255,255,255,0.2)), color-stop(51%,rgba(255,255,255,0.1)), color-stop(100%,rgba(255,255,255,0.0))); font-size:10pt;text-shadow: 0 1px 1px #e8ebee;color: #121517;font-weight: bold;"
                content += "<td>"+items[i]["KPI"].split("*_*")[0]+"</td><td testcasename='"+items[i]["testcasename"]+"' style='vertical-align:middle;"+kpistyle+"'>"+items[i]["KPI"].split("*_*")[1]+"</td><td style='vertical-align:middle'>"+items[i]["KPI"].split("*_*")[2] +"("+symbol+")</td>"; 
            }else{
                var cur_score=0,pre_score=0,target=0,margin=0,tth1=0,tth2=0;
                var curScore = items[i][cols[col]+"*_*"+cur_releaseid];
                if(curScore){
                    cur_score = parseFloat(curScore.split("*_*")[0].replace(",",""));
                    target = parseFloat(curScore.split("*_*")[1].replace(",",""));
                    margin = parseFloat(curScore.split("*_*")[2].replace(",",""))*100;
                    tth1 = parseFloat(curScore.split("*_*")[3].replace(",",""))*100;
                    tth2 = parseFloat(curScore.split("*_*")[4].replace(",",""))*100;
                }
                var preScore = items[i][cols[col]+"*_*"+pre_releaseid];
                pre_score = preScore ? parseFloat(preScore.split("*_*")[0].replace(",","")):0;
                
                var cls_tt = GetThresholdClass(cur_score,pre_score,tth1,tth2,largeisbetter);
                var cls_m = GetMarginClass(cur_score,target,margin,largeisbetter);
                var pre_cls_m = GetMarginClass(pre_score,target,margin,largeisbetter);
                var tth = GetThreshold(cur_score,pre_score,largeisbetter);
                content += "<td device='"+cols[col]+"' class='"+cls_m+"' kpiid='"+items[i]["KPI"].split("*_*")[4]+"' deviceid='"+items[i]["device_id"]+"' style='font-size:14pt;text-align:center;'><div class='tmDiv'><font class='mTitle'>T/M&nbsp;:&nbsp;</font>"+target+"/"+margin+"%<br/><font class='mTitle'>THD:&nbsp;</font><span class='ttWarning'>"+tth1+"%</span><span class='ttDanger'>"+tth2+"%</span></div> <a style='cursor:pointer;' onclick='ShowDetail(this)'>"+cur_score+"</a><br/><div class='preSpan "+pre_cls_m+"'>"+pre_score+"</div><span class='floatThreshold "+cls_tt+"'>"+tth+"</span></td>";
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
}
function ShowDetail(obj){
    var deviceid= $(obj).parent().attr("deviceid");
    var kpiid= $(obj).parent().attr("kpiid");
    var releaseid= 13;
    var pre_releaseid= 12;
    $("#regDetail").dialog("open");
    var cur_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=" + kpiid + "&releaseid=" + releaseid;
    var pre_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=" + kpiid + "&releaseid=" + pre_releaseid;
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
                strValues += "<tr><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2] +"' target='_blank'>Goto>></a></td></tr>"; 
                values.push(parseFloat(items[item][0].replace(/,/g,"")));
            }
            $("#curValueInfo").html(strValues);
            $("#curTimes").html(items.length);
            $("#curRelease").html(items[0][1]);
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
                strValues += "<tr><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2] +"' target='_blank'>Goto>></a></td></tr>"; 
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

function FilterFeature(featurename){
    currentFeature = featurename;
    $("#div_content").html('<table id="r_content" class="table table-bordered table-striped vMiddle fancyTable"></table>');
    $("#r_content").html(strResult);
    $("#r_content tr td:nth-child(2)").each(function(i){
        if(featurename != "All" && $(this).attr("testcasename").split("#")[0] != featurename){
            $(this).parent().remove();
        }
    });
    _w_table_rowspan("#r_content",1,1);
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true });
}
function ChangeDomain(obj){
    var url = "http://"+serverHost+"/rest/getkpideviceview?domain=" + $(obj).val() + "&platform=" + $("#platform").val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items);
            FilterFeature(currentFeature);
        }
    });
}
function ChangePlatform(obj){
    var url = "http://"+serverHost+"/rest/getkpideviceview?platform=" + $(obj).val() + "&domain=" + $("#domain").val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items);
            FilterFeature(currentFeature);
        }
    });
}
function SelectDevice(){
    $("#div_content").html('<table id="r_content" class="table table-bordered table-striped vMiddle fancyTable"></table>');
    $("#r_content").html(strResult);

    $("#device label").each(function(){
        if(!$(this).find("input[disabled!='disabled']").prop("checked")){
            var tmpDevice = $(this).find("input").attr("device");
            $("#r_content tr").find("th[device='"+tmpDevice+"']").remove();
            $("#r_content tr").find("td[device='"+tmpDevice+"']").remove();
        }
    }); 
    
    _w_table_rowspan("#r_content",1,1);
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true });
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
function unique(array){
    return array.sort().join(",,").replace(/(,|^)([^,]+)(,,\2)+(,|$)/g,"$1$2$4").replace(/,,+/g,",").replace(/,$/,"").split(",");
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
}
