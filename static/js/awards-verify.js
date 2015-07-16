$(document).ready(function() {

	$( "#verify-button" ).click(function() {

		$("#progress-msg").Loadingdotdotdot({
		    "speed": 400,
		    "maxDots": 4,
		    "word": "Verifying signature"
		});

		//$("#verified-icon").show()
		//$("#progress-msg").html('Verified.')
	});
});
