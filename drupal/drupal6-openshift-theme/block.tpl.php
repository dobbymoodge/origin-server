<div id="block-<?php print $block->module .'-'. $block->delta; ?>" class="block <?php print $block_classes; ?> block-<?php print $block->module ?>">
<?php if ($block->subject): ?>
  <h3><?php print $block->subject ?></h3>
<?php endif;?>

  <div class="content">
    <?php print $block->content ?>
  </div>
</div>
