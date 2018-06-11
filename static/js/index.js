$(function(){

	// 返回页顶
	$('.bck-top').click(function(){
		$("html,body").animate({scrollTop:0},500);
	});


	// 弹出个人信息
	$('.photo').mouseover(function(){
		$('.pop').show()
	});


	$('.photo').mouseout(function(){
		var t=setTimeout(hM,50);
		$('.pop').mouseover(function(){
			clearTimeout(t)
		})
	});
	$('.pop').mouseout(function(){
		var t=setTimeout(hM,50);
		$('.pop').mouseover(function(){
			clearTimeout(t)
		})
	});
		
	function hM(){
		$('.pop').hide()
	}
	
	// 开关灯
	$('#light').click(function(){
		if($('.navbar').css('display')=='none'){
  			$('.navbar').show();
			$('.bottom').show();
			$('body').css('background-color','#fff')
 		}else{
 			$('.navbar').hide();
			$('.bottom').hide();
			$('body').css('background-color','#1c1c1d')  
		}		
	});

	// 首页右侧导航
	$(window).scroll(function(){
	var scr = $(window).scrollTop();
	var menuTop = 650-scr;
	if(scr<450){
		$('.menu').css({
			'top':menuTop
		})
	}
	else{
		$('.menu').css({
			'top':'200px'
		})
	}
	})

	// 表单验证
	$('#form').submit(function(){
		if ($('#username').val()=='') {
			$('.usermsg').show();
			return false;
		}else{$('.usermsg').hide()}
		if ($('#pwd').val()=='') {
			$('.pwdmsg').show();
			return false;
		}else{$('.pwdmsg').hide()}
		if ($('#id_captcha_1').val()=='') {
			$('.captchamsg').show();
			return false;
		}else{$('.captchamsg').hide()}
		if ($('#pwd1').val()=='') {
			$('.pwd1msg').show();
			return false;
		}else{$('.pwd1msg').hide()}
		if ($('#pwd2').val()=='') {
			$('.pwd2msg').show().text('密码不能为空');
			return false;
		}else{$('.pwd2msg').hide()}
		if ($('#pwd1').val()!=$('#pwd2').val()){
			$('.pwd2msg').text('两次密码输入不一致').show();
			return false
		}
	});

	//	弹出富文本编辑框
	$('.addcomment').click(function(){
		$('.mask,.comment-form').show()
	});
	$('#exit').click(function(){
		$('.mask,.comment-form').hide()
	});

});

