function start() {
	$("#menu li a").hover(function() {
		$(this).animate("fast", 1);
	}, function() {
		$(this).animate("fast", 0.70);
	});

$(document).ready(start);