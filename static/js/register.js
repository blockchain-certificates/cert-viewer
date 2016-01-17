function scrollAndShow(){
  $("#next-btn").hide();
  $("#shipping-info").show();
  $('html, body').animate({
    scrollTop: $("#shipping-info").offset().top - 100
  }, 'slow');
}

function validateFirstForm(){
  var isValid = true;
  $('.errors').remove();
  $('.first-group').each(function(){
    if( ($(this).find("input").val()==='' && $(this).find("input").attr("id")!="comments") || ($(this).find(".radio-input").length > 0 && $(this).find(".radio-input").is(':checked') == false)){
      if($(this).is("span")==true && $(this).next().hasClass("errors")==false){
        $('<p class="font-light errors radio-error">Please select one.</p>').insertAfter(this);
      } else if ($(this).next().hasClass("errors")==false){
        $('<p class="font-light errors">This field is required.</p>').insertAfter(this);
      }
      isValid = false;
    }
  });
  return isValid;
}

$(document).ready(function() {
  var flag = false;

  if($(".errors").length > 0){
    $("#shipping-info").show();
    $("#next-btn").hide();
    flag=true;
  }

  if(flag == false){
    $("#next-btn").click(function(){
      console.log(validateFirstForm())
      if(validateFirstForm() == true){
        scrollAndShow();
        flag = true;
      }
    })
  }

});