

function getStatus() {
	
	var target_epg_list = [
		"A/App1/WEB",
		"B/App2/WAS",
		"C/APP3/DB"
	];
	var merge_path = target_epg_list.join(", ");
	
	$("#app-status").html("Test 1");
	$("#apic-status").html("Test 2");
	$("#genian-status").html("Test 3");
	$("#app-status-alert").attr("class", "alert alert-warning")
	$("#apic-status-alert").attr("class", "alert alert-success")
	$("#genian-status-alert").attr("class", "alert alert-danger")
	
	var epg_list = "";
	for (i in target_epg_list) {
		epg_list += '<li class="list-group-item">' + target_epg_list[i] + '</li>';
	}
	$("#apic-status-epg-list").html(epg_list);
	
	$("#target-epg-list").val(merge_path);
	
	$("#apic-address").val("Test 4");
	$("#apic-username").val("Test 5");
	$("#apic-password").val("Test 6");
	
	$("#genian-address").val("Test 7");
	$("#genian-passkey").val("Test 8");
	
	console.log($("#target-epg-list").val());
}

function printLogging() {
	var logging = [
	    "[2018-10-24 14:56:03,052] 127.0.0.1 - - [2018-10-24 14:56:03] \"GET /logging.json HTTP/1.1\" 200 2375 0.003903",
	    "[2018-10-24 14:56:03,806] 127.0.0.1 - - [2018-10-24 14:56:03] \"GET /logging.json HTTP/1.1\" 200 2376 0.004881",
	    "[2018-10-24 14:56:04,375] 127.0.0.1 - - [2018-10-24 14:56:04] \"GET /logging.json HTTP/1.1\" 200 2378 0.003905",
	    "[2018-10-24 14:56:04,928] 127.0.0.1 - - [2018-10-24 14:56:04] \"GET /logging.json HTTP/1.1\" 200 2389 0.004882",
	    "[2018-10-24 14:56:05,453] 127.0.0.1 - - [2018-10-24 14:56:05] \"GET /logging.json HTTP/1.1\" 200 2353 0.005856",
	    "[2018-10-24 14:56:05,998] 127.0.0.1 - - [2018-10-24 14:56:05] \"GET /logging.json HTTP/1.1\" 200 2370 0.004879",
	    "[2018-10-24 14:56:06,595] 127.0.0.1 - - [2018-10-24 14:56:06] \"GET /logging.json HTTP/1.1\" 200 2371 0.005856",
	    "[2018-10-24 14:56:07,158] 127.0.0.1 - - [2018-10-24 14:56:07] \"GET /logging.json HTTP/1.1\" 200 2372 0.004878",
	    "[2018-10-24 14:56:07,709] 127.0.0.1 - - [2018-10-24 14:56:07] \"GET /logging.json HTTP/1.1\" 200 2392 0.004881",
	    "[2018-10-24 14:56:08,313] 127.0.0.1 - - [2018-10-24 14:56:08] \"GET /logging.json HTTP/1.1\" 200 2411 0.005857",
	    "[2018-10-24 14:56:08,852] 127.0.0.1 - - [2018-10-24 14:56:08] \"GET /logging.json HTTP/1.1\" 200 2429 0.004879",
	    "[2018-10-24 14:56:09,401] 127.0.0.1 - - [2018-10-24 14:56:09] \"GET /logging.json HTTP/1.1\" 200 2444 0.004880",
	    "[2018-10-24 14:56:09,917] 127.0.0.1 - - [2018-10-24 14:56:09] \"GET /logging.json HTTP/1.1\" 200 2494 0.004933",
	    "[2018-10-24 14:56:10,506] 127.0.0.1 - - [2018-10-24 14:56:10] \"GET /logging.json HTTP/1.1\" 200 2505 0.004875",
	    "[2018-10-24 14:56:11,033] 127.0.0.1 - - [2018-10-24 14:56:11] \"GET /logging.json HTTP/1.1\" 200 2528 0.003905",
	    "[2018-10-24 14:56:11,700] 127.0.0.1 - - [2018-10-24 14:56:11] \"GET /logging.json HTTP/1.1\" 200 2526 0.003904",
	    "[2018-10-24 14:56:12,200] 127.0.0.1 - - [2018-10-24 14:56:12] \"GET /logging.json HTTP/1.1\" 200 2524 0.004869",
	    "[2018-10-24 14:56:12,751] 127.0.0.1 - - [2018-10-24 14:56:12] \"GET /logging.json HTTP/1.1\" 200 2522 0.004881",
	    "[2018-10-24 14:56:13,307] 127.0.0.1 - - [2018-10-24 14:56:13] \"GET /logging.json HTTP/1.1\" 200 2486 0.004879",
	    "[2018-10-24 14:56:13,844] 127.0.0.1 - - [2018-10-24 14:56:13] \"GET /logging.json HTTP/1.1\" 200 2503 0.004879",
	    "[2018-10-24 14:56:14,373] 127.0.0.1 - - [2018-10-24 14:56:14] \"GET /logging.json HTTP/1.1\" 200 2504 0.004880",
	    "[2018-10-24 14:56:14,857] 127.0.0.1 - - [2018-10-24 14:56:14] \"GET /logging.json HTTP/1.1\" 200 2504 0.003902",
	    "[2018-10-24 14:56:15,359] 127.0.0.1 - - [2018-10-24 14:56:15] \"GET /logging.json HTTP/1.1\" 200 2504 0.003903",
	    "[2018-10-24 14:56:20,654] 127.0.0.1 - - [2018-10-24 14:56:20] \"GET /logging.json HTTP/1.1\" 200 2504 0.003905",
	    "[2018-10-24 14:56:21,192] 127.0.0.1 - - [2018-10-24 14:56:21] \"GET /logging.json HTTP/1.1\" 200 2504 0.005854",
	    "[2018-10-24 14:56:21,694] 127.0.0.1 - - [2018-10-24 14:56:21] \"GET /logging.json HTTP/1.1\" 200 2504 0.005854",
	    "[2018-10-24 14:56:22,278] 127.0.0.1 - - [2018-10-24 14:56:22] \"GET /logging.json HTTP/1.1\" 200 2504 0.003930",
	    "[2018-10-24 14:56:22,902] 127.0.0.1 - - [2018-10-24 14:56:22] \"GET /logging.json HTTP/1.1\" 200 2504 0.005855",
	    "[2018-10-24 14:56:23,339] 127.0.0.1 - - [2018-10-24 14:56:23] \"GET /logging.json HTTP/1.1\" 200 2504 0.005855",
	    "[2018-10-24 14:56:23,756] 127.0.0.1 - - [2018-10-24 14:56:23] \"GET /logging.json HTTP/1.1\" 200 2504 0.020460",
	    "[2018-10-24 14:56:24,139] 127.0.0.1 - - [2018-10-24 14:56:24] \"GET /logging.json HTTP/1.1\" 200 2504 0.004878",
	    "[2018-10-24 14:56:25,057] 127.0.0.1 - - [2018-10-24 14:56:25] \"GET /logging.json HTTP/1.1\" 200 2504 0.004879",
	    "[2018-10-24 14:56:25,486] 127.0.0.1 - - [2018-10-24 14:56:25] \"GET /logging.json HTTP/1.1\" 200 2504 0.004880",
	    "[2018-10-24 14:57:21,081] register uri {GET:/genaci.json} link to {engine.get_status(...)}",
	    "[2018-10-24 14:57:21,082] register uri {POST:/genaci.json} link to {engine.set_config(...)}",
	    "[2018-10-24 14:57:21,082] register uri {GET:/logging.json} link to {engine.get_logging(...)}",
	    "[2018-10-24 14:57:21,082] register uri {DELETE:/logging.json} link to {engine.del_logging(...)}",
	    "[2018-10-24 14:57:21,083] directory dir::engine is installed",
	    "[2018-10-24 14:57:27,440] 127.0.0.1 - - [2018-10-24 14:57:27] \"GET /logging.json HTTP/1.1\" 200 5690 0.004910",
	    "[2018-10-24 15:14:16,680] register uri {GET:/genaci.json} link to {engine.get_status(...)}",
	    "[2018-10-24 15:14:16,680] register uri {POST:/genaci.json} link to {engine.set_config(...)}",
	    "[2018-10-24 15:14:16,680] register uri {GET:/logging.json} link to {engine.get_logging(...)}",
	    "[2018-10-24 15:14:16,680] register uri {DELETE:/logging.json} link to {engine.del_logging(...)}",
	    "[2018-10-24 15:14:16,684] directory dir::engine is installed",
	    "[2018-10-24 15:14:28,561] 127.0.0.1 - - [2018-10-24 15:14:28] \"GET /logging.json HTTP/1.1\" 200 5704 0.003928",
	    "[2018-10-24 15:18:56,284] 127.0.0.1 - - [2018-10-24 15:18:56] \"GET /logging.json HTTP/1.1\" 200 5702 0.005857",
	    "[2018-10-24 15:19:12,916] register uri {GET:/genaci.json} link to {engine.get_status(...)}",
	    "[2018-10-24 15:19:12,917] register uri {POST:/genaci.json} link to {engine.set_config(...)}",
	    "[2018-10-24 15:19:12,917] register uri {GET:/logging.json} link to {engine.get_logging(...)}",
	    "[2018-10-24 15:19:12,917] register uri {DELETE:/logging.json} link to {engine.del_logging(...)}",
	    "[2018-10-24 15:19:12,919] directory dir::engine is installed"
	];
	
	logging_html = logging.join("<br/>");
	$("#logging-text").html(logging_html);

}

$(document).ready(function() {
	getStatus();
	printLogging();
	console.log("OK")
});