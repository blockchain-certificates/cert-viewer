loading_messages = [
	'Computing SHA256 digest of local certificate...', 
	'Fetching hash in OP_RETURN field from blockchain.info...', 
	'Comparing local hash to hash stored on the blockchain...']



$(document).ready(function() {
	$( "#verify-button" ).click(function() {
		var counter = 0
		$("#progress-msg").text(loading_messages[counter])
		$("#progress-msg").show()
		var data = $(this).attr('value');
		url = '/verify?'+data
		$.get(url, function(res){
    		if(res=="True"){
    			var timerId = 0;
    			timerId = setInterval(change, 2000)
    			function change() {
					counter++;
					if(counter >= loading_messages.length) { 
					    	$("#verified").show()
				        	$("#progress-msg").hide()  
				        	clearInterval(timerId);
					    }
					$("#progress-msg").html($("#progress-msg").html()+"<br>"+loading_messages[counter]);
				    }
        	}
        	else{
        		$("#not-verified").show()
        		$("#progress-msg").hide()
        	}
		})
	});
});