$(document).ready(function(){
  var resize = new Array('p','html');
  resize = resize.join(',');
  
  //resets the font size when "reset" is clicked
  /*
  var resetFont = $(resize).css('font-size');
    $(".reset").click(function(){
      $(resize).css('font-size', resetFont);
    });
  */
  //increases font size when "+" is clicked
  $(".btnsize").click(function(){
    /*
    var originalFontSize = $(resize).css('font-size');
    var originalFontNumber = parseFloat(originalFontSize, 10);
    var newFontSize = originalFontNumber*1.2;
    */
    //$(resize).css('font-size', newFontSize);
    $(resize).css('font-size', "200%");
    return false;
  });
  
});







/*
//var flip = 1;
(function($) {
  function changeFont(fontSize) {
    return function() {
      $('html').css('font-size', fontSize + '%');
    }
  }
  var normalFont = changeFont(100),
  mediumFont = changeFont(200);


  $('.btn-size').on('click', function(){
    normalFont();
    /*
    if (flip = 1){
      changeFont(200);
      flip = 0;
    }
    else {
      changeFont(50);
      flip = 1;
    }
    */
//  });

//})
*/