loading_messages = [
	{'message': 'Computing SHA256 digest of local certificate...', 'results': 'DONE'}, 
	{'message': 'Fetching hash in OP_RETURN field from the blockchain...', 'results': 'DONE'}, 
	{'message': 'Comparing local hash to hash stored on the blockchain...', 'results': {'True': 'PASS', 'False': 'FAIL'}},
	{'message': 'Checking cryptographic signature in certificate...', 'results': {'True': 'PASS', 'False': 'FAIL'}},
	{'message': 'Determining validility...', 'results': 'DONE'}
	]

urls = ['/computeHash', '/fetchHashFromChain', '/compareHashes', '/checkAuthor', '/verify']

timeDelay = 2000;

function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
  }

function callUrl(i, data, callback){
	var url = urls[i]+"?"+data;
	$.get(url, function(res){
		callback(res, i);
	})
}

function makeCall(i, data, callback){
	callUrl(i, data, callback)
}

function getMark(index, res){
	var mark = loading_messages[index]['results']
	if (mark.constructor == Object){
			return mark[res]
	}
	return mark
}

$(document).ready(function() {
	$( "#verify-button" ).click(function() {
		$("#not-verified").hide();
		$("#verified").hide();
		$("#progress-msg").html("");
		var data = $(this).attr('value');
		var timeFactors = []
		for (i=0; i<urls.length; i++){
			(function(index) {
	        	var progress = (index+1).toString()+"/"+urls.length.toString();
				makeCall(index, data, function(res, index){
					setTimeout(function(){
					    $("#progress-msg").show();
						$("#progress-msg").html($("#progress-msg").html()+loading_messages[index]['message']+'</span>');
						var mark = getMark(index, res)
						setTimeout(function(){
							if(index == urls.length-1){
								if(res.indexOf("Oops!")>-1){
									$("#not-verified").show()
								}
								else{
									$("#verified").show()
								}
								$("#progress-msg").html($("#progress-msg").html()+'<br><span class="return-fields font-light">'+res+'<span class="okay-field">['+mark+' '+progress+']</span></span><br>');
							}
							else{
								$("#progress-msg").html($("#progress-msg").html()+'<br><span class="return-fields font-light okay-field ">['+mark+' '+progress+']</span><br>');
							}
						}, timeDelay)
					}, timeDelay*index);
				});
		    })(i);
		}
	});
});