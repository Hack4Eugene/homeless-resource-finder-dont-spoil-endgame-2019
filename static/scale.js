var flip = 1; //variable that keeps track of if font has been enlarged

$(document).ready(function(){
  var resize = new Array('p','html');
  resize = resize.join(',');

  $(".btnsize").click(function(){
    if (flip == 1) {
      $(resize).css('font-size', "200%");
      flip = 0;
    }
    else {
      $(resize).css('font-size', "100%");
      flip = 1;
    }
    return false;
  });
  
});
