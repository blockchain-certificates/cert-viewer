
$(document).ready(function() {
	var clipboard = new Clipboard('#copy-btn');

  $('#copy-btn').tooltip({'trigger': 'click', delay: { "show": 500, "hide": 100 }});

  $("#generatekeys").click(function(){

    $("#keys").hide();
    $("#print-btn").hide();
    $("#copy-btn").hide();
    $("#return-link").hide();

    var keyPair = bitcoin.ECPair.makeRandom();
    $('#privKey').text(keyPair.toWIF());
    $('#pubKey').text(keyPair.getAddress());
    $("#pubKeyQr").html("");
    $("#privKeyQr").html("");

    var qrcode1 = new QRCode(document.getElementById("pubKeyQr"), {
      text: keyPair.getAddress(),
      width: 70,
      height: 70,
      colorDark : "#000000",
      colorLight : "#ffffff",
      correctLevel : QRCode.CorrectLevel.H
    });
    var qrcode2 = new QRCode(document.getElementById("privKeyQr"), {
      text: keyPair.toWIF(),
      width: 60,
      height: 60,
      colorDark : "#000000",
      colorLight : "#ffffff",
      correctLevel : QRCode.CorrectLevel.H
    });

    $("#to-load").show();
    $("#to-load").Loadingdotdotdot({
        "speed": 400,
        "maxDots": 4,
        "word": "Loading"
    });

    setTimeout(
      function() 
      {
        $("#keys").show();
        $("#print-btn").show();
        $("#copy-btn").show();
        $("#return-link").attr('href', '/request?identity=true&address='+keyPair.getAddress());
        $("#return-link").show();
        $("#to-load").Loadingdotdotdot("Stop");
        $("#to-load").hide();
      }, 5000);

  });

  clipboard.on('success', function(e) {
      console.info('Action:', e.action);
      console.info('Text:', e.text);
      console.info('Trigger:', e.trigger);
      e.clearSelection();
  });

  clipboard.on('error', function(e) {
      console.error('Action:', e.action);
      console.error('Trigger:', e.trigger);
  });
});