function start() {
	$("#signin-btn").fadeTo(0, 0.70);
	$("#signin-btn").hover(function() {
		$(this).fadeTo("fast", 1);
	}, function() {
		$(this).fadeTo("fast", 0.70);
	});
}

$(document).ready(start);