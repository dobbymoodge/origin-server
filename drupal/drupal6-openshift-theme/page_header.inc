<?php

  $contexts = context_active_contexts();
  if (array_key_exists('viewing-developer-center', $contexts)) {
    $config = array(
      'menu_name' => 'primary-links',
      'level' => 2,
      'menu_class' => 'nav nav-list',
      'sub_menu_class' => 'nav nav-list',
      'hide_titles' => 1,
      'delta' => '1',
      'collapsible' => array(
        'from_depth' => 2,
        'collapse_menu_class' => 'nav nav-list collapse',
        'expanded_menu_class' => 'nav nav-list collapse in',
      ),
    );
    $tree = openshift_menu_tree_build($config);
    if ($tree) {
      $data = openshift_menu_tree_block_output($tree, $config);
      if ($data['content']) {
        $sidebar_left = '<h3>' . $data['subject'] . '</h3>' . $data['content'] . $sidebar_left;
      }
    }
  }
  // Special conditions that are difficult to represent as contexts
  elseif (!$user->uid && $_GET['q'] == 'user') {
  }
  elseif (array_key_exists('viewing-page', $contexts)) {
    $config = array(
      'menu_name' => 'primary-links',
      'level' => 2,
      'depth' => 1,
      'hide_titles' => 1,
      'menu_class' => 'nav nav-tabs nav-tabs-secondary',
      'highlight_active_trail' => TRUE,
    );
    $tree = openshift_menu_tree_build($config);
    $content_header = openshift_menu_block_tree_output($tree, $config) . $content_header;

    $config['level'] = 3;
    $config['depth'] = NULL;
    $config['expanded'] = TRUE;
    $config['menu_class'] = 'nav nav-list nav-tertiary';
    $config['sub_menu_class'] = 'nav nav-list';
    $config['highlight_active_trail'] = FALSE;
    $tree = openshift_menu_tree_build($config);
    $sidebar_right = openshift_menu_block_tree_output($tree, $config) . $sidebar_right;
  }

  if (empty($sidebar_left)) {
    if (empty($sidebar_right)) { $layout = 'none'; }
    else { $layout = 'right'; }
  }
  else {
    if (empty($sidebar_right)) { $layout = 'left'; }
    else { $layout = 'both'; }
  }

?><!DOCTYPE html>
<!--[if lt IE 7]> <html class="ie6 no-js" lang="en"> <![endif]-->
<!--[if IE 7]>    <html class="ie7 no-js" lang="en"> <![endif]-->
<!--[if IE 8]>    <html class="ie8 no-js" lang="en"> <![endif]-->
<!--[if IE 9]>    <html class="ie9 no-js" lang="en"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class='no-js' lang='en'>
  <!--<![endif]-->
  <head>
    <meta charset='utf-8'>
    <meta content='IE=edge,chrome=1' http-equiv='X-UA-Compatible'>
    <?php print $head; ?>
    <title><?php print $head_title; ?></title>
    <?php if ($node && isset($node->field_search_meta_description) && $node->field_search_meta_description[0]) { ?>
    <meta name="description" content="<?php print $node->field_search_meta_description[0]['safe']; ?>">
    <?php }

      $openshift_server_url = openshift_server_url();
      // reference CSS files directly from openshift
      //print_r(menu_get_active_trail());
      global $base_url;
      global $base_root;
    ?> 
    <link type="image/png" rel="shortcut icon" href="<?php print openshift_assets_url(); ?>/favicon-32.png"></link>
    <link type="text/css" rel="stylesheet" href="<?php print openshift_assets_url(); ?>/overpass.css"></link>
    <script src="<?php print openshift_assets_url(); ?>/modernizr.min.js" type="text/javascript"></script>
    <link type="text/css" rel="stylesheet" href="<?php print openshift_assets_url(); ?>/common.css"></link>
    <link type="text/css" rel="stylesheet" href="<?php print openshift_assets_url(); ?>/site.css"></link>
	  <?php print $styles; ?>
    <script type="text/javascript" src="<?php print openshift_assets_url(); ?>/application.js"></script>
	  <?php print $scripts; ?>
    <meta content='' name='author'>
    <meta content='width=device-width, initial-scale=1.0' name='viewport'>
    <meta name="csrf-param" content="authenticity_token"/>
    <meta name="csrf-token" content="+CyXrdA5MZFVwLks73ibMfRiwRE+ixICENvvHms1Exk="/>
  </head>
  <body class='<?php print $body_classes; ?> community'>
