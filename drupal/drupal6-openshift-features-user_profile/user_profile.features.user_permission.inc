<?php

/**
 * Implementation of hook_user_default_permissions().
 */
function user_profile_user_default_permissions() {
  $permissions = array();

  // Exported permission: Use PHP input for field settings (dangerous - grant with care)
  $permissions['Use PHP input for field settings (dangerous - grant with care)'] = array(
    'name' => 'Use PHP input for field settings (dangerous - grant with care)',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: access administration menu
  $permissions['access administration menu'] = array(
    'name' => 'access administration menu',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: access administration pages
  $permissions['access administration pages'] = array(
    'name' => 'access administration pages',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: access all views
  $permissions['access all views'] = array(
    'name' => 'access all views',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: access comments
  $permissions['access comments'] = array(
    'name' => 'access comments',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
    ),
  );

  // Exported permission: access content
  $permissions['access content'] = array(
    'name' => 'access content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
      '4' => 'page author',
    ),
  );

  // Exported permission: access devel information
  $permissions['access devel information'] = array(
    'name' => 'access devel information',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: access site reports
  $permissions['access site reports'] = array(
    'name' => 'access site reports',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: access statistics
  $permissions['access statistics'] = array(
    'name' => 'access statistics',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: access user profiles
  $permissions['access user profiles'] = array(
    'name' => 'access user profiles',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: access vote up/down statistics
  $permissions['access vote up/down statistics'] = array(
    'name' => 'access vote up/down statistics',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer actions
  $permissions['administer actions'] = array(
    'name' => 'administer actions',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer block classes
  $permissions['administer block classes'] = array(
    'name' => 'administer block classes',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer blocks
  $permissions['administer blocks'] = array(
    'name' => 'administer blocks',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer comments
  $permissions['administer comments'] = array(
    'name' => 'administer comments',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: administer content types
  $permissions['administer content types'] = array(
    'name' => 'administer content types',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer custom breadcrumbs
  $permissions['administer custom breadcrumbs'] = array(
    'name' => 'administer custom breadcrumbs',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer faq
  $permissions['administer faq'] = array(
    'name' => 'administer faq',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer faq order
  $permissions['administer faq order'] = array(
    'name' => 'administer faq order',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer features
  $permissions['administer features'] = array(
    'name' => 'administer features',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer files
  $permissions['administer files'] = array(
    'name' => 'administer files',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer filters
  $permissions['administer filters'] = array(
    'name' => 'administer filters',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer flags
  $permissions['administer flags'] = array(
    'name' => 'administer flags',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer homebox
  $permissions['administer homebox'] = array(
    'name' => 'administer homebox',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer imageapi
  $permissions['administer imageapi'] = array(
    'name' => 'administer imageapi',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer imagecache
  $permissions['administer imagecache'] = array(
    'name' => 'administer imagecache',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer menu
  $permissions['administer menu'] = array(
    'name' => 'administer menu',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer messaging
  $permissions['administer messaging'] = array(
    'name' => 'administer messaging',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer nodes
  $permissions['administer nodes'] = array(
    'name' => 'administer nodes',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: administer notifications
  $permissions['administer notifications'] = array(
    'name' => 'administer notifications',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer organic groups
  $permissions['administer organic groups'] = array(
    'name' => 'administer organic groups',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer pathauto
  $permissions['administer pathauto'] = array(
    'name' => 'administer pathauto',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: administer permissions
  $permissions['administer permissions'] = array(
    'name' => 'administer permissions',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer redirects
  $permissions['administer redirects'] = array(
    'name' => 'administer redirects',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: administer rules
  $permissions['administer rules'] = array(
    'name' => 'administer rules',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer search
  $permissions['administer search'] = array(
    'name' => 'administer search',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer site configuration
  $permissions['administer site configuration'] = array(
    'name' => 'administer site configuration',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer string overrides
  $permissions['administer string overrides'] = array(
    'name' => 'administer string overrides',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer taxonomy
  $permissions['administer taxonomy'] = array(
    'name' => 'administer taxonomy',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer url aliases
  $permissions['administer url aliases'] = array(
    'name' => 'administer url aliases',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: administer userpoints
  $permissions['administer userpoints'] = array(
    'name' => 'administer userpoints',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer users
  $permissions['administer users'] = array(
    'name' => 'administer users',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: administer views
  $permissions['administer views'] = array(
    'name' => 'administer views',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer vote up/down
  $permissions['administer vote up/down'] = array(
    'name' => 'administer vote up/down',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer vote up/down on comments
  $permissions['administer vote up/down on comments'] = array(
    'name' => 'administer vote up/down on comments',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer vote up/down on nodes
  $permissions['administer vote up/down on nodes'] = array(
    'name' => 'administer vote up/down on nodes',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer voting api
  $permissions['administer voting api'] = array(
    'name' => 'administer voting api',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: administer xmlsitemap
  $permissions['administer xmlsitemap'] = array(
    'name' => 'administer xmlsitemap',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: cancel own vote
  $permissions['cancel own vote'] = array(
    'name' => 'cancel own vote',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: change badge assignments
  $permissions['change badge assignments'] = array(
    'name' => 'change badge assignments',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: change own username
  $permissions['change own username'] = array(
    'name' => 'change own username',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: collapse format fieldset by default
  $permissions['collapse format fieldset by default'] = array(
    'name' => 'collapse format fieldset by default',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: collapsible format selection
  $permissions['collapsible format selection'] = array(
    'name' => 'collapsible format selection',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: create author content
  $permissions['create author content'] = array(
    'name' => 'create author content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: create blog content
  $permissions['create blog content'] = array(
    'name' => 'create blog content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'content author',
      '3' => 'moderator',
    ),
  );

  // Exported permission: create discussion content
  $permissions['create discussion content'] = array(
    'name' => 'create discussion content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: create document content
  $permissions['create document content'] = array(
    'name' => 'create document content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
      '2' => 'doc content owner',
      '3' => 'moderator',
    ),
  );

  // Exported permission: create event content
  $permissions['create event content'] = array(
    'name' => 'create event content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'content author',
      '3' => 'doc content owner',
      '4' => 'moderator',
    ),
  );

  // Exported permission: create faq
  $permissions['create faq'] = array(
    'name' => 'create faq',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: create file content
  $permissions['create file content'] = array(
    'name' => 'create file content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: create group content
  $permissions['create group content'] = array(
    'name' => 'create group content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: create idea content
  $permissions['create idea content'] = array(
    'name' => 'create idea content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'blogger',
      '3' => 'doc content owner',
      '4' => 'moderator',
    ),
  );

  // Exported permission: create knowledge_base content
  $permissions['create knowledge_base content'] = array(
    'name' => 'create knowledge_base content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: create newsletter content
  $permissions['create newsletter content'] = array(
    'name' => 'create newsletter content',
    'roles' => array(
      '0' => 'content author',
    ),
  );

  // Exported permission: create page content
  $permissions['create page content'] = array(
    'name' => 'create page content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
      '2' => 'moderator',
      '3' => 'page author',
    ),
  );

  // Exported permission: create partner content
  $permissions['create partner content'] = array(
    'name' => 'create partner content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
      '3' => 'page author',
    ),
  );

  // Exported permission: create poll content
  $permissions['create poll content'] = array(
    'name' => 'create poll content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: create promotion_blocks content
  $permissions['create promotion_blocks content'] = array(
    'name' => 'create promotion_blocks content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: create quickstart content
  $permissions['create quickstart content'] = array(
    'name' => 'create quickstart content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: create story content
  $permissions['create story content'] = array(
    'name' => 'create story content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: create url aliases
  $permissions['create url aliases'] = array(
    'name' => 'create url aliases',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: create video content
  $permissions['create video content'] = array(
    'name' => 'create video content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete any author content
  $permissions['delete any author content'] = array(
    'name' => 'delete any author content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any blog content
  $permissions['delete any blog content'] = array(
    'name' => 'delete any blog content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any discussion content
  $permissions['delete any discussion content'] = array(
    'name' => 'delete any discussion content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any document content
  $permissions['delete any document content'] = array(
    'name' => 'delete any document content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'doc content owner',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete any event content
  $permissions['delete any event content'] = array(
    'name' => 'delete any event content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any file content
  $permissions['delete any file content'] = array(
    'name' => 'delete any file content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete any group content
  $permissions['delete any group content'] = array(
    'name' => 'delete any group content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any idea content
  $permissions['delete any idea content'] = array(
    'name' => 'delete any idea content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any knowledge_base content
  $permissions['delete any knowledge_base content'] = array(
    'name' => 'delete any knowledge_base content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any newsletter content
  $permissions['delete any newsletter content'] = array(
    'name' => 'delete any newsletter content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any page content
  $permissions['delete any page content'] = array(
    'name' => 'delete any page content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete any partner content
  $permissions['delete any partner content'] = array(
    'name' => 'delete any partner content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any poll content
  $permissions['delete any poll content'] = array(
    'name' => 'delete any poll content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any promotion_blocks content
  $permissions['delete any promotion_blocks content'] = array(
    'name' => 'delete any promotion_blocks content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any quickstart content
  $permissions['delete any quickstart content'] = array(
    'name' => 'delete any quickstart content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete any story content
  $permissions['delete any story content'] = array(
    'name' => 'delete any story content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete any video content
  $permissions['delete any video content'] = array(
    'name' => 'delete any video content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete faq content
  $permissions['delete faq content'] = array(
    'name' => 'delete faq content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete own author content
  $permissions['delete own author content'] = array(
    'name' => 'delete own author content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own blog content
  $permissions['delete own blog content'] = array(
    'name' => 'delete own blog content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own discussion content
  $permissions['delete own discussion content'] = array(
    'name' => 'delete own discussion content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own document content
  $permissions['delete own document content'] = array(
    'name' => 'delete own document content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'doc content owner',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own event content
  $permissions['delete own event content'] = array(
    'name' => 'delete own event content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own faq content
  $permissions['delete own faq content'] = array(
    'name' => 'delete own faq content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete own file content
  $permissions['delete own file content'] = array(
    'name' => 'delete own file content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete own group content
  $permissions['delete own group content'] = array(
    'name' => 'delete own group content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete own idea content
  $permissions['delete own idea content'] = array(
    'name' => 'delete own idea content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: delete own knowledge_base content
  $permissions['delete own knowledge_base content'] = array(
    'name' => 'delete own knowledge_base content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete own newsletter content
  $permissions['delete own newsletter content'] = array(
    'name' => 'delete own newsletter content',
    'roles' => array(),
  );

  // Exported permission: delete own page content
  $permissions['delete own page content'] = array(
    'name' => 'delete own page content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: delete own partner content
  $permissions['delete own partner content'] = array(
    'name' => 'delete own partner content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: delete own poll content
  $permissions['delete own poll content'] = array(
    'name' => 'delete own poll content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete own promotion_blocks content
  $permissions['delete own promotion_blocks content'] = array(
    'name' => 'delete own promotion_blocks content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete own quickstart content
  $permissions['delete own quickstart content'] = array(
    'name' => 'delete own quickstart content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: delete own story content
  $permissions['delete own story content'] = array(
    'name' => 'delete own story content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: delete own video content
  $permissions['delete own video content'] = array(
    'name' => 'delete own video content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: delete revisions
  $permissions['delete revisions'] = array(
    'name' => 'delete revisions',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: display drupal links
  $permissions['display drupal links'] = array(
    'name' => 'display drupal links',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: display source code
  $permissions['display source code'] = array(
    'name' => 'display source code',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit any author content
  $permissions['edit any author content'] = array(
    'name' => 'edit any author content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: edit any blog content
  $permissions['edit any blog content'] = array(
    'name' => 'edit any blog content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
      '3' => 'page author',
    ),
  );

  // Exported permission: edit any discussion content
  $permissions['edit any discussion content'] = array(
    'name' => 'edit any discussion content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any document content
  $permissions['edit any document content'] = array(
    'name' => 'edit any document content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'doc content owner',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit any event content
  $permissions['edit any event content'] = array(
    'name' => 'edit any event content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit any file content
  $permissions['edit any file content'] = array(
    'name' => 'edit any file content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit any group content
  $permissions['edit any group content'] = array(
    'name' => 'edit any group content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any idea content
  $permissions['edit any idea content'] = array(
    'name' => 'edit any idea content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any knowledge_base content
  $permissions['edit any knowledge_base content'] = array(
    'name' => 'edit any knowledge_base content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any newsletter content
  $permissions['edit any newsletter content'] = array(
    'name' => 'edit any newsletter content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit any page content
  $permissions['edit any page content'] = array(
    'name' => 'edit any page content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: edit any partner content
  $permissions['edit any partner content'] = array(
    'name' => 'edit any partner content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any poll content
  $permissions['edit any poll content'] = array(
    'name' => 'edit any poll content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit any promotion_blocks content
  $permissions['edit any promotion_blocks content'] = array(
    'name' => 'edit any promotion_blocks content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any quickstart content
  $permissions['edit any quickstart content'] = array(
    'name' => 'edit any quickstart content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit any story content
  $permissions['edit any story content'] = array(
    'name' => 'edit any story content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit any video content
  $permissions['edit any video content'] = array(
    'name' => 'edit any video content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit faq
  $permissions['edit faq'] = array(
    'name' => 'edit faq',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit field_author
  $permissions['edit field_author'] = array(
    'name' => 'edit field_author',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'doc content owner',
      '3' => 'moderator',
      '4' => 'page author',
    ),
  );

  // Exported permission: edit field_author_image
  $permissions['edit field_author_image'] = array(
    'name' => 'edit field_author_image',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'doc content owner',
      '3' => 'moderator',
      '4' => 'page author',
    ),
  );

  // Exported permission: edit field_author_profession_title
  $permissions['edit field_author_profession_title'] = array(
    'name' => 'edit field_author_profession_title',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'doc content owner',
      '3' => 'moderator',
      '4' => 'page author',
    ),
  );

  // Exported permission: edit field_cartridges_list
  $permissions['edit field_cartridges_list'] = array(
    'name' => 'edit field_cartridges_list',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit field_code_language
  $permissions['edit field_code_language'] = array(
    'name' => 'edit field_code_language',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit field_document_file
  $permissions['edit field_document_file'] = array(
    'name' => 'edit field_document_file',
    'roles' => array(
      '0' => 'authenticated user',
      '1' => 'content author',
    ),
  );

  // Exported permission: edit field_event_categories
  $permissions['edit field_event_categories'] = array(
    'name' => 'edit field_event_categories',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_city
  $permissions['edit field_event_city'] = array(
    'name' => 'edit field_event_city',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_country
  $permissions['edit field_event_country'] = array(
    'name' => 'edit field_event_country',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_logo
  $permissions['edit field_event_logo'] = array(
    'name' => 'edit field_event_logo',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_online
  $permissions['edit field_event_online'] = array(
    'name' => 'edit field_event_online',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_short_description
  $permissions['edit field_event_short_description'] = array(
    'name' => 'edit field_event_short_description',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_start_date
  $permissions['edit field_event_start_date'] = array(
    'name' => 'edit field_event_start_date',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_state
  $permissions['edit field_event_state'] = array(
    'name' => 'edit field_event_state',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_url
  $permissions['edit field_event_url'] = array(
    'name' => 'edit field_event_url',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_event_venue
  $permissions['edit field_event_venue'] = array(
    'name' => 'edit field_event_venue',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_file
  $permissions['edit field_file'] = array(
    'name' => 'edit field_file',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
    ),
  );

  // Exported permission: edit field_git_repository_url
  $permissions['edit field_git_repository_url'] = array(
    'name' => 'edit field_git_repository_url',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit field_image_upload
  $permissions['edit field_image_upload'] = array(
    'name' => 'edit field_image_upload',
    'roles' => array(
      '0' => 'authenticated user',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_kb_applies_to
  $permissions['edit field_kb_applies_to'] = array(
    'name' => 'edit field_kb_applies_to',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_kb_attachment
  $permissions['edit field_kb_attachment'] = array(
    'name' => 'edit field_kb_attachment',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'doc content owner',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_kb_code
  $permissions['edit field_kb_code'] = array(
    'name' => 'edit field_kb_code',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_kb_issue
  $permissions['edit field_kb_issue'] = array(
    'name' => 'edit field_kb_issue',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_kb_resolution
  $permissions['edit field_kb_resolution'] = array(
    'name' => 'edit field_kb_resolution',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_page_image
  $permissions['edit field_page_image'] = array(
    'name' => 'edit field_page_image',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: edit field_promo_image
  $permissions['edit field_promo_image'] = array(
    'name' => 'edit field_promo_image',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_promo_url
  $permissions['edit field_promo_url'] = array(
    'name' => 'edit field_promo_url',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_quickstart_admin_tags
  $permissions['edit field_quickstart_admin_tags'] = array(
    'name' => 'edit field_quickstart_admin_tags',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit field_quickstart_icon
  $permissions['edit field_quickstart_icon'] = array(
    'name' => 'edit field_quickstart_icon',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit field_quickstart_priority
  $permissions['edit field_quickstart_priority'] = array(
    'name' => 'edit field_quickstart_priority',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit field_quickstart_trust
  $permissions['edit field_quickstart_trust'] = array(
    'name' => 'edit field_quickstart_trust',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_search_meta_description
  $permissions['edit field_search_meta_description'] = array(
    'name' => 'edit field_search_meta_description',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'doc content owner',
      '3' => 'page author',
    ),
  );

  // Exported permission: edit field_state
  $permissions['edit field_state'] = array(
    'name' => 'edit field_state',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit field_summary
  $permissions['edit field_summary'] = array(
    'name' => 'edit field_summary',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_video_subtitle
  $permissions['edit field_video_subtitle'] = array(
    'name' => 'edit field_video_subtitle',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_video_third_party
  $permissions['edit field_video_third_party'] = array(
    'name' => 'edit field_video_third_party',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_video_thumbnail
  $permissions['edit field_video_thumbnail'] = array(
    'name' => 'edit field_video_thumbnail',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_video_youku
  $permissions['edit field_video_youku'] = array(
    'name' => 'edit field_video_youku',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit field_website
  $permissions['edit field_website'] = array(
    'name' => 'edit field_website',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own author content
  $permissions['edit own author content'] = array(
    'name' => 'edit own author content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'moderator',
    ),
  );

  // Exported permission: edit own blog content
  $permissions['edit own blog content'] = array(
    'name' => 'edit own blog content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own discussion content
  $permissions['edit own discussion content'] = array(
    'name' => 'edit own discussion content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own document content
  $permissions['edit own document content'] = array(
    'name' => 'edit own document content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
      '2' => 'doc content owner',
      '3' => 'moderator',
    ),
  );

  // Exported permission: edit own event content
  $permissions['edit own event content'] = array(
    'name' => 'edit own event content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own faq
  $permissions['edit own faq'] = array(
    'name' => 'edit own faq',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit own file content
  $permissions['edit own file content'] = array(
    'name' => 'edit own file content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit own group content
  $permissions['edit own group content'] = array(
    'name' => 'edit own group content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit own idea content
  $permissions['edit own idea content'] = array(
    'name' => 'edit own idea content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own knowledge_base content
  $permissions['edit own knowledge_base content'] = array(
    'name' => 'edit own knowledge_base content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit own newsletter content
  $permissions['edit own newsletter content'] = array(
    'name' => 'edit own newsletter content',
    'roles' => array(
      '0' => 'content author',
    ),
  );

  // Exported permission: edit own page content
  $permissions['edit own page content'] = array(
    'name' => 'edit own page content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'content author',
      '2' => 'moderator',
      '3' => 'page author',
    ),
  );

  // Exported permission: edit own partner content
  $permissions['edit own partner content'] = array(
    'name' => 'edit own partner content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own poll content
  $permissions['edit own poll content'] = array(
    'name' => 'edit own poll content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit own promotion_blocks content
  $permissions['edit own promotion_blocks content'] = array(
    'name' => 'edit own promotion_blocks content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: edit own quickstart content
  $permissions['edit own quickstart content'] = array(
    'name' => 'edit own quickstart content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: edit own story content
  $permissions['edit own story content'] = array(
    'name' => 'edit own story content',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: edit own video content
  $permissions['edit own video content'] = array(
    'name' => 'edit own video content',
    'roles' => array(
      '0' => 'authenticated user',
    ),
  );

  // Exported permission: execute php code
  $permissions['execute php code'] = array(
    'name' => 'execute php code',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: flush imagecache
  $permissions['flush imagecache'] = array(
    'name' => 'flush imagecache',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: inspect all votes
  $permissions['inspect all votes'] = array(
    'name' => 'inspect all votes',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: maintain own subscriptions
  $permissions['maintain own subscriptions'] = array(
    'name' => 'maintain own subscriptions',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: manage all subscriptions
  $permissions['manage all subscriptions'] = array(
    'name' => 'manage all subscriptions',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: manage badges
  $permissions['manage badges'] = array(
    'name' => 'manage badges',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: manage features
  $permissions['manage features'] = array(
    'name' => 'manage features',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: manage own subscriptions
  $permissions['manage own subscriptions'] = array(
    'name' => 'manage own subscriptions',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: notify of path changes
  $permissions['notify of path changes'] = array(
    'name' => 'notify of path changes',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: post comments
  $permissions['post comments'] = array(
    'name' => 'post comments',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: post comments without approval
  $permissions['post comments without approval'] = array(
    'name' => 'post comments without approval',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: rate content
  $permissions['rate content'] = array(
    'name' => 'rate content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: reset vote up/down votes
  $permissions['reset vote up/down votes'] = array(
    'name' => 'reset vote up/down votes',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: revert revisions
  $permissions['revert revisions'] = array(
    'name' => 'revert revisions',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'page author',
    ),
  );

  // Exported permission: search content
  $permissions['search content'] = array(
    'name' => 'search content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
    ),
  );

  // Exported permission: see vote up/down node stats
  $permissions['see vote up/down node stats'] = array(
    'name' => 'see vote up/down node stats',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: select different theme
  $permissions['select different theme'] = array(
    'name' => 'select different theme',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: show format selection for blocks
  $permissions['show format selection for blocks'] = array(
    'name' => 'show format selection for blocks',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: show format selection for comments
  $permissions['show format selection for comments'] = array(
    'name' => 'show format selection for comments',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: show format selection for nodes
  $permissions['show format selection for nodes'] = array(
    'name' => 'show format selection for nodes',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: show format tips
  $permissions['show format tips'] = array(
    'name' => 'show format tips',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: show more format tips link
  $permissions['show more format tips link'] = array(
    'name' => 'show more format tips link',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: skip notifications
  $permissions['skip notifications'] = array(
    'name' => 'skip notifications',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: subscribe to author
  $permissions['subscribe to author'] = array(
    'name' => 'subscribe to author',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: subscribe to content
  $permissions['subscribe to content'] = array(
    'name' => 'subscribe to content',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: subscribe to content in groups
  $permissions['subscribe to content in groups'] = array(
    'name' => 'subscribe to content in groups',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: subscribe to content type
  $permissions['subscribe to content type'] = array(
    'name' => 'subscribe to content type',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: switch users
  $permissions['switch users'] = array(
    'name' => 'switch users',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: upload files
  $permissions['upload files'] = array(
    'name' => 'upload files',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'content author',
      '3' => 'doc content owner',
      '4' => 'moderator',
      '5' => 'page author',
    ),
  );

  // Exported permission: use PHP for block visibility
  $permissions['use PHP for block visibility'] = array(
    'name' => 'use PHP for block visibility',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: use PHP for fivestar target
  $permissions['use PHP for fivestar target'] = array(
    'name' => 'use PHP for fivestar target',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: use advanced search
  $permissions['use advanced search'] = array(
    'name' => 'use advanced search',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
    ),
  );

  // Exported permission: use php in custom breadcrumbs
  $permissions['use php in custom breadcrumbs'] = array(
    'name' => 'use php in custom breadcrumbs',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: use views exporter
  $permissions['use views exporter'] = array(
    'name' => 'use views exporter',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: use vote up/down
  $permissions['use vote up/down'] = array(
    'name' => 'use vote up/down',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: use vote up/down on comments
  $permissions['use vote up/down on comments'] = array(
    'name' => 'use vote up/down on comments',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: use vote up/down on nodes
  $permissions['use vote up/down on nodes'] = array(
    'name' => 'use vote up/down on nodes',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: view advanced help index
  $permissions['view advanced help index'] = array(
    'name' => 'view advanced help index',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: view advanced help popup
  $permissions['view advanced help popup'] = array(
    'name' => 'view advanced help popup',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: view advanced help topic
  $permissions['view advanced help topic'] = array(
    'name' => 'view advanced help topic',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: view date repeats
  $permissions['view date repeats'] = array(
    'name' => 'view date repeats',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: view faq page
  $permissions['view faq page'] = array(
    'name' => 'view faq page',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
    ),
  );

  // Exported permission: view field_author
  $permissions['view field_author'] = array(
    'name' => 'view field_author',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_author_image
  $permissions['view field_author_image'] = array(
    'name' => 'view field_author_image',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_author_profession_title
  $permissions['view field_author_profession_title'] = array(
    'name' => 'view field_author_profession_title',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_cartridges_list
  $permissions['view field_cartridges_list'] = array(
    'name' => 'view field_cartridges_list',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_code_language
  $permissions['view field_code_language'] = array(
    'name' => 'view field_code_language',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_document_file
  $permissions['view field_document_file'] = array(
    'name' => 'view field_document_file',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_categories
  $permissions['view field_event_categories'] = array(
    'name' => 'view field_event_categories',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_city
  $permissions['view field_event_city'] = array(
    'name' => 'view field_event_city',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_country
  $permissions['view field_event_country'] = array(
    'name' => 'view field_event_country',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_logo
  $permissions['view field_event_logo'] = array(
    'name' => 'view field_event_logo',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_online
  $permissions['view field_event_online'] = array(
    'name' => 'view field_event_online',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_short_description
  $permissions['view field_event_short_description'] = array(
    'name' => 'view field_event_short_description',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_start_date
  $permissions['view field_event_start_date'] = array(
    'name' => 'view field_event_start_date',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_state
  $permissions['view field_event_state'] = array(
    'name' => 'view field_event_state',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_url
  $permissions['view field_event_url'] = array(
    'name' => 'view field_event_url',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_event_venue
  $permissions['view field_event_venue'] = array(
    'name' => 'view field_event_venue',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_file
  $permissions['view field_file'] = array(
    'name' => 'view field_file',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_git_repository_url
  $permissions['view field_git_repository_url'] = array(
    'name' => 'view field_git_repository_url',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_image_upload
  $permissions['view field_image_upload'] = array(
    'name' => 'view field_image_upload',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_kb_applies_to
  $permissions['view field_kb_applies_to'] = array(
    'name' => 'view field_kb_applies_to',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_kb_attachment
  $permissions['view field_kb_attachment'] = array(
    'name' => 'view field_kb_attachment',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_kb_code
  $permissions['view field_kb_code'] = array(
    'name' => 'view field_kb_code',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_kb_issue
  $permissions['view field_kb_issue'] = array(
    'name' => 'view field_kb_issue',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_kb_resolution
  $permissions['view field_kb_resolution'] = array(
    'name' => 'view field_kb_resolution',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_page_image
  $permissions['view field_page_image'] = array(
    'name' => 'view field_page_image',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_promo_image
  $permissions['view field_promo_image'] = array(
    'name' => 'view field_promo_image',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_promo_url
  $permissions['view field_promo_url'] = array(
    'name' => 'view field_promo_url',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_quickstart_admin_tags
  $permissions['view field_quickstart_admin_tags'] = array(
    'name' => 'view field_quickstart_admin_tags',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_quickstart_icon
  $permissions['view field_quickstart_icon'] = array(
    'name' => 'view field_quickstart_icon',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_quickstart_priority
  $permissions['view field_quickstart_priority'] = array(
    'name' => 'view field_quickstart_priority',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_quickstart_trust
  $permissions['view field_quickstart_trust'] = array(
    'name' => 'view field_quickstart_trust',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_search_meta_description
  $permissions['view field_search_meta_description'] = array(
    'name' => 'view field_search_meta_description',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_state
  $permissions['view field_state'] = array(
    'name' => 'view field_state',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'moderator',
    ),
  );

  // Exported permission: view field_summary
  $permissions['view field_summary'] = array(
    'name' => 'view field_summary',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_video_subtitle
  $permissions['view field_video_subtitle'] = array(
    'name' => 'view field_video_subtitle',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_video_third_party
  $permissions['view field_video_third_party'] = array(
    'name' => 'view field_video_third_party',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_video_thumbnail
  $permissions['view field_video_thumbnail'] = array(
    'name' => 'view field_video_thumbnail',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_video_youku
  $permissions['view field_video_youku'] = array(
    'name' => 'view field_video_youku',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view field_website
  $permissions['view field_website'] = array(
    'name' => 'view field_website',
    'roles' => array(
      '0' => 'anonymous user',
      '1' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache blog_author_image_30x30
  $permissions['view imagecache blog_author_image_30x30'] = array(
    'name' => 'view imagecache blog_author_image_30x30',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache blog_author_image_80x80
  $permissions['view imagecache blog_author_image_80x80'] = array(
    'name' => 'view imagecache blog_author_image_80x80',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache blog_insert_image
  $permissions['view imagecache blog_insert_image'] = array(
    'name' => 'view imagecache blog_insert_image',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache generic_icon_150_50
  $permissions['view imagecache generic_icon_150_50'] = array(
    'name' => 'view imagecache generic_icon_150_50',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache generic_icon_256_256
  $permissions['view imagecache generic_icon_256_256'] = array(
    'name' => 'view imagecache generic_icon_256_256',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache user_image_large_80x80
  $permissions['view imagecache user_image_large_80x80'] = array(
    'name' => 'view imagecache user_image_large_80x80',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache user_image_medium_40x40
  $permissions['view imagecache user_image_medium_40x40'] = array(
    'name' => 'view imagecache user_image_medium_40x40',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view imagecache user_image_small_20x20
  $permissions['view imagecache user_image_small_20x20'] = array(
    'name' => 'view imagecache user_image_small_20x20',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
    ),
  );

  // Exported permission: view own userpoints
  $permissions['view own userpoints'] = array(
    'name' => 'view own userpoints',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  // Exported permission: view post access counter
  $permissions['view post access counter'] = array(
    'name' => 'view post access counter',
    'roles' => array(
      '0' => 'administrator',
    ),
  );

  // Exported permission: view revisions
  $permissions['view revisions'] = array(
    'name' => 'view revisions',
    'roles' => array(
      '0' => 'authenticated user',
      '1' => 'moderator',
      '2' => 'page author',
    ),
  );

  // Exported permission: view uploaded files
  $permissions['view uploaded files'] = array(
    'name' => 'view uploaded files',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'blogger',
      '2' => 'content author',
      '3' => 'doc content owner',
      '4' => 'moderator',
      '5' => 'page author',
    ),
  );

  // Exported permission: view userpoints
  $permissions['view userpoints'] = array(
    'name' => 'view userpoints',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'moderator',
    ),
  );

  // Exported permission: view vote up/down count on nodes
  $permissions['view vote up/down count on nodes'] = array(
    'name' => 'view vote up/down count on nodes',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'anonymous user',
      '2' => 'authenticated user',
      '3' => 'blogger',
      '4' => 'doc content owner',
      '5' => 'moderator',
      '6' => 'page author',
    ),
  );

  // Exported permission: vote on polls
  $permissions['vote on polls'] = array(
    'name' => 'vote on polls',
    'roles' => array(
      '0' => 'administrator',
      '1' => 'authenticated user',
      '2' => 'moderator',
    ),
  );

  return $permissions;
}
