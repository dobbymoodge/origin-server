<?php 
  $block = module_invoke('block', 'block', 'view', '4'); 
  $messaging = $block['content'];

?><?php include 'page_header.inc' ?>

<header>
  <?php include 'page_top.inc' ?>
  <?php include 'page_nav.inc' ?>
</header>

<div id="home" class="">
  <div class="container">
    <?php $block = module_invoke('block', 'block', 'view', '6'); print $block['content']; ?>

    <div id="buzz" class="section-base">
      <div class="container">
        <div class="row row-buzz">
          <div class="span12">
            <div class="column-buzz">
              <h2>
                What others are saying
              </h2>
              <hr>
              <div class="row-fluid">
                <div id="buzz-testimonials" class="span5"><?php $block = module_invoke('block', 'block', 'view', '3'); print $block['content']; ?></div>
                <div class="span1">&nbsp;</div>
                <div id="buzz-retweets" class="span6"><?php print _redhat_frontpage_load_retweets(); ?></div>
              </div>

              <div class="row-fluid buzz-actions">
                <div class="span6"><a class="link-with-action" href="/products#why-openshift"><strong>Why</strong> OpenShift?</a></div>
                <div class="span6">
                  <div class="align-right"><a class="link-with-action" href="http://www.twitter.com/#!/openshift"><strong>Follow</strong> OpenShift</a></div>
                  <div class="align-right"><a class="link-with-action" href="http://twitter.com/#!/search/%23OpenShift"><strong>More</strong> #OpenShift buzz</a></div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<script type="text/javascript">
  $.fn.setAllToMaxHeight = function(){
    return this.height( Math.max.apply(this, $.map( this , function(e){ return $(e).height() }) ) );
  }
  $(document).ready(function() {
    var wide = $(window).width() > 767;
    var products = $('li', '#products');
    products.on('mouseover', function() {
      if (!wide) { return; }
      products.removeClass('active');
      $(this).addClass('active');
    });
    if (!wide) {
      products.addClass('active');
    }

    var productDescriptions = $('#products li p');
    productDescriptions.setAllToMaxHeight();
    $(window).resize(function() {
      if (wide = $(window).width() > 767) {
        products.removeClass('active');
      } else {
        products.addClass('active');
      }
      productDescriptions.css('height', 'auto');
      productDescriptions.setAllToMaxHeight();
    });

    var $window = $(window);
    if ($window.width() > 800) {
      var $home = $('body.home2 #home');
      var cometW = 822, 
          cometH = 576, 
          slope  = -2.8;
      var windowW, windowH, 
          centerX, centerY, 
          homeTop, buzzTop, 
          intersectY;
      var calcIntersection = function() {
        windowW = $window.width();
        windowH = $window.height();

        homeTop = parseInt($home.offset().top);
        buzzTop = parseInt($('#buzz').offset().top);
        
        // intersect the center of the comet with the top of the buzz section
        intersectY = buzzTop - (cometH/2);

        // background-position coordinates to center the comet at the top of the screen
        centerX = parseInt((windowW-cometW)/2);
        centerY = 0;
      };
      var moveComet = function() {
        var scrollTop = $window.scrollTop();

        // Y offset to keep background vertically stationary while scrolling
        var offsetY = scrollTop - homeTop;

        // Compute X, given slope and intersect
        var x = centerX + (scrollTop-intersectY)*slope;
        if (x > windowW)
          x = windowW;
        else if (x < -cometW)
          x = -cometW;

        $home.css('background-position', x + "px " + (centerY + offsetY) + "px");
      };
      var calcAndMove = function() {
        calcIntersection();
        moveComet();
      };

      $(window).scroll(moveComet);
      $(window).resize(calcAndMove);
      calcAndMove();
    }
  });
</script>
<?php include 'page_footer.inc' ?>