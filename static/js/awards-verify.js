$(document).ready(function() {

	$( "#verify-button" ).click(function() {

		data = decodeURIComponent($(this).attr("value"));

		$.ajax({                                                                                                           
            type:'POST', 
            url: "/verify",
            data: data,                                                                                                                                                                                                       
            beforeSend:function(){                                                                                         
                $("#progress-msg").Loadingdotdotdot({
			    	"speed": 400,
			    	"maxDots": 4,
			    	"word": "Verifying OP_RETURN"
				});                                                                               
            },
            success:function(res){
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
            },                                                                                                                                                                                                                                                                    
        });

	});
});
