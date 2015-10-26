loading_messages = [
	{'message': 'Computing SHA256 digest of local certificate', 'results': 'DONE'}, 
	{'message': 'Fetching hash in OP_RETURN field', 'results': 'DONE'}, 
	{'message': 'Comparing local and blockchain hashes', 'results': {'True': 'PASS', 'False': 'FAIL'}},
	{'message': 'Checking Media Lab signature', 'results': {'True': 'PASS', 'False': 'FAIL'}},
	{'message': '', 'results': {'True': 'PASS', 'False': 'FAIL'}}
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
			if(res.indexOf("Oops") > -1){
				return mark['False']
			}
			if(res.indexOf("Success") > -1){
				return mark['True']
			}
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
		for (i=0; i<urls.length; i++){
			(function(index) {
	        	var progress = (index+1).toString()+"/"+(urls.length-1).toString();
				makeCall(index, data, function(res, index){
					setTimeout(function(){
					    $("#progress-msg").show();
						$("#progress-msg").html($("#progress-msg").html()+loading_messages[index]['message']+'</span>');
						var mark = getMark(index, res);
						setTimeout(function(){
							if(index == urls.length-1){
								if(res.indexOf("Oops!")>-1){
									$("#not-verified").show()
								}
								else{
									$("#verified").show()
								}
								$("#progress-msg").html($("#progress-msg").html()+res);
							}
							else{
								$("#progress-msg").html($("#progress-msg").html()+' ['+mark+' '+progress+']<br>');
							}
						}, timeDelay-500)
					}, timeDelay*index);
				});
		    })(i);
		}
	});
});
