<article id="node-<?php print $node->nid; ?>" class="quickstart node<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?> node-quickstart">

  <?php if ($node->field_quickstart_icon[0]){ ?><div class="pull-right"><?php print $node->field_quickstart_icon[0]['view']; ?></div><?php } ?>
  <div class="metadata"><?php 
  $trust = $node->field_quickstart_trust[0]; 
  if (!empty($trust['value'])) {

    if ($trust['value'] == 'partner' || $trust['value'] == 'openshift') {
      print "<span class='provider trusted' title='This QuickStart is provided by OpenShift or a partner.'>";
    } else {
      print "<span class='provider' title='This QuickStart is provided by the community - please review before deploying.'>";
    }
    print check_plain($trust['view']);

    ?></span><?php
  }
  ?>
  <span class="created">Added by <?php print $node->name; ?> on <?php print readabledate($node->created); ?></span>
  <?php if ($node->comment_count > 0) { ?><span class="divider"> | </span><span class="comment-count"><?php print $node->comment_count; ?> comments</span><?php } ?>
  </div>

  <p><a class="btn btn-primary" href="<?php print openshift_server_url(); ?>/app/console/application_types/quickstart!<?php print check_plain($node->nid); ?>">Deploy Now</a></p>

  <div class="content cleafix">
    <div class="pull-right" style="margin-left: 10px;"><?php print $node->content['vud_node_widget_display']['#value']; ?></div>
    <?php print $node->content['body']['#value']; ?>
    <p class="action-quickstart">
      <span class="requires"><?php 
        print application_quickstarts_summary(
          $node->field_cartridges_list[0]['value'], 
          $node->field_git_repository_url[0]['value']);
        ?></span>
    </p>
    <?php print $field_code_language_rendered; ?>
    <?php print $field_website_rendered; ?>
  </div>

  <?php if ($taxonomy): ?>
    <div class="terms">Tags: <?php print $terms ?></div>
  <?php endif;?>

  <?php if ($links): ?>
    <div class="links"><?php print $links; ?></div>
  <?php endif; ?>

  <?php print openshift_social_sharing($node_url, $title); ?>    

</article>
