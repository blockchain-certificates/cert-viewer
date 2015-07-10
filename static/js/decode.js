$( document ).ready(function() {
    
    qrcode.callback = revealUrl;

	var imageLoader = document.getElementById('js-qr-input');
    imageLoader.addEventListener('change', handleImage, false);

	function isUrl(s) {
	    var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
	    return regexp.test(s);
	}

	function handleImage(e){
	    var reader = new FileReader();
	    $('#js-scan-btn').button('loading');
	    reader.onload = function(event){
	    	var canvas = document.getElementById("qr-canvas");
    		var ctx = canvas.getContext("2d");
	    	var img = new Image();
	    	img.onload = function(){
	            canvas.width = img.width;
	            canvas.height = img.height;
	            ctx.drawImage(img,0,0);
	            qrcode.decode(event.target.result);
	        }
	        img.src = event.target.result;
	    }
	    reader.readAsDataURL(e.target.files[0]); 
	}


	function revealUrl(data) {
		$('#js-scan-btn').button('reset');
		if (isUrl(data)==true) {
			// window.location.replace(data);
			alert(data);
		}
		else{
			alert('Oops! Please try again.');
		}
	  }

    $('#js-scan-btn').click(function(){
    	$("#js-qr-input").click();
    });

});