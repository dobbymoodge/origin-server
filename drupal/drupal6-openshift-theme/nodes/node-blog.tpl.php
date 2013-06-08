<article id="node-<?php print $node->nid; ?>" class="blog-post node<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?> node-blog">
  <div class="metadata"><span class="created"><?php print format_date($node->created, $type='custom', $format = 'F j, Y \a\t H:i A'); ?></span>
  <?php 
    $author_nid = $field_author[0]['nid'];
    print views_embed_view('author_profile_box', 'block_1', $author_nid);
  ?>
  </div>

  <div class="content clearfix">
    <?php print $content ?>
  </div>

  <?php if ($taxonomy): ?>
    <div class="terms">Tags: <?php print $terms ?></div>
  <?php endif;?>

  <?php if ($links): ?>
    <div class="links"><?php print $links; ?></div>
  <?php endif; ?>

  <?php print openshift_social_sharing($node_url, $title); ?>

</article>
