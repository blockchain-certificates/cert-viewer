loading_messages = [
	'Computing SHA256 digest of local certificate...', 
	'Fetching hash in OP_RETURN field from the blockchain...', 
	'Comparing local hash to hash stored on the blockchain...',
	'Checking cryptographic signature in certificate...',
	'Determining validility...'
	]

urls = ['/computeHash', '/fetchHashFromChain', '/compareHashes', '/checkAuthor', '/verify']

// $(document).ready(function() {
// 	$( "#verify-button" ).click(function() {
// 		var counter = 0
// 		$("#progress-msg").text(loading_messages[counter])
// 		$("#progress-msg").show()
// 		var data = $(this).attr('value');
// 		url = '/verify?'+data
// 		$.get(url, function(res){
//     		if(res=="True"){
//     			var timerId = 0;
//     			timerId = setInterval(change, 2000)
//     			function change() {
// 					counter++;
// 					if(counter >= loading_messages.length) { 
// 					    	$("#verified").show()
// 				        	$("#progress-msg").hide()  
// 				        	clearInterval(timerId);
// 					    }
// 					$("#progress-msg").html($("#progress-msg").html()+"<br>"+loading_messages[counter]);
// 				    }
//         	}
//         	else{
//         		$("#not-verified").show()
//         		$("#progress-msg").hide()
//         	}
// 		})
// 	});
// });

var timeFactor = 4000

function makeCall(i, data, callback){
	var t = i*Math.random()*timeFactor/7
	setTimeout(function(){
		var url = urls[i]+"?"+data;
		$.get(url, function(res){
			callback(res, i);
		})
	}, t)
}

$(document).ready(function() {
	$( "#verify-button" ).click(function() {
		$("#not-verified").hide();
		$("#verified").hide();
		$("#progress-msg").html("");
		$("#progress-msg").show();
		var data = $(this).attr('value');
		for (i=0; i<urls.length; i++){
			(function(index) {
		        setTimeout(function() {
		        	$("#progress-msg").html($("#progress-msg").html()+loading_messages[index]+'</span>');
						makeCall(i, data, function(res, index){
						if(index == urls.length-1){
							if(res.indexOf("Oops!")>-1){
								$("#not-verified").show()
							}
							else{
								$("#verified").show()
							}
						}
						$("#progress-msg").html($("#progress-msg").html()+'<br><span class="return-fields font-light okay-field ">[DONE]</span><br>');
					});
		        }, i * timeFactor);
		    })(i);
		}
		// for (i=0; i<urls.length; i++){
		// 	var url = urls[i]+"?"+data;
		// 	$.get(url, function(res){
		// 		console.log(res);
	 //        })
		// }
	});
});