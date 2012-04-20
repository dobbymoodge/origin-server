<?php
// $Id: node-og-group-post.tpl.php,v 1.3 2008/11/09 17:17:54 weitzman Exp $

/**
 * @file node-og-group-post.tpl.php
 * 
 * Og has added a brief section at bottom for printing links to affiliated groups.
 * This template is used by default for non group nodes.
 *
 * Theme implementation to display a node.
 *
 * Available variables:
 * - $title: the (sanitized) title of the node.
 * - $content: Node body or teaser depending on $teaser flag.
 * - $picture: The authors picture of the node output from
 *   theme_user_picture().
 * - $date: Formatted creation date (use $created to reformat with
 *   format_date()).
 * - $links: Themed links like "Read more", "Add new comment", etc. output
 *   from theme_links().
 * - $name: Themed username of node author output from theme_user().
 * - $node_url: Direct url of the current node.
 * - $terms: the themed list of taxonomy term links output from theme_links().
 * - $submitted: themed submission information output from
 *   theme_node_submitted().
 *
 * Other variables:
 * - $node: Full node object. Contains data that may not be safe.
 * - $type: Node type, i.e. story, page, blog, etc.
 * - $comment_count: Number of comments attached to the node.
 * - $uid: User ID of the node author.
 * - $created: Time the node was published formatted in Unix timestamp.
 * - $zebra: Outputs either "even" or "odd". Useful for zebra striping in
 *   teaser listings.
 * - $id: Position of the node. Increments each time it's output.
 *
 * Node status variables:
 * - $teaser: Flag for the teaser state.
 * - $page: Flag for the full page state.
 * - $promote: Flag for front page promotion state.
 * - $sticky: Flags for sticky post setting.
 * - $status: Flag for published status.
 * - $comment: State of comment settings for the node.
 * - $readmore: Flags true if the teaser content of the node cannot hold the
 *   main body content.
 * - $is_front: Flags true when presented in the front page.
 * - $logged_in: Flags true when the current user is a logged-in member.
 * - $is_admin: Flags true when the current user is an administrator.
 *
 * @see template_preprocess()
 * @see template_preprocess_node()
 */
?>
<?php
//echo '<pre>';
//print_r($node->uid);
//$user->uid;
//echo '</pre>';
$do = og_comment_perms_do();
?>
<div id="node-<?php print $node->nid; ?>" class="thread node node-og-group-post<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?>">

  <?php if ($forum) { ?>
    <ul class="forum-navigation-links">
      <li><a href="<?php print base_path(); ?>forums"><?php print t('Main List of Forums'); ?></a></li>
      <li><a href="<?php print base_path(); ?>forums/<?php print $forum['id'] ?>"><?php print $forum['title']; ?></a></li>
    </ul><?php
  } ?>

<div class="clearfix" id="thread-intro">
	<?php print theme('user_picture', $node); ?>

  <h2><?php print $title ?></h2>
  

  <div class="meta thread-author">
  <?php if ($submitted): ?>
    <div class="submitted">
      <?php
      print '<span>by <strong>' . theme('username', $node) . '</strong> on </span>' . format_date($created, $type='custom', $format = 'F j, Y');
      ?>
    </div>
  <?php endif; ?>

  <?php print views_embed_view('user_profile_box', 'block_3', $node->uid); ?>

  <?php if ($terms): ?>
    <div class="terms terms-inline"><?php print $terms ?></div>
  <?php endif;?>
  </div>
</div><!-- /thread-intro -->

  <div id="thread-text" class="content">
    <?php print $content ?>
  </div>
  <?php if ($do->perm == 'post'): ?>
  
  <div class="new-post-button"><a class="btn" href="#comment-form">Reply to Thread</a></div>
  <?php endif; ?>
  
  
  <?php print $links; ?>
</div>
