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

function printStatus(data) {
	$("#total-status").html(data.status);
	$("#apic-status").html(data.apic.status);
	$("#genian-status").html(data.genian.status);
	$("#target-epg-list").val(data.target_epg_list.join(", "));
	$("#apic-address").val(data.apic.address);
	$("#apic-username").val(data.apic.username);
	$("#apic-password").val(data.apic.password);
	$("#genian-address").val(data.genian.address);
	$("#genian-passkey").val(data.genian.passkey);
}

function getStatus() {
    $.ajax({
        url: document.location.origin + "/appcenter/Ciscokr/GeniNacTrigger/genaci.json",
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        headers: {
            "DevCookie": window.APIC_DEV_COOKIE,
            "APIC-challenge": window.APIC_URL_TOKEN
        },
        success: function(data) {
        	printStatus(data);
        },
        error: function(xhr, status, thrown) {
			window.alert("error");
		}
    });
}

function setStatus() {
    $.ajax({
        url: "/appcenter/Ciscokr/GeniNacTrigger/genaci.json",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify({
    		target_epg_list: $("#target-epg-list").val(),
    		apic: {
    			address: $("#apic-address").val(),
    			username: $("#apic-username").val(),
    			password: $("#apic-password").val()
    		},
    		genian: {
    			address: $("#genian-address").val(),
    			passkey: $("#genian-passkey").val()
    		}
    	}),
    	headers: {
            "DevCookie": window.APIC_DEV_COOKIE,
            "APIC-challenge": window.APIC_URL_TOKEN
        },
        success: function(data) {
        	printStatus(data);
        },
        error: function(xhr, status, thrown) {
        	window.alert("error");
		}
    });
}

$(document).ready(function() {
	$("#genaci-submit").click(function() { setStatus(); });
	getStatus();
});
