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
	    	var convertedImg = new Image();

	    	img.onload = function(){	

	            canvas.width = img.width;
	            canvas.height = img.height;
	            ctx.drawImage(img, 0, 0);
	            
	            // Processing pixels and thresholding the image
	            var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
	            var threshold = 100;

	            for (var i = 0; i < imgData.data.length; i += 4) {
				    var r = imgData.data[i];
				    var g = imgData.data[i+1];
				    var b = imgData.data[i+2];
				    var v = (0.2126 * r + 0.7152 * g + 0.0722 * b >= threshold) ? 255 : 0;
				    imgData.data[i] = imgData.data[i+1] = imgData.data[i+2] = v
				}

				ctx.putImageData(imgData, 0, 0);
				convertedImg.src = canvas.toDataURL();

				qrcode.decode(convertedImg.src); 
	        }
	        
	        img.src = event.target.result; 
	    }

	    reader.readAsDataURL(e.target.files[0]); 
	}

	function revealUrl(data) {
		$('#js-scan-btn').button('reset');
		if (isUrl(data) == true) {
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