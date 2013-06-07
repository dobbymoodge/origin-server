<?php

/**
 * @file
 * OpenShift Partner Self Service Portal template.
 */
?>
<div class="partner-portal">
  <div id='portal-welcome'><h2 class="alert alert-error" style="display: inline-block;"><?php print (t('Welcome')); ?> <?php print ($partner_level['partner_level']); ?></h2></div>
  <div><h2><?php print (t('Get Started Now!')); ?></h2></div>
  <section>
    <div class="row-fluid">
      <div class="span6">
        <a class="tile tile-click tile-compact" href="/partner/portal/company-info">
          <div style="transform: rotate(180deg); display: inline-block; margin-left: -4px; padding-left: 10px;" class="icon-download-alt font-icon-size-34 pull-left"></div>
          <h3>Upload: Company Information</h3>
        </a>
      </div>
      <div class="span6">
        <a href="<?php print (($partner_level['partner_level'] == 'Ready Partner') ? 'https://www.openshift.com/sites/default/files/file_downloads/OpenShiftReadyPartnerLogoFiles.zip' : 'https://www.openshift.com/sites/default/files/file_downloads/OpenShiftAdvancedPartnerLogoFiles.zip'); ?>" class="tile tile-click tile-compact">
          <span class="icon-download-alt font-icon-size-34 pull-left"></span>
          <h3>Download: OpenShift by Red Hat Partner Logo</h3>
        </a>
      </div>
    </div>
  </section>
  <div class="row-fluid">
    <div class="span6" style="margin-bottom: 35.875px">
      <h2><?php print (t('Marketing Assets')); ?></h2>
      <a href="https://www.openshift.com/sites/default/files/file_downloads/RH_Openshift_Enterprise_PaaS_WP_10204147_1112_dc_web.pdf" class="tile tile-click tile-compact">
        <span class="icon-list-ol font-icon-size-34 pull-left"></span>
        <h3>The Road to Enterprise PaaS</h3>
      </a>
      <a href="/partner/portal/blog-content" class="tile tile-click tile-compact">
        <span class="icon-code font-icon-size-34 pull-left"></span>
        <h3>Blog Content</h3>
      </a>
      <a href="/partner/portal/social-media-posts" class="tile tile-click tile-compact">
        <span class="icon-bubbles font-icon-size-34 pull-left"></span>
        <h3>Social Media Posts</h3>
      </a>
    </div>
    <div class="span6"  style="margin-bottom: 35.875px">
      <h2><?php print (t('Manage Your Partnership')); ?></h2>
      <a href="/partner/portal/customer-story" class="tile tile-click tile-compact">
        <span class="icon-star-empty font-icon-size-34 pull-left"></span>
        <h3>Submit a Customer Success Story</h3>
      </a>
      <?php if ($partner_level['partner_level'] == 'Ready Partner'): ?>
        <a href="/partner/portal/upgrade" class="tile tile-click tile-compact">
          <span class="font-icon-block font-icon-size-34 pull-left"> 
            <span aria-hidden="true" class="font-icon icon-scalable-part1"></span>
            <span aria-hidden="true" class="font-icon icon-scalable-part2 font-icon-grey"></span>
          </span>
          <h3>Request to Upgrade Partner Level</h3>
        </a>
      <?php endif; ?>  
      <a href="/partner/portal/request-assistance" class="tile tile-click tile-compact">
        <span class="icon-question-sign font-icon-size-34 pull-left"></span>
        <h3>Request Assistance / Materials</h3>
      </a>
    </div>
  </div>

  <section>
    <?php print (t('Questions? Email ') . l(t('openshift-partners@redhat.com'), 'mailto:openshift-partners@redhat.com')); ?>
  </section>
</div>
