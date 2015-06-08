function getEntropy(chars, passwordLength) {
	var charsLength = chars.length;
	var entropyPerChar = Math.log(charsLength) / Math.log(2);
	var entropy = passwordLength * entropyPerChar;
	return entropy;
}

function start() {
	$("#signup-btn").fadeTo(0, 0.70);
	$("#signup-btn").hover(function() {
		$(this).fadeTo(100, 1);
	}, function() {
		$(this).fadeTo(100, 0.70);
	});

	$("#password-fld")
			.keypress(
					function() {
						var pass = document.getElementById('password-fld').value;

						var lower = false;
						var upper = false;
						var digits = false;
						var special = false;

						if (/[a-z]/.test(pass))
							lower = true;
						if (/[A-Z]/.test(pass))
							upper = true;
						if (/[0-9]/.test(pass))
							digits = true;

						tab = new String();
						if (lower == true)
							tab += "abcdefghijklmnopqrstuvwxyz";
						if (upper == true)
							tab += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
						if (digits == true)
							tab += "0123456789";

						var value = getEntropy(tab, pass.length);

						var strip = document.getElementById('strengh');
						strip.innerHTML = "";
						var str1 = document.createElement("div");
						str1
								.setAttribute(
										"style",
										"background-color: #ff0000; width:60px; height: 10px; float:left; margin-left: 2px; margin-right: 2px; margin-top:10px");
						var str2 = document.createElement("div");
						str2
								.setAttribute(
										"style",
										"background-color: #ff4f00; width:60px; height: 10px; float:left; margin-left: 2px; margin-right: 2px; margin-top:10px");
						var str3 = document.createElement("div");
						str3
								.setAttribute(
										"style",
										"background-color: #fff900; width:60px; height: 10px; float:left; margin-left: 2px; margin-right: 2px; margin-top:10px");
						var str4 = document.createElement("div");
						str4
								.setAttribute(
										"style",
										"background-color: #a3ff00; width:60px; height: 10px; float:left; margin-left: 2px; margin-right: 2px; margin-top:10px");
						var str5 = document.createElement("div");
						str5
								.setAttribute(
										"style",
										"background-color: #00ff00; width:60px; height: 10px; float:left; margin-left: 2px; margin-right: 2px; margin-top:10px");

						if (isNaN(value)){
						} else if ( value < 15) {
							strip.appendChild(str1);
						} else if (value < 30) {
							strip.appendChild(str1);
							strip.appendChild(str2);
						} else if (value < 45) {
							strip.appendChild(str1);
							strip.appendChild(str2);
							strip.appendChild(str3);
						} else if (value < 60) {
							strip.appendChild(str1);
							strip.appendChild(str2);
							strip.appendChild(str3);
							strip.appendChild(str4);
						} else {
							strip.appendChild(str1);
							strip.appendChild(str2);
							strip.appendChild(str3);
							strip.appendChild(str4);
							strip.appendChild(str5);
						}

					});
}

$(document).ready(start);