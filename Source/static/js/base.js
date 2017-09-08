/**
 * Created by Administrator on 2017/3/6.
 */


function goToUrl(url, msg){
    if (msg == null){
        window.location.href = url;
        return;
    }
    if (msg != ""){
        if (window.confirm(msg)) {
            window.location.href = url;
            return;
        }
        else{
            return;
        }
    }
    window.location.href = url;
}

function AjaxSender(urlStr, methodStr, successFun, errorFun, jsonData) {
    $.ajax({
        url: urlStr,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFTOKEN", $.cookie('csrftoken'));
            xhr.setRequestHeader("auth-token", $.cookie('auth-token'));
        },
        type: methodStr,
        data: jsonData,
        crossDomain: false,
        error: errorFun,
        success: successFun,
        dataType: 'json'
    });
}

function EzAjaxGet(url, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "get", success, failed);
}

function EzAjaxPut(url, json_param, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "put", success, failed, json_param);
}

function EzAjaxPost(url, json_param, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "post", success, failed, json_param);
}

function EzAjaxDelete(url, success, failed) {
    failed = failed || function (data) {
        console.log(data);
    };
    AjaxSender(url, "delete", success, failed);
}

function isNone(obj){
    return obj == "" || obj==null || obj==undefined || obj=={};
}

function getUrlParam(name) {
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}


Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};
