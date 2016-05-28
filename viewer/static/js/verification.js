(function() {

  function renderResponse(i, len, data){
    setTimeout(function() {
      count = i+1;
      total = len-1;
      message = data[0];
      value = data[1];

      // not on last step
      if (i != len-1) {

        var messageTemplate = $("<li>Step " + count.toString() + " of " + total.toString() + "... " + message + "</li>");
        $("#progress-msg").append(messageTemplate);

        setTimeout(function() {
          messageTemplate.text(messageTemplate.text() + " [" + markMappings[value] + "]");
        }, 1000);

      } else { // on last one
        setTimeout(function() {
          if (value==true) {
            $("#progress-msg").append("<li>Success! The certificate has been verified.</li>");
            $("#verified").show();
          } else {
            $("#progress-msg").append("<li>Oops! The certificate could not be verified.</li>");
            $("#not-verified").show();
          }
        }, 1000)
      }
    }, timeDelay*i);
  }

  timeDelay = 2000;
  markMappings = {true: "PASS", false: "FAIL", "DONE": "DONE"}

  $(document).ready(function() {
    $( "#verify-button" ).click(function() {
      $("#not-verified, #verified").hide();

      $("#progress-msg").empty();

      var data = $(this).attr('value');

      $.get("/verify?"+data, function(res){
        res = JSON.parse(res);
        $("#progress-msg").show();

        if(res == null){
          $("#progress-msg").append("<li>Oops! There was an issue connecting to the Blockchain.info API</li>");
        } else {
          for (i=0; i<res.length; i++) {
            renderResponse(i, res.length, res[i])
          }
        }
      });
    });
  });


})();
