function start() {
	$("#sub-btn").fadeTo(0, 0.70);
	$("#sub-btn").hover(function() {
		$(this).fadeTo(100, 1);
	}, function() {
		$(this).fadeTo(100, 0.70);
	});
}

$(document).ready(start);