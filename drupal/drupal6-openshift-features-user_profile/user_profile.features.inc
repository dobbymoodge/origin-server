<?php

/**
 * Implementation of hook_ctools_plugin_api().
 */
function user_profile_ctools_plugin_api() {
  list($module, $api) = func_get_args();
  if ($module == "context" && $api == "context") {
    return array("version" => 3);
  }
}

/**
 * Implementation of hook_imagecache_default_presets().
 */
function user_profile_imagecache_default_presets() {
  $items = array(
    'user_image_large_80x80' => array(
      'presetname' => 'user_image_large_80x80',
      'actions' => array(
        '0' => array(
          'weight' => '0',
          'module' => 'imagecache',
          'action' => 'imagecache_scale_and_crop',
          'data' => array(
            'width' => '80',
            'height' => '80',
          ),
        ),
      ),
    ),
    'user_image_medium_40x40' => array(
      'presetname' => 'user_image_medium_40x40',
      'actions' => array(
        '0' => array(
          'weight' => '0',
          'module' => 'imagecache',
          'action' => 'imagecache_scale_and_crop',
          'data' => array(
            'width' => '40',
            'height' => '40',
          ),
        ),
      ),
    ),
    'user_image_small_20x20' => array(
      'presetname' => 'user_image_small_20x20',
      'actions' => array(
        '0' => array(
          'weight' => '0',
          'module' => 'imagecache',
          'action' => 'imagecache_scale_and_crop',
          'data' => array(
            'width' => '20',
            'height' => '20',
          ),
        ),
      ),
    ),
  );
  return $items;
}

/**
 * Implementation of hook_node_info().
 */
function user_profile_node_info() {
  $items = array(
    'book' => array(
      'name' => t('Book page'),
      'module' => 'features',
      'description' => t('A <em>book page</em> is a page of content, organized into a collection of related entries collectively known as a <em>book</em>. A <em>book page</em> automatically displays links to adjacent pages, providing a simple navigation system for organizing and reviewing structured content.'),
      'has_title' => '1',
      'title_label' => t('Title'),
      'has_body' => '1',
      'body_label' => t('Body'),
      'min_word_count' => '0',
      'help' => '',
    ),
    'file' => array(
      'name' => t('File'),
      'module' => 'features',
      'description' => t('For use in distributing files from the community.  Admin access only.'),
      'has_title' => '1',
      'title_label' => t('Title'),
      'has_body' => '0',
      'body_label' => '',
      'min_word_count' => '0',
      'help' => '',
    ),
    'partner' => array(
      'name' => t('Partner'),
      'module' => 'features',
      'description' => t('Information about an OpenShift partner, displayed on the partners page.'),
      'has_title' => '1',
      'title_label' => t('Partner Name'),
      'has_body' => '1',
      'body_label' => t('Description'),
      'min_word_count' => '0',
      'help' => '',
    ),
  );
  return $items;
}

/**
 * Implementation of hook_views_api().
 */
function user_profile_views_api() {
  return array(
    'api' => '2',
  );
}
