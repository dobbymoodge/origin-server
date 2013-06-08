// Tracking code
var _gaq = _gaq || [];

(function() {
	
	var getParameterByName = function(name) {
		name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
		var regexS = "[\\?&]" + name + "=([^&#]*)";
		var regex = new RegExp(regexS);
		var results = regex.exec(window.location.search);
		if(results === null) {
			return "";
		} else {
			return decodeURIComponent(results[1].replace(/\+/g, " "));
		}
	};

	var getInputByName = function(name) {
		var inputName = "input[name="+name+"]";
		return $(inputName).val();
	};
	
	var setMongoRef = function() {
		function getCookie(c_name) {
			var c_value = document.cookie;
			var c_start = c_value.indexOf(" " + c_name + "=");
			if (c_start === -1) {
				c_start = c_value.indexOf(c_name + "=");
			}
			if (c_start === -1) {
				c_value = null;
			} else {
				c_start = c_value.indexOf("=", c_start) + 1;
				var c_end = c_value.indexOf(";", c_start);
				if (c_end === -1) {
					c_end = c_value.length;
				}
				c_value = unescape(c_value.substring(c_start, c_end));
			}
			return c_value;
		}

		function getFormattedDate(timestamp) {
			var b = new Date(timestamp);
			var d = b.getFullYear().toString();
			var c = (b.getMonth() + 1).toString();
			var a = b.getDate().toString();
			return d + '-' + (c.charAt(1) ? c : "0" + c.charAt(0)) + '-' + (a.charAt(1) ? a : "0" + a.charAt(0));
		}

		var first_visit = getFormattedDate((new Date()).getTime());
		var source = 'direct';
		var medium = 'none';
		var term = 'not set';
		var utma = getCookie('__utma');
		var utmz = getCookie('__utmz');

		if(utma) {
			utma = utma.split('.');
			first_visit = getFormattedDate(utma[2]*1000);
		}

		if(utmz) {
			utmz = utmz.match(/[0-9.]+(.*)/i)[1];
			utmgclid = utmz.match(/utmgclid=(.*?)(?:$|\|)/i);
			if(utmgclid) {
				source = 'google';
				medium = 'cpc';
			} else {
				utmcsr = utmz.match(/utmcsr=(.*?)(?:$|\|)/i);
				source = utmcsr[1].replace(/\(|\)/g, "").substring(0,128);

				utmcmd = utmz.match(/utmcmd=(.*?)(?:$|\|)/i);
				medium = utmcmd[1].replace(/\(|\)/g, "").substring(0,128);
			}
			utmctr = utmz.match(/utmctr=(.*?)(?:$|\|)/i);
			if(utmctr) {
    			term = utmctr[1].replace(/\(|\)/g, "").substring(0,128);
			}		
		}

		var hiddenInput = document.createElement("input");
		hiddenInput.name = 'source';
		hiddenInput.type = 'hidden';
		hiddenInput.value = 'first_visit='+first_visit +'|'+ 'source='+source +'|'+ 'medium='+medium +'|'+ 'term='+term;
		$('#new_user_form').append(hiddenInput);
	};

	var promoCode = getParameterByName("promo_code");
	var firstLogin = getParameterByName("confirm_signup");
	var omniCode = getParameterByName("sc_cid");
	
	// Google Analytics tracking configuration
	_gaq.push(['_require', 'inpage_linkid', '//www.google-analytics.com/plugins/ga/inpage_linkid.js']);
	
	if(/openshift\.com$/.test(location.hostname) || /^\/(app\/)?account\/(new|complete)/.test(location.pathname)) {
		_gaq.push(['_setAccount', 'UA-30752912-5']); // drupal account
		_gaq.push(function(){
			$("a[href*='openshift.redhat.com']").on('click', function(event){
				event.preventDefault();
				var url = $(this).attr("href");
				_gaq.push(['_link', url]);
			});
		});	
	} else {
		_gaq.push(['_setAccount', 'UA-30752912-6']); // app account
	}
	
	if(/redhat\.com/.test(location.hostname)) {
		_gaq.push(['_setDomainName', 'redhat.com']);
	} else {
		_gaq.push(['_setDomainName', 'openshift.com']);
	}
	
	_gaq.push(['_setAllowLinker', true]);
	_gaq.push(['_addIgnoredRef', 'openshift.com']);
	_gaq.push(['_addIgnoredRef', 'www.openshift.com']);
	_gaq.push(['_addIgnoredRef', 'openshift.redhat.com']);
	_gaq.push(['_setCustomVar', 3, 'Omni', omniCode, 1]);
	_gaq.push(['_setSiteSpeedSampleRate', 10]);

	// Track captcha usage
	if(/^\/(app\/)?account/.test(location.pathname)) {
		// We're using the inputs here because we are mixing GET and POST pages
		var captchaType = getInputByName('captcha_type');
		var captchaStatus = getInputByName('captcha_status');
		
		if(captchaType && captchaStatus) {
			_gaq.push(['_trackEvent', 'Captcha', captchaType, captchaStatus]);
		}
	}
	
	// Viewed pricing page
	if(/^\/pricing/.test(location.pathname)) {
		_gaq.push(['_setCustomVar', 4, 'Viewed Pricing Page', 'Viewed Page', 1]);
	}
	
	// Track origin downloads
	if(/^\/open-source\/download-origin/.test(location.pathname)) {
		_gaq.push(function(){
			$('.action-call').on('click', function(event){
				event.preventDefault();
				var url = $(this).attr("href");
				_gaq.push(['_trackEvent', 'Downloads', 'Origin', url]);
				setTimeout('document.location = "' + url + '"', 300);
			});
		});
	}
	
	// Disable campaign tracking for users returning from email validation
	if(firstLogin && firstLogin == "true") {
		_gaq.push(['_setCampaignTrack', false]);
	}
	
	// Send promo code info to GA as events
	if(promoCode && promoCode != "") {
		_gaq.push(['_trackEvent', 'Promo Code', 'Evangelist Event', promoCode]);
	}
	
	// Enterprise form links
	_gaq.push(function(){
		$('a[href*="engage.redhat.com"],a[href*="inexpo.com"]').on("click", function(event){
			event.preventDefault();

			var url = $(this).attr("href");
			_gaq.push(['_trackEvent', 'Outbound Links', 'OpenShift Enterprise', url]);

			var pixel = new Image;
			var pixel_src = '//www.googleadservices.com/pagead/conversion/997127018/?value=0&amp;label=SomnCJaDrwQQ6ua72wM&amp;guid=ON';
			pixel_src += "&amp;url=" + url.substring(0, 256);
			pixel.src = pixel_src;
			pixel.onload = function() {};

			setTimeout('document.location = "' + url + '"', 300);  
		});
	});
	
	// PDF Tracking
	_gaq.push(function(){
		$("a[href*='.pdf']").on("click", function(event){
			event.preventDefault();
			var url = $(this).attr("href");
			_gaq.push(['_trackEvent', 'Downloads', 'PDF Whitepaper', url]);
			setTimeout('document.location = "' + url + '"', 300);  
		});
	});
	
	// Site search tracking
	if (/\/search\/node\//.test(location.href)) {
		var newurl = location.href.replace("/node/", "?node=");
		_gaq.push(['_trackPageview', newurl]);
	} else {
		_gaq.push(['_trackPageview']);
	}
	if (/\/app\/account\/new/.test(location.href)) {
		_gaq.push(setMongoRef);
	}
})();

(function () {
	var ga = document.createElement('script');
	ga.type = 'text/javascript';
	ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(ga, s);
})();

// KissInsights
try {
	if(!(navigator.userAgent.match(/iphone|android/i))){
		var _kiq = _kiq || [];

		(function () {
			var ki = document.createElement('script');
			ki.type = 'text/javascript';
			ki.async = true;
			ki.src = '//s3.amazonaws.com/ki.js/35352/7LV.js';
			var s = document.getElementsByTagName('script')[0];
			s.parentNode.insertBefore(ki, s);
		})();
	}
} catch(err){}
