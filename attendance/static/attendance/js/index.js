$(function() {
	$('#about-btn').bind('click',function(event){
		var $anchor = $(this);

		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top-50
		}, 2000, 'easeOutElastic');
		event.preventDefault();
	});

	var amountScrolled = 300;

	$(window).scroll(function() {
		if ( $(window).scrollTop() > amountScrolled ) {
			$('.back-to-top').fadeIn('fast');
		} else {
			$('.back-to-top').fadeOut('fast');
		}
	});

	$('#up-btn').click(function() {
	$('html, body').animate({
		scrollTop: 0
	}, 1500, 'easeInOutExpo');
	return false;
});

});


$(".link-btn").mouseover(function(){
	$(this).addClass("change").delay(500);
});

$(".link-btn").mouseleave(function(){
	$(this).removeClass("change").delay(500);
});
