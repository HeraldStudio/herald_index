	
var h,t;
t=52;
h=53330;
//var markTop=true;
$(document).ready(function(){
	$(window).scroll(function(){
	var top=$(window).scrollTop();

	if(top>460){
		markTop=false;
		$('#nav').addClass('fixed');
		$('#information').addClass('martop');
		//$('#nav').addClass('col-lg-12 col-md-12 col-sm-12');
		$('#nav').removeClass('row');
        h=50;		
	}
	else{
		markTop=true;
		$('#nav').removeClass('fixed');	
		$('#nav').addClass('row');
		$('#information').removeClass('martop');
        h=100;		
	}
	});


	var nav_switch=1;
	$('#nav_redian').click(function(){
		if(nav_switch){
		nav_switch=0;
			$("html,body").animate({scrollTop: ($("#redian").offset().top)-t}, 1000,function(){
				nav_switch=1;
			});
		}
		return false;
	});
	$('#nav_huodong').click(function(){
		if(nav_switch){
		nav_switch=0;
			$("html,body").animate({scrollTop: ($("#huodong").offset().top)-t}, 1000,function(){
				nav_switch=1;
			});
		}
		return false;
	});
	$('#nav_baike').click(function(){
		if(nav_switch){
		nav_switch=0;
			$("html,body").animate({scrollTop: ($("#baike").offset().top)-t}, 1000,function(){
				nav_switch=1;
			});
		}
		return false;
	});
	$('#nav_shiwu').click(function(){
	   alert("期待开发中...")
	//	if(nav_switch){
	//	nav_switch=0;
	//	$("html,body").animate({scrollTop: ($("#shiwu").offset().top) - h}, 1000,function(){
	//		nav_switch=1;
	//	});
	//	}
	//	return false;
	});

    });
	
	
	
