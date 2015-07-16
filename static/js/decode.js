$( document ).ready(function() {

	var imageLoader = document.getElementById('js-qr-input');
    imageLoader.addEventListener('change', handleImage, false);

	function handleImage(e){
	    var reader = new FileReader();

	    reader.onload = function(event){
	    	var canvas = document.getElementById("qr-canvas");
    		var ctx = canvas.getContext("2d");
	    	var img = new Image();
	    	var convertedImg = new Image();
 
	    	img.onload = function() {	

	            canvas.width = img.width/4;
	            canvas.height = img.height/4;
	            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
	            
	            // Processing pixels and thresholding the image
	            var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);

	            var stepSize = 4*4;

	            var contrast = 180;
			    var factor = (259 * (contrast + 255)) / (255 * (259 - contrast));

			    var sum = 0;
			    var num = 0;

	            for (var i = 0; i < imgData.data.length-stepSize; i += stepSize) { //histogram

	    		    	var r = imgData.data[i];
	        			var g = imgData.data[i+1];
	        			var b = imgData.data[i+2];
					    var v = (0.2126 * r + 0.7152 * g + 0.0722 * b);

	    		    	var rn = imgData.data[i+stepSize];
	        			var gn = imgData.data[i+stepSize+1];
	        			var bn = imgData.data[i+stepSize+2];
					    var vn = (0.2126 * rn + 0.7152 * gn + 0.0722 * bn);

					    if(v-vn > 13){
					    	num += 1;
					    	sum = sum + vn;
						}
					    else if(vn-v > 13){
					    	num += 1;
					    	sum = sum + v;
						}
				}

				var average = 100;
				if(num > 0){
					average = sum/num;
				}

			    var pivot = average+12;
				var threshold = average+18;

				for (var i = 0; i < imgData.data.length; i += 4) { //contrast
 
        			var r = imgData.data[i];
        			var g = imgData.data[i+1];
        			var b = imgData.data[i+2];

    		    	r = factor * (r - pivot) + pivot;
        			g = factor * (g - pivot) + pivot;
        			b = factor * (b - pivot) + pivot;

        			var l = (0.2126 * r + 0.7152 * g + 0.0722 * b);
        			if(l>255) l = 255;
        			if(l<0) l = 0;
        			
				    var v = (l >= threshold) ? 255 : 1.*(l-threshold)+threshold;
				    imgData.data[i] = imgData.data[i+1] = imgData.data[i+2] = v;				  
				}


				ctx.putImageData(imgData, 0, 0);
				convertedImg.src = canvas.toDataURL();

				var qr = new QCodeDecoder();

				qr.decodeFromImage(convertedImg, function(er, res) {

					$(".result").addClass('show');
				    $(".result").removeClass('hide');

					if(er) {
				    	$(".result").text("Error decoding QR Code from Image");
				    	return;
					}

				    $(".result").html('<a href="' + res + '">' + res + '</a>');
				 });

	        }
	        
	        img.src = event.target.result; 
	    }

	    reader.readAsDataURL(e.target.files[0]); 
	}

    $('#js-scan-btn').click(function(){
    	$("#js-qr-input").click();

    	$(".result").addClass('hide');
		$(".result").removeClass('show');
    });

});