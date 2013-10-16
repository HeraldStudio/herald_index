	
var h;
h=100;
$(document).ready(function(){
	$(window).scroll(function(){
	var top=$(window).scrollTop();
	

	if(top>488){
		$('#nav').addClass('fixed');
        h=50;		
	}
	else{
		$('#nav').removeClass('fixed');	
        h=100;		
	}
	});


	var nav_switch=1;
	$('#nav_redian').click(function(){
		if(nav_switch){
		nav_switch=0;
		$("html,body").animate({scrollTop: ($("#redian").offset().top) - h}, 1000,function(){
			nav_switch=1;
		});
		}
		return false;
	});
	$('#nav_huodong').click(function(){
		if(nav_switch){
		nav_switch=0;
		$("html,body").animate({scrollTop: ($("#huodong").offset().top) -h}, 1000,function(){
			nav_switch=1;
		});
		}
		return false;
	});
	$('#nav_ershou').click(function(){
		if(nav_switch){
		nav_switch=0;
		$("html,body").animate({scrollTop: ($("#ershou").offset().top) -h}, 1000,function(){
			nav_switch=1;
		});
		}
		return false;
	});
	$('#nav_shiwu').click(function(){
		if(nav_switch){
		nav_switch=0;
		$("html,body").animate({scrollTop: ($("#shiwu").offset().top) - h}, 1000,function(){
			nav_switch=1;
		});
		}
		return false;
	});

    });
	
	
	
