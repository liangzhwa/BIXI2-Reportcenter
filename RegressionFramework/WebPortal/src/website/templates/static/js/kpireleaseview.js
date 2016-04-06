'use strict';
var serverHost = window.location.host;
var deviceid = "1"; //GetQueryString("deviceid");
var sltdRelease = "";
var sltdKpi = "";
var strResult = "";
var curComment = "";
var kpiIndexList = [];
var startKpiIndex = 1;
var endKpiIndex = 1;
var currentFeature = "All";
var isShowRegression = false;
var isShowImprovement = false;
var isShowFailed = false;
var test = ''
$(document).ready(function(){
    initDeviceList();
    initDomainList();
    initReleaseTypeList();
    initTestData();
    $("#regDetail").dialog({
        position: [(document.documentElement.clientWidth-800)/2,180],
        autoOpen:false,
        width:800
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
            $("#device").html(strItems);
        }
    });
}
function LoadDataForDevice(obj){
    deviceid = $(obj).val();
    initTestData()
}
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
    var url = "http://"+serverHost+"/rest/getkpireleaseview?deviceid=" + deviceid;
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
        if(key != "testcasename" && key != "summary" && key != "key"){
            cols.push(key); 
        }
    }
    cols.sort();
    
    ////////head////////
    for(var col in cols){
        if(col ==0){
            content += "<th style='width:80px;'></th><th style='width:280px;' class='tHead'>KPI</th><th style='width:120px;' class='tHead'>T/M/THD</th><th style='width:80px;' class='tHead'>Unit</th>";
        }else if(col%2 !=0){
            var url = cols[col].startWith("LM") ? "https://jfstor001.jf.intel.com/artifactory/simple/otc-jf/releases/gmin-l/" + cols[col] : "https://jfstor001.jf.intel.com/artifactory/simple/irda-jf/irda-l/releases/" + cols[col];
            content += "<th style='width:300px;' class='tHead'><a href='"+url+"' target='_blank' style='color:black;text-decoration:underline;'>"+cols[col]+"</a></th>";
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
        content += "<tr>";
        var temp = "";
		var f_target = parseFloat(items[i]["KPI"].split("*_*")[5].replace(/,/g,""));
		var largeisbetter = items[i]["KPI"].split("*_*")[3];
		var f_margin = parseFloat(items[i]["KPI"].split("*_*")[6].replace(/,/g,""))*100;
		var f_tth1 = parseFloat(items[i]["KPI"].split("*_*")[7].replace(/,/g,""))*100;
		var f_tth2 = parseFloat(items[i]["KPI"].split("*_*")[8].replace(/,/g,""))*100;
        var symbol = largeisbetter == "0" ? "-":"+";
        var showname = items[i]["summary"] == "" ? items[i]["KPI"].split("*_*")[1] : "<a style='color:black;text-decoration:underline;' href='"+items[i]["summary"]+"' target='_blank'>"+items[i]["KPI"].split("*_*")[1]+"</a>";
        for(var col in cols){
            if(col == 0){
                var kpistyle = " background-color: #8ca9cf;background-image: -webkit-gradient( linear, left top, left bottom, color-stop(0%,rgba(255,255,255,0.4)), color-stop(50%,rgba(255,255,255,0.2)), color-stop(51%,rgba(255,255,255,0.1)), color-stop(100%,rgba(255,255,255,0.0))); font-size:10pt;text-shadow: 0 1px 1px #e8ebee;color: #121517;font-weight: bold;"
                content += "<td>"+items[i]["KPI"].split("*_*")[0]+"</td><td testcasename='"+items[i]["testcasename"]+"' style='vertical-align:middle;"+kpistyle+"'>"+showname+"</td><td><span class='tmDiv' style='background-color:inherit;'><font class='mTitle'>T/M&nbsp;:&nbsp;</font><span class='margin'>"+f_target+"/"+f_margin+"%</span><br/><font class='mTitle'>THD:&nbsp;</font><span class='ttWarning'>"+f_tth1+"%</span><span class='ttDanger'>"+f_tth2+"%</span></span></td><td style='vertical-align:middle'>"+items[i][cols[col]].split("*_*")[2] +"("+symbol+")</td>";            
            }else if(col%2 !=0){
                var pre = parseFloat(items[i][cols[col-(-1)]].replace(/,/g,""));
                var cur = parseFloat(items[i][cols[col]].replace(/,/g,""));
                var offsetText = GetThreshold(cur,pre,largeisbetter); //(cur==0 || pre==0) ? "":offset.toString() + "%";
                var cls_tt = GetThresholdClass(cur,pre,f_tth1,f_tth2,largeisbetter);
				var cls_m = GetMarginClass(cur,f_target,f_margin,largeisbetter);
                var text = items[i][cols[col]].split("*_*")[0] == "0" ? "":items[i][cols[col]].split("*_*")[0];
				var releaseid = items[i][cols[col]].split("*_*")[1];
				var preid = items[i][cols[col]].split("*_*")[2];
                var showcomment = "";
                var rerunflag = "";
                if(items[i][cols[col]].split("*_*")[3]){
                    showcomment = "<img src='/static/css/comment.jpg' class='comment' onmouseover='ShowComment(this,\""+escape(items[i][cols[col]].split("*_*")[3])+"\")' onmouseout='HideComment()'/>";
                }else{
                    showcomment = "";
                }
                if(parseInt(items[i][cols[col]].split("*_*")[4])>2){
                    rerunflag = "<img src='/static/css/rerunflag.png' class='rerunflag'/>";
                }else{
                    rerunflag = "";
                }
                
                content += "<td class='"+cls_m+"' kpiid='"+items[i]["KPI"].split("*_*")[4]+"' deviceid='"+deviceid+"' releaseid='"+releaseid+"' preid='"+preid+"' style='font-size:14pt; width:100px; text-align:center; vertical-align:middle;'>"
                        + "<span class='"+cls_tt+" floatMarginSpan'>"+offsetText+"</span>"
                        + "<a style='cursor:pointer;' onclick='ShowDetail(this)'>" + text + "</a>"+showcomment+rerunflag+"</td>";
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
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true, });

    if(isFirst){
        //startKpiIndex = 1;
        //endKpiIndex = kpiIndexList[kpiIndexList.length-1];
        startKpiIndex = kpiIndexList[(cols.length-21)/2];
        endKpiIndex = kpiIndexList[(cols.length-3)/2];
        FilterData();
    }else{
        FilterData();
    }
    $("#release_s").val(startKpiIndex);
    $("#release_e").val(endKpiIndex);
}
function ShowComment(obj,comment){
    $('#commentPanel').html(unescape(comment).replace(/\n/g,"<br/>"));
    $("#commentPanel").css("left",$(obj).offset().left);
    $("#commentPanel").css("top",$(obj).offset().top+$(obj).height()+10);
    $('#commentPanel').show();
}
function HideComment(){
    $('#commentPanel').hide();
}
function ShowDetail(obj){
    var kpiid = sltdKpi = $(obj).parent().attr("kpiid");
    var releaseid = sltdRelease = $(obj).parent().attr("releaseid");
    var pre_releaseid= $(obj).parent().attr("preid");
    $("#regDetail").dialog("open");
    var cur_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=" + kpiid + "&releaseid=" + releaseid;
    var pre_url = "http://"+serverHost+"/rest/getscoredetail?deviceid=" + deviceid + "&kpiid=" + kpiid + "&releaseid=" + pre_releaseid;
    $.ajax({
        type: 'GET',
        url: cur_url,
        success: function(data) {
            var items = JSON.parse(data)["result"];
            var comment = JSON.parse(data)["comment"];
            var strValues = "";
            var values = [];
            if(items.length<=0){return;}
            $("#d_kpiinfo").html(items[0][3] + "&nbsp;&nbsp;&nbsp;&nbsp;" + items[0][4]);
            for(var item in items){
                if(item<=2){
                    strValues += "<tr style='font-weight:bolder;'><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2].replace(/#/g,"%23") +"' target='_blank'>Goto>></a></td></tr>"; 
                    values.push(parseFloat(items[item][0].replace(/,/g,"")));
                    if(item == 2){
                        strValues += "<tr><td colspan=3>Comment:<textarea style='width:100%;height:46px;' id='comment'></textarea></td><td><button style='margin-top:25px;' onclick='SaveComment()'>Save</button></td></tr>";
                    }
                }else{
                    if(item == 3){
                        strValues += "<tr style='background-color:#ddd'><td colspan=4>Rerun Result:</td></tr>"
                    }
                    strValues += "<tr><td></td><td>"+items[item][0] +"</td><td>"+items[item][5]+"</td><td><a href='"+items[item][2].replace(/#/g,"%23") +"' target='_blank'>Goto>></a></td></tr>"; 
                }
            }
            $("#curRelease").html(items[0][1]);
			$("#curValueInfo").html(strValues);
			$("#curTimes").html(items.length);
            $("#curMid").html(getMidValue(values).toString());
            $("#curAvg").html(getAvgValue(values).toString());
            $("#curStd").html(getStdDevValue(values).toString());
            $("#comment").val(comment);
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

function ChangeDomain(obj){
    var url = "http://"+serverHost+"/rest/getkpireleaseview?domain=" + $(obj).val()+"&releasetype=" + $("#releasetype").val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            var items = JSON.parse(data)["viewdata"];
            showView(items,false);
            $("#con_feature button:eq(0)").click();
        }
    });
}
function ChangeReleaseType(obj){
    var url = "http://"+serverHost+"/rest/getkpireleaseview?releasetype=" + $(obj).val();
    $.ajax({
        type: 'GET',
        url: url,
        success: function(data) {
            console.log(data);
            var items = JSON.parse(data)["viewdata"];
            showView(items,true);
        }
    });
}
function FilterFeature(featurename){
    currentFeature = featurename;
    FilterData();
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
        isShowImprovement = false;
        isShowFailed = false;
        $("#cbImprovement").prop("checked",false);
        $("#cbFailed").prop("checked",false);
    }else{
        isShowRegression = false;
    }
    FilterData();
}
function ShowImprovement(obj){
    if($(obj).prop("checked")){
        isShowImprovement = true;
        isShowRegression = false;
        isShowFailed = false;
        $("#cbRegression").prop("checked",false);
        $("#cbFailed").prop("checked",false);
    }else{
        isShowImprovement = false;
    }
    FilterData();
}
function ShowFailed(obj){
    if($(obj).prop("checked")){
        isShowFailed = true;
        isShowImprovement = false;
        isShowRegression = false;
        $("#cbImprovement").prop("checked",false);
        $("#cbRegression").prop("checked",false);
    }else{
        isShowFailed = false;
    }
    FilterData();
}
function FilterData(){
    $("#div_content").html('<table id="r_content" class="table table-bordered table-striped vMiddle fancyTable"></table>');
    $("#r_content").html(strResult);
    
    //filter by featurename
    $("#r_content tr td:nth-child(2)").each(function(i){
        if(currentFeature != "All" && $(this).attr("testcasename").split("#")[0] != currentFeature){
            $(this).parent().remove();
        }
    });
    
    //filter by release
    var colIndex = 0;
    for(var i in kpiIndexList){
        var curIndex = parseInt(kpiIndexList[i]);
        colIndex = (curIndex-1)/2 + 5;
        if(curIndex < startKpiIndex || curIndex > endKpiIndex){
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
            var symbol = $(this).find("td:eq(3)").html().indexOf("+") > 0 ? "-":"";
            var tt = parseFloat($(this).find("td:eq(2) .ttWarning").html().replace(/%/g,""));
            $(this).find("td:gt(4)").each(function(){
                if(!isNaN(parseFloat($(this).find("span").html().replace(/%/g,""))) && parseFloat((symbol+$(this).find("span").html().replace(/%/g,"")).replace(/--/g,"")) > tt){
                    isShow = true;
                    //return false;
                }else{
                    $(this).html("");
                }
            });
            if(!isShow){ $(this).remove(); }
        });
    }
    if(isShowImprovement == true){
        $("#r_content tr:gt(0)").each(function(i){
            var isShow = false;
            var symbol = $(this).find("td:eq(3)").html().indexOf("+") > 0 ? "-":"";
            var tt = parseFloat($(this).find("td:eq(2) .ttWarning").html().replace(/%/g,""));
            $(this).find("td:gt(4)").each(function(){
                if(!isNaN(parseFloat($(this).find("span").html().replace(/%/g,""))) && parseFloat((symbol+$(this).find("span").html().replace(/%/g,"")).replace(/--/g,"")) < -tt){
                    isShow = true;
                    //return false;
                }else{
                    $(this).html("");
                }
            });
            if(!isShow){ $(this).remove(); }
        });
    }
    if(isShowFailed == true){
        $("#r_content tr:gt(0)").each(function(i){
            var isShow = false;
            var symbol = $(this).find("td:eq(3)").html().indexOf("+") > 0 ? "-":"";
            var target = parseFloat($(this).find("td:eq(2) .margin").html().split("/")[0]);
            var margin = parseFloat($(this).find("td:eq(2) .margin").html().split("/")[1].replace(/%/g,""));
            $(this).find("td:gt(3)").each(function(){
                var score = parseFloat($(this).find("a").html().replace(/,/g,""));
                var offset = symbol == "-" && target != 0 ? (target-score)/target:(score-target)/score;
                if(target != 0 && !isNaN(offset) && offset*100 > margin){
                    isShow = true;
                    //return false;
                }else{
                    $(this).html("");
                }
            });
            if(!isShow){ $(this).remove(); }
        });
    }
    
    _w_table_rowspan("#r_content",1,1);
    $("#r_content").fixedHeaderTable({ autoShow:true,autoResize: true, });
}

function SaveComment(){
    console.log(sltdKpi);
    console.log(sltdRelease);
    var record = { "deviceid":deviceid,"releaseid":sltdRelease,"kpiid":sltdKpi,"comment":$("#comment").val() };
    var url = "http://"+serverHost+"/rest/editcomment";
    $.ajax({
        type: 'POST',
        data: { "record": JSON.stringify(record) },
        url: url,
        success: function(data) {
            console.log(data)
        }
    });
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
}
String.prototype.startWith=function(str){ 
var reg=new RegExp("^"+str); 
return reg.test(this); 
} 