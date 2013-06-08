<div id="node-<?php print $node->nid; ?>" class="<?php print $node->type; ?> node<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?>">

  <div class="content clearfix">
    <?php print $content ?>
  </div>

  <?php if ($submitted): ?>
    <span class="submitted"><?php print $submitted; ?></span>
  <?php endif; ?>

  <?php if ($taxonomy): ?>
    <div class="terms">Tags: <?php print $terms ?></div>
  <?php endif;?>

  <?php if ($links): ?>
    <div class="links"><?php print $links; ?></div>
  <?php endif; ?>
</div>
