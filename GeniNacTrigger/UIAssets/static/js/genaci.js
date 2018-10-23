
function getStatus(){
    return $.ajax({
        url: "/appcenter/Ciscokr/GeniNacTrigger/genaci.json",
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        headers: {
            "DevCookie": Cookies.get("app_Ciscokr_GeniNacTrigger_token"),
            "APIC-Challenge": Cookies.get("app_Ciscokr_GeniNacTrigger_urlToken")
        },
        success: function(data) {
        	console.log(data);
        	$("#total-status").html(data.status);
        	$("#apic-status").html(data.apic.status);
        	$("#genian-status").html(data.genian.status);
        },
        error: function(xhr, status, thrown) {
			window.alert(xhr, status, thrown);
		}
    });
}

function setStatus(data){
    return $.ajax({
        url: "/appcenter/Ciscokr/GeniNacTrigger/genaci.json",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(data),
        headers: {
            "DevCookie": Cookies.get("app_Ciscokr_GeniNacTrigger_token"),
            "APIC-Challenge": Cookies.get("app_Ciscokr_GeniNacTrigger_urlToken")
        },
        success: function(data) {
        	console.log(data);
        },
        error: function(xhr, status, thrown) {
			window.alert(xhr, status, thrown);
		}
    });
}

$(document).ready(function() {
	
	window.APIC_DEV_COOKIE = Ext.util.Cookies.get("app_Ciscokr_GeniNacTrigger_token");
	window.APIC_URL_TOKEN =  Ext.util.Cookies.get("app_Ciscokr_GeniNacTrigger_urlToken");
	window.addEventListener('message', function (e) {
		if (e.source === window.parent) {
			var tokenObj = Ext.decode(e.data, true);
			if (tokenObj) {
				window.APIC_DEV_COOKIE = tokenObj.token;
				window.APIC_URL_TOKEN = tokenObj.urlToken;
			}
		}
	});
	
	getStatus();
}