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
	$("#app-status").html(data.status);
	switch(data.status) {
		"running":
			$("#app-status-alert").attr("class", "alert alert-success");
			break;
		"Genian NAC is not ready":
		"APIC is not ready":
			$("#app-status-alert").attr("class", "alert alert-warning");
			break;
		"stopped":
			$("#app-status-alert").attr("class", "alert alert-danger");
			break;
	}
	$("#apic-status").html(data.apic.status);
	switch(data.apic.status) {
		"connected":
			$("#apic-status-alert").attr("class", "alert alert-success");
			break;
		"disconnected":
			$("#apic-status-alert").attr("class", "alert alert-danger");
			break;
	}
	$("#genian-status").html(data.genian.status);
	switch(data.genian.status) {
		"connected":
			$("#genian-status-alert").attr("class", "alert alert-success");
			break;
		"disconnected":
			$("#genian-status-alert").attr("class", "alert alert-danger");
			break;
	}
	
	var target_epg_list_html = "";
	for (i in data.target_epg_list) {
		target_epg_list_html += '<li class="list-group-item">' + data.target_epg_list[i] + '</li>';
	}
	$("#apic-status-epg-list").html(target_epg_list_html);
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
        url: document.location.origin + "/appcenter/Ciscokr/GeniNacTrigger/genaci.json",
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
        	console.log(xhr);
        	console.log(status);
        	console.log(thrown);
        	window.alert("error");
		}
    });
}

function getLogging() {
	$.ajax({
        url: document.location.origin + "/appcenter/Ciscokr/GeniNacTrigger/logging.json",
        type: "GET",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        headers: {
            "DevCookie": window.APIC_DEV_COOKIE,
            "APIC-challenge": window.APIC_URL_TOKEN
        },
        success: function(data) {
        	$("#logging-text").html(data.join("<br/>"));
        },
        error: function(xhr, status, thrown) {
			window.alert("error");
		}
    });
}

function delLogging() {
	$.ajax({
        url: document.location.origin + "/appcenter/Ciscokr/GeniNacTrigger/logging.json",
        type: "DELETE",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        headers: {
            "DevCookie": window.APIC_DEV_COOKIE,
            "APIC-challenge": window.APIC_URL_TOKEN
        },
        success: function(data) {
        	if (data.result == true) { window.alert("old log files are deleted"); }
        	else { window.alert("deleting old log files failed"); }
        },
        error: function(xhr, status, thrown) {
			window.alert("deleting old log files failed");
		}
    });
}

$(document).ready(function() {
	$("#genaci-submit").click(function() { setStatus(); });
	$("#logging-refresh").click(function() { getLogging(); });
	$("#logging-delete").click(function() { delLogging(); });
	getStatus();
	getLogging();
});
