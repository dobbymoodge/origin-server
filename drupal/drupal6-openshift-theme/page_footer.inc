    <footer>
      <div id="footer-nav">
        <div class="container">
          <?php if ($footer){ print $footer; } ?>
          <?php
            $menu = menu_tree_page_data('menu-top-footer-menu');
            if ($menu) {
              print openshift_flat_menu_tree_output($menu);
            }
          ?>
        </div>
      </div>
      <section id="copyright">
        <div class="container">
          <a href="https://www.redhat.com/">
            <img src="<?php print openshift_assets_url(); ?>/redhat.png" alt="Red Hat">
          </a>
          <div class="pull-right"><?php print $footer_message; ?></div>
        </div>
      </section>
    </footer>
	<!-- Begin Eloqua Tracking -->
	<script type='text/javascript' src='https://www.redhat.com/j/elqNow/elqCfg.js'></script> 
	<script type='text/javascript' src='https://www.redhat.com/j/elqNow/elqImg.js'></script>
	<!-- End Eloqua Tracking -->
	<!-- Begin Google Analytics Tracking -->
	<script type="text/javascript" src="<?php print openshift_assets_url(); ?>/site/tracking.js"></script>
	<!-- End Google Analytics Tracking -->
    <!-- SiteCatalyst code version: H.23.3.
    Copyright 1996-2011 Adobe, Inc. All Rights Reserved
    More info available at http://www.omniture.com -->
    <div id="oTags">
    <script type="text/javascript" src="<?php print openshift_assets_url(); ?>/site/s_code.js"></script>
    <script language="JavaScript" type="text/javascript"><!--
    /* You may give each page an identifying name, server, and channel on
    the next lines. */
    s.pageName="openshift | community | <?php print $head_title; ?>"
    s.server=""
    s.channel="<?php if($product): ?>OpenShift | Product | <?php print $product; ?><?php endif; ?>"
    s.heir1=""
    s.pageType=""
    s.prop1=""
    s.prop2=""
    s.prop3=""
    s.prop4=""
    s.prop5=""
    /* Conversion Variables */
    s.campaign=""
    s.state=""
    s.zip=""
    s.events=""
    s.products=""
    s.purchaseID=""
    s.eVar1=""
    s.eVar2=""
    s.eVar3=""
    s.eVar4=""
    s.eVar5=""
    s.eVar51="<?php if($product): ?><?php print $product; ?><?php endif; ?>"
    s.eVar27=""
    s.eVar28=""
    s.eVar29=""
    /************* DO NOT ALTER ANYTHING BELOW THIS LINE ! **************/
    var s_code=s.t();if(s_code)document.write(s_code)//--></script>
    <script language="JavaScript" type="text/javascript"><!--
    if(navigator.appVersion.indexOf('MSIE')>=0)document.write(unescape('%3C')+'\!-'+'-')
    //--></script><noscript><img src="http://redhat.122.2o7.net/b/ss/redhatopenshift/1/H.23.3--NS/0"
    height="1" width="1" border="0" alt="" /></noscript><!--/DO NOT REMOVE/-->
    <!-- End SiteCatalyst code version: H.23.3. -->
    </div>
	
	<!-- Google Code for Remarketing tag -->
	<script type="text/javascript">
	/* <![CDATA[ */
	var google_conversion_id = 1007064360;
	var google_conversion_label = "amNWCJipqAQQqKqa4AM";
	var google_custom_params = window.google_tag_params;
	var google_remarketing_only = true;
	/* ]]> */
	</script>
	<script type="text/javascript" src="//www.googleadservices.com/pagead/conversion.js">
	</script>
	<noscript>
	<div style="display:inline;">
	<img height="1" width="1" style="border-style:none;" alt="" src="//googleads.g.doubleclick.net/pagead/viewthroughconversion/1007064360/?value=0&amp;label=amNWCJipqAQQqKqa4AM&amp;guid=ON&amp;script=0"/>
	</div>
	</noscript>
    
	<div style="display:none;"> <?php # FIXME remove after sprint 10 ?>
    <script src="<?php print $openshift_server_url; ?>/app/status/status.js?id=outage" type="text/javascript"></script>
    </div>
  </body>
<?php print $closure; ?>
</script>
</html>
