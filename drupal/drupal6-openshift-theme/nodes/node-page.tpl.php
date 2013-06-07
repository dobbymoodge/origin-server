<?php if (!$status) { ?><div class="node-unpublished"><?php } ?>

  <?php if ($submitted): ?>
    <span class="submitted"><?php print $submitted; ?></span>
  <?php endif; ?>

  <?php print $content ?>

  <!-- <?php if ($taxonomy): ?>
    <div class="terms-page">Tags: <?php print $terms ?></div>
  <?php endif;?>

  <?php if ($links): ?>
    <div class="links"><?php print $links; ?></div>
  <?php endif; ?> -->

  <?php if ($node->taxonomy && !empty($node->taxonomy)): ?>
    <div class="terms terms-page">Tags: <?php foreach($node->taxonomy as $term) { ?>
      <a href="/tags/<?php print $term->name; ?>"><?php print $term->name; ?></a> 
    <?php }?></div>
  <?php endif;?>

<?php if (!$status) { ?></div><?php } ?>
