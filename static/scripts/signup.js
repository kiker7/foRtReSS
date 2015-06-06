function start() {
	$("#signup-btn").fadeTo(0, 0.70);
	$("#signup-btn").hover(function() {
		$(this).fadeTo("fast", 1);
	}, function() {
		$(this).fadeTo("fast", 0.70);
	});
}

$(document).ready(start);