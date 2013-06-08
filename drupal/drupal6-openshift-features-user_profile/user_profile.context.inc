<?php

/**
 * Implementation of hook_context_default_contexts().
 */
function user_profile_context_default_contexts() {
  $export = array();

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'doc-owner-role';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'user' => array(
      'values' => array(
        'doc content owner' => 'doc content owner',
      ),
    ),
  );
  $context->reactions = array(
    'block' => array(
      'blocks' => array(
        'menu-menu-doc-owner-menu' => array(
          'module' => 'menu',
          'delta' => 'menu-doc-owner-menu',
          'region' => 'sidebar_left',
          'weight' => 30,
        ),
      ),
    ),
  );
  $context->condition_mode = 0;
  $export['doc-owner-role'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'get-involved-blocks';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'path' => array(
      'values' => array(
        'get-involved' => 'get-involved',
        'developers/get-involved' => 'developers/get-involved',
      ),
    ),
  );
  $context->reactions = array(
    'block' => array(
      'blocks' => array(
        'views-content_list-block_1' => array(
          'module' => 'views',
          'delta' => 'content_list-block_1',
          'region' => 'content_suffix',
          'weight' => 0,
        ),
        'views-content_list-block_2' => array(
          'module' => 'views',
          'delta' => 'content_list-block_2',
          'region' => 'content_suffix',
          'weight' => 1,
        ),
      ),
    ),
  );
  $context->condition_mode = 0;
  $export['get-involved-blocks'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-blogs';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'author' => 'author',
        'blog' => 'blog',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'blogs',
  );
  $context->condition_mode = 0;
  $export['menu-active-blogs'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-community';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'author' => 'author',
        'newsletter' => 'newsletter',
        'poll' => 'poll',
        'promotion_blocks' => 'promotion_blocks',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'community' => 'community',
        'community/*' => 'community/*',
        'notifications/*' => 'notifications/*',
      ),
    ),
    'user_page' => array(
      'values' => array(
        'form' => 'form',
        'register' => 'register',
        'view' => 'view',
      ),
      'options' => array(
        'mode' => 'all',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'community',
  );
  $context->condition_mode = 0;
  $export['menu-active-community'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-events';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'event' => 'event',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'events' => 'events',
        'calendar' => 'calendar',
        'calendar/*' => 'calendar/*',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'events',
  );
  $context->condition_mode = 0;
  $export['menu-active-events'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-faq';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'faq' => 'faq',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'faq/express-faq' => 'faq/express-faq',
        'faq/openshift-community-faq' => 'faq/openshift-community-faq',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'faq',
  );
  $context->condition_mode = 0;
  $export['menu-active-faq'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-forum';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'discussion' => 'discussion',
        'group' => 'group',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'forums' => 'forums',
        'forums/*' => 'forums/*',
        'og' => 'og',
        'og/*' => 'og/*',
        'node/add/discussion/*' => 'node/add/discussion/*',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'node/1',
  );
  $context->condition_mode = 0;
  $export['menu-active-forum'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-ideas';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'idea' => 'idea',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'views' => array(
      'values' => array(
        'Ideas' => 'Ideas',
        'Ideas:page_1' => 'Ideas:page_1',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'ideas',
  );
  $context->condition_mode = 0;
  $export['menu-active-ideas'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-kb';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'knowledge_base' => 'knowledge_base',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'kb',
  );
  $context->condition_mode = 0;
  $export['menu-active-kb'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-quickstarts';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'quickstart' => 'quickstart',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'quickstart-tags/*' => 'quickstart-tags/*',
      ),
    ),
    'views' => array(
      'values' => array(
        'application_quickstarts_content' => 'application_quickstarts_content',
        'application_quickstarts_content:page_2' => 'application_quickstarts_content:page_2',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'quickstarts',
  );
  $context->condition_mode = 0;
  $export['menu-active-quickstarts'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-user';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'path' => array(
      'values' => array(
        'user' => 'user',
        'user/' => 'user/',
        'user/*' => 'user/*',
        '~user/login' => '~user/login',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'node/9515',
  );
  $context->condition_mode = 1;
  $export['menu-active-user'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-videos';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'video' => 'video',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'views' => array(
      'values' => array(
        'nodes_by_category:page_2' => 'nodes_by_category:page_2',
        'nodes_by_category:page_5' => 'nodes_by_category:page_5',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'videos',
  );
  $context->condition_mode = 0;
  $export['menu-active-videos'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'menu-active-wiki-page';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'node' => array(
      'values' => array(
        'wiki_page' => 'wiki_page',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
  );
  $context->reactions = array(
    'menu' => 'node/9475',
  );
  $context->condition_mode = 0;
  $export['menu-active-wiki-page'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'messaging-home';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['messaging-home'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'moderator-role';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'user' => array(
      'values' => array(
        'moderator' => 'moderator',
      ),
    ),
  );
  $context->reactions = array(
    'block' => array(
      'blocks' => array(
        'menu-menu-moderator-menu' => array(
          'module' => 'menu',
          'delta' => 'menu-moderator-menu',
          'region' => 'sidebar_left',
          'weight' => 50,
        ),
      ),
    ),
  );
  $context->condition_mode = 0;
  $export['moderator-role'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'recent-changes-sidebar';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array(
    'block' => array(
      'blocks' => array(
        'views-nodes_by_category-block_3' => array(
          'module' => 'views',
          'delta' => 'nodes_by_category-block_3',
          'region' => 'sidebar_left',
          'weight' => 0,
        ),
      ),
    ),
  );
  $context->condition_mode = 0;
  $export['recent-changes-sidebar'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'user-logged-in';
  $context->description = 'Displays blocks for users who are logged in.';
  $context->tag = '';
  $context->conditions = array(
    'path' => array(
      'values' => array(
        'community' => 'community',
        'community/*' => 'community/*',
        'user/*' => 'user/*',
        '~user/login' => '~user/login',
        'forums/*' => 'forums/*',
      ),
    ),
  );
  $context->reactions = array(
    'block' => array(
      'blocks' => array(
        'views-user_profile_box-block_1' => array(
          'module' => 'views',
          'delta' => 'user_profile_box-block_1',
          'region' => 'sidebar_right',
          'weight' => 10,
        ),
      ),
    ),
  );
  $context->condition_mode = 1;

  // Translatables
  // Included for use with string extractors like potx.
  t('Displays blocks for users who are logged in.');
  $export['user-logged-in'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'user-logged-in-forums-home-page';
  $context->description = 'Displays blocks for users who are logged in and on the forums home page.';
  $context->tag = '';
  $context->conditions = array(
    'path' => array(
      'values' => array(
        'forums' => 'forums',
      ),
    ),
  );
  $context->reactions = array();
  $context->condition_mode = 1;

  // Translatables
  // Included for use with string extractors like potx.
  t('Displays blocks for users who are logged in and on the forums home page.');
  $export['user-logged-in-forums-home-page'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'user-logged-out';
  $context->description = 'Displays blocks for anonymous uses.';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array();
  $context->condition_mode = 0;

  // Translatables
  // Included for use with string extractors like potx.
  t('Displays blocks for anonymous uses.');
  $export['user-logged-out'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'viewing-book';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['viewing-book'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'viewing-developer-center';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'context' => array(
      'values' => array(
        'menu-active-quickstarts' => 'menu-active-quickstarts',
      ),
    ),
    'menu' => array(
      'values' => array(
        'documentation' => 'documentation',
        'https://access.redhat.com/knowledge/docs/en-US/OpenShift/2.0/html/User_Guide/index.html' => 'https://access.redhat.com/knowledge/docs/en-US/OpenShift/2.0/html/User_Guide/index.html',
        'node/10295' => 'node/10295',
        'node/10863' => 'node/10863',
        'node/10866' => 'node/10866',
        'node/11066' => 'node/11066',
        'node/11129' => 'node/11129',
        'node/11158' => 'node/11158',
        'node/11327' => 'node/11327',
        'node/11422' => 'node/11422',
        'node/12009' => 'node/12009',
        'node/12010' => 'node/12010',
        'node/12036' => 'node/12036',
        'node/12037' => 'node/12037',
        'node/12038' => 'node/12038',
        'node/12255' => 'node/12255',
        'node/12420' => 'node/12420',
        'node/14083' => 'node/14083',
        'node/5085' => 'node/5085',
        'node/5475' => 'node/5475',
        'node/9445' => 'node/9445',
        'node/9525' => 'node/9525',
        'quickstarts' => 'quickstarts',
        'videos' => 'videos',
      ),
    ),
    'node' => array(
      'values' => array(
        'quickstart' => 'quickstart',
        'video' => 'video',
      ),
      'options' => array(
        'node_form' => '1',
      ),
    ),
    'path' => array(
      'values' => array(
        'developers/extend' => 'developers/extend',
        'developers/cartridge-authors-guide' => 'developers/cartridge-authors-guide',
        'developers/mysql' => 'developers/mysql',
        'developers/perl' => 'developers/perl',
        'developers/postgresql' => 'developers/postgresql',
      ),
    ),
  );
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['viewing-developer-center'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'viewing-hierarchy';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['viewing-hierarchy'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'viewing-page';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array(
    'path' => array(
      'values' => array(
        '*' => '*',
        '~admin' => '~admin',
        '~admin/*' => '~admin/*',
        '~user' => '~user',
      ),
    ),
    'user_page' => array(
      'values' => array(
        'form' => 'form',
        'view' => 'view',
      ),
      'options' => array(
        'mode' => 'all',
      ),
    ),
  );
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['viewing-page'] = $context;

  $context = new stdClass;
  $context->disabled = FALSE; /* Edit this to true to make a default context disabled initially */
  $context->api_version = 3;
  $context->name = 'viewing-poll';
  $context->description = '';
  $context->tag = '';
  $context->conditions = array();
  $context->reactions = array();
  $context->condition_mode = 0;
  $export['viewing-poll'] = $context;

  return $export;
}
