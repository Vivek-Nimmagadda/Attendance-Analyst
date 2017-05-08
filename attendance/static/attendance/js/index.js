$(function() {
	$('#about-btn').bind('click',function(event){
		var $anchor = $(this);

		$('html, body').stop().animate({
			scrollTop: $($anchor.attr('href')).offset().top-50
		}, 1500, 'easeOutElastic');
		event.preventDefault();
	});
});


$("#about-btn").mouseover(function(){
	$(this).addClass("change").delay(500);
});

$("#about-btn").mouseleave(function(){
	$(this).removeClass("change").delay(500);
});
