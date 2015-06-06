function start() {
	$("#sub-btn").fadeTo(0, 0.70);
	$("#sub-btn").hover(function() {
		$(this).fadeTo("fast", 1);
	}, function() {
		$(this).fadeTo("fast", 0.70);
	});
	
	$(".pass-sub-btn").fadeTo(0, 0.70);
	$(".pass-sub-btn").hover(function() {
		$(this).fadeTo("fast", 1);
	}, function() {
		$(this).fadeTo("fast", 0.70);
	});
}

$(document).ready(start);