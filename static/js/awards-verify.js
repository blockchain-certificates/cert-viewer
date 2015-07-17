$(document).ready(function() {
	$( "#verify-button" ).click(function() {
		var data = $(this).attr('value');
		$("#progress-msg").Loadingdotdotdot({
				"speed": 400,
				"maxDots": 4,
				"word": "Verifying OP_RETURN"
			});
		url = '/verify?'+data
		$.get(url, function(res){
			setTimeout(function(){
        		$("#progress-msg").Loadingdotdotdot("Stop");
        		if(res=="True"){
            		$("#verified-icon").show()
            		$("#progress-msg").html('Verified.')  
            	}
            	else{
            		$("#not-verified-icon").show()
            		$("#progress-msg").html('Unable to verify.')  
            	}
            }, 3000)
		})
	});
});