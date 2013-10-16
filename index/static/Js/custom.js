
$(document).scroll(function(){
    var navFixedTopHeight=$('#topNav').height()+$('#wrapper').height();
    if($(window).scrollTop() >= navFixedTopHeight ){
        $("#subNavFixed").css("display", "block");
        $("#subNav").css("visibility", "hidden");
    }
    else {
        $("#subNav").css("visibility", "visible");
        $("#subNavFixed").css("display", "none");
    };
});
