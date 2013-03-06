// Tracking code

function trackAdWordsConversion(f, b, e) {
    var c = new Image();
    var g = location.protocol + "//www.googleadservices.com/pagead/conversion/" + f + "/?";
    var d = document.getElementsByTagName("script")[0];
    c.height = "1";
    c.width = "1";
    c.display = "none";
    c.style.borderStyle = "none";
    c.alt = "";
    if (e > 0) {
        g += "value=" + e + "&";
    }
    g += "label=" + b + "&guid=ON&script=0";
    g += "&url=" + encodeURIComponent(location.href);
    c.src = g;
    d.parentNode.insertBefore(c, d);
}

function getParameterByName(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

function getInputByName(name) {
  var inputName = "input[name="+name+"]"
  return $(inputName).val();
}

function customGATracker() {
    var url = location.pathname + location.search, promoCode, firstLogin, omniCode;
    if(typeof getParameterByName == "function"){
        promoCode = getParameterByName("promo_code");
        firstLogin = getParameterByName("confirm_signup");
        omniCode = getParameterByName("sc_cid");
    }
    _gaq.push(['_setAccount', 'UA-30752912-1']);
    _gaq.push(['_setDomainName', 'redhat.com']);
    _gaq.push(['_setCustomVar', 3 ,'Omni', omniCode , 1]);
    _gaq.push(['_setSiteSpeedSampleRate', 10]);

    if(/app\/account\/complete/.test(url) && typeof trackAdWordsConversion == "function"){
        trackAdWordsConversion('1007064360', '3qfsCMjw0gIQqKqa4AM');
    }
    if(/app\/account/.test(url)){
      if(typeof getInputByName == "function"){
        // We're using the inputs here because we are mixing GET and POST pages
        captchaType = getInputByName('captcha_type');
        captchaStatus = getInputByName('captcha_status');
      }
      if(captchaType && captchaStatus){
        _gaq.push(['_trackEvent','Captcha',captchaType,captchaStatus]);
      }
    }
    if(/community\/pricing/.test(url)){
      _gaq.push(['_setCustomVar', 4 ,'Viewed Pricing Page', 'Viewed Page', 1]);
    }
    if(/community\/open-source\/download-origin/.test(url)){
      try{
        $('.action-call').live('click',function(e){
          var url = $(this).attr("href");
          category = 'Downloads';
          _gat._getTrackerByName()._trackEvent(category, 'Origin', url, 0);
          e.preventDefault();
          setTimeout('document.location = "' + url + '"', 250);  
        });
      }catch(err){}
    }
    if(firstLogin && firstLogin == "true"){
      _gaq.push(['_setCampaignTrack', false]);
    }
    if(/prev_login=true/.test(document.cookie)){
      _gaq.push(['_setCustomVar', 1 ,'User Type', 'Previous Login', 1]);
    } else{
      _gaq.push(['_setCustomVar', 1 ,'User Type', 'No Login', 1]);
    }
    if(promoCode && promoCode != ""){
      _gaq.push(['_setCustomVar', 2 ,'Promo Code', promoCode , 3]);
    }
    if (/\/search\/node\//.test(url)){
      var newurl = url.replace("/node/", "?node=");
      _gaq.push(['_trackPageview', newurl]);
    }
    else{
      _gaq.push(['_trackPageview']);
    }
}

var _gaq = _gaq || [];
if (typeof customGATracker == "function"){
  customGATracker();
}

(function () {
  var ga = document.createElement('script');
  ga.type = 'text/javascript';
  ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(ga, s);
})();

//KissInsights
try{
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
}catch(err){}
