<?php include 'page_header.inc' ?>

    <header>
      <?php include 'page_top.inc' ?>
      <?php include 'page_nav.inc' ?>
    </header>

    <div id="content" class="section-striped">
      <div class="container"><div class="row-content">
      <div class='row row-flush-right'>
        <div class="column-navbar">       
          <a data-toggle="collapse" data-target=".nav-collapse" class="btn btn-navbar">
          <span class="pull-left">Navigate</span>
          <span class="pull-right">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          </span>
          </a>
        </div>

        <?php if ($content_header) :?><div class="column-navbar-secondary lift grid-wrapper"><div class="nav-collapse collapse"><?php print $content_header; ?></div></div><?php endif; ?>

        <?php if ($layout == 'left' || $layout == 'both') :?>
        <div class="column-nav lift-less grid-wrapper">
          <div class="nav-collapse collapse">
            <nav class="span3">
              <div class="gutter-right">
                <?php print $sidebar_left; ?>
              </div>
            </nav>
           </div>
          </div>
          <div class="column-content lift grid-wrapper">
            <div class="span9 span-flush-right">

        <?php else :?>
          <div class="column-content column-content-page lift grid-wrapper">
            <div class="span12 span-flush-right">
        <?php endif; ?>

          <?php if ($layout == 'right' || $layout == 'both') :?>
            <div class="span3 pull-right column-floating nav-collapse collapse">
              <?php print $sidebar_right; ?>
            </div>
          <?php endif; ?>
            <?php print $breadcrumb; ?>
          
            <?php if (!empty($heading)) {
                    if ($layout == 'left' || $layout == 'both') :?>
              <h1 class="ribbon"><?php print $heading; ?></h1>
              <?php else :?>
              <h1><?php print $heading; ?></h1>
            <?php endif; } ?>

            <?php if ($show_messages && $messages): print $messages; endif; ?>
            <?php if ($forum['new-topic'] == TRUE) :?>
            <div id="forum-header" class="forum-new-topic">
              <div class="forum-header-left">
                <h2>Post a New Thread</h2>
              </div>
            </div>
            <?php endif; ?>
    
            <?php print $content_prefix; ?>
            <?php print $content; ?>
            <?php openshift_wrap_region($content_suffix); ?>

            <?php if ($tabs) :?><?php print $tabs; ?><?php endif; ?>
         </div>

          </div>
        </div>
      </div>
      </div></div>
    </div>

<?php include 'page_footer.inc' ?>
