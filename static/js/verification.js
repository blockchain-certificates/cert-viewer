function hidefields(fields){
	for(i=0; i<fields.length; i++){
		$(fields[i]).hide();
	}
}

function renderResponse(i, len, data){
	setTimeout(function(){
		count = i+1;
		total = len-1;
		message = data[0];
		value = data[1];
		if(i != len-1){
			$("#progress-msg").html($("#progress-msg").html()+'Step ' + count.toString() +' of ' + total.toString() + "... " +message+'</span>');
		}
		setTimeout(function(){
			if(i == len-1){
				if(value==true){
					$("#progress-msg").html($("#progress-msg").html()+"Success! The certificate has been verified.")
					$("#verified").show();
				}
				else{
					$("#progress-msg").html($("#progress-msg").html()+"Oops! The certificate could not be verified.")
					$("#not-verified").show();
				}
			}
			else{
				$("#progress-msg").html($("#progress-msg").html()+'  ['+markMappings[value]+']<br>')
			}
		}, 1000)

	}, timeDelay*i);
}

timeDelay = 2000;
markMappings = {true: "PASS", false: "FAIL", "DONE": "DONE"}

$(document).ready(function() {
	$( "#verify-button" ).click(function() {
		hidefields("#not-verified", "#verified");
		$("#progress-msg").html("");
		var data = $(this).attr('value');
		$.get("/verify?"+data, function(res){
			res = JSON.parse(res);
			$("#progress-msg").show();
			if(res == null){
				$("#progress-msg").html($("#progress-msg").html()+"Oops! There was an issue connecting to the Blockchain.info API")
			}
			else{
				for(i=0; i<res.length; i++){
					renderResponse(i, res.length, res[i])
				}
			}
		});
	});
});