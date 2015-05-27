function start() {
	$("#blok").hover(function() {
		$(this).fadeTo("fast", 0.50);
	}, function() {
		$(this).fadeTo("fast", 1);
	});
}

$(document).ready(start);
