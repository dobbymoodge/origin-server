<?php
//echo '<pre>';
//print_r($node->uid);
//$user->uid;
//echo '</pre>';
$do = og_comment_perms_do();
?>
<div id="node-<?php print $node->nid; ?>" class="node node-og-group-post<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?>">
  <div class="thread-header">Feature Request</div>

  <?php if ($forum) { ?>
    <ul class="forum-navigation-links">
      <li><a href="<?php print base_path(); ?>forums"><?php print t('Main List of Forums'); ?></a></li>
      <li><a href="<?php print base_path(); ?>forums/<?php print $forum['id'] ?>"><?php print $forum['title']; ?></a></li>
    </ul><?php
  } ?>

  <h2><a href="<?php print $node_url ?>" title="<?php print $title ?>"><?php print $title ?></a></h2>
  
  <?php print theme('user_picture', $node); ?>

  <div class="meta">
  <?php if ($submitted): ?>
    <div class="submitted">
      <?php
      print 'Started by ' . theme('username', $node) . ' on ' . format_date($created, $type='custom', $format = 'F j, Y');
      ?>
    </div>
  <?php endif; ?>
  
  <?php print views_embed_view('user_profile_box', 'block_3', $node->uid); ?>

  <?php if ($terms): ?>
    <div class="terms terms-inline"><?php print $terms ?></div>
  <?php endif;?>
  </div>

  <div class="content">
    <?php if ($node->field_state[0]['value'] == 'Completed'): ?>
      <h3 class='implemented'>This feature has been implemented</h3>
      <br />
      <?php print $node->content['body']['#value'] ?>
    <?php else: print $content ?>
    <?php endif; ?>
  </div>
  
  
  <?php print $links; ?>
</div>
