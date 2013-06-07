<?php
//echo '<pre>';
//print_r($node->uid);
//$user->uid;
//echo '</pre>';
$do = og_comment_perms_do();
?>
<?php if (!$status) { ?><div class="node-unpublished"><?php } ?>

  <div class="metadata">
    <?php if ($submitted) {
      print 'Feature request from ' . theme('username', $node) . ' on ' . format_date($created, $type='custom', $format = 'F j, Y');
    } ?>
    <?php if ($terms): ?>
      | <span class="terms terms-inline"><?php print $terms ?></span>
    <?php endif;?>
  </div>

  <?php if ($node->field_state[0]['value'] == 'Completed'): ?>
    <h3 class='implemented'>This feature has been implemented</h3>
    <br />
    <?php print $node->content['body']['#value'] ?>
  <?php else: print $content ?>
  <?php endif; ?>
    
  <?php if ($links): ?>
    <p class="links clearfix"><?php print $links; ?></p>
  <?php endif; ?>

  <?php print openshift_social_sharing($node_url); ?>      

<?php if (!$status) { ?></div><?php } ?>