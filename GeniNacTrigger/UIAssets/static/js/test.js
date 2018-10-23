

function getStatus() {
	
	var target_epg_list = [
		"A/App1/WEB",
		"B/App2/WAS",
		"C/APP3/DB"
	];
	var merge_path = target_epg_list.join(", ");
	
	$("#total-status").html("Test 1");
	$("#apic-status").html("Test 2");
	$("#genian-status").html("Test 3");
	
	$("#target-epg-list").val(merge_path);
	
	$("#apic-address").val("Test 4");
	$("#apic-username").val("Test 5");
	$("#apic-password").val("Test 6");
	
	$("#genian-address").val("Test 7");
	$("#genian-passkey").val("Test 8");
	
	console.log($("#target-epg-list").val());
}


$(document).ready(function() {
	getStatus();
	console.log("OK")
});