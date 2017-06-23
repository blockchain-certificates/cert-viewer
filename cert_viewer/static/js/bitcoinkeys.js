$(document).ready(function () {
    var clipboard = new Clipboard('#copy-btn');

    jQuery( '#copy-btn' ).ready(function( ) {
        $('.hasTooltip').tooltip({'trigger': 'click', delay: {"show": 500, "hide": 100}});
    });

    $("#generatekeys").click(function () {

        $(".show-later").hide();
        var keyPair = bitcoin.ECPair.makeRandom();
        $('#privKey').text(keyPair.toWIF());
        $('#pubKey').text(keyPair.getAddress());
        $(".enable-clear").html("");

        var qrcode1 = new QRCode(document.getElementById("pubKeyQr"), {
            text: keyPair.getAddress(),
            width: 70,
            height: 70,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });
        var qrcode2 = new QRCode(document.getElementById("privKeyQr"), {
            text: keyPair.toWIF(),
            width: 60,
            height: 60,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });

        $("#to-load").show();
        $("#to-load").Loadingdotdotdot({
            "speed": 400,
            "maxDots": 4,
            "word": "Loading"
        });

        setTimeout(
            function () {
                $(".show-later").show();
                $("#return-link").attr('href', '/request?identity=true&address=' + keyPair.getAddress());
                $("#to-load").Loadingdotdotdot("Stop");
                $("#to-load").hide();
            }, 5000);

    });

});