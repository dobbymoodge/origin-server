<?php
/*
 * Allows us to keep the theme registry cleared during build.  This will affect .local and .vmldev
 * so if you want to use this capability make sure your servername has (.local - ex. cbi.local) for
 * this to work or modify to fit your local install.
 */

//if (preg_match('/(vmldev\.com|local)$/', $_SERVER['SERVER_NAME'])) {
//  drupal_rebuild_theme_registry();
//}

// Add the CSS for the vote up/down module on all pages.
// This eliminates a bug with AJAX comments and vote up/down not working together.

function openshift_theme() {
  return array(
    'comment_form' => array('arguments' => array(
      'form' => NULL,
      'edit' => NULL,
    )),
    'search_form' => array(
      'arguments' => array('form' => NULL),
    ),
    'user_login' => array(
      'template' => 'user-login',
      'arguments' => array('form' => NULL),
    ),
  );
}

function openshift_preprocess_user_login( &$variables ) {
  unset($variables['form']['name']['#description']);
  unset($variables['form']['pass']['#description']);
  $variables['form']['name']['#attributes'] = array('class' => 'input-max');
  $variables['form']['pass']['#attributes'] = array('class' => 'input-max', 'autocomplete' => 'off');
  $variables['form']['submit']['#attributes'] = array('class' => 'btn-block-phone btn-large');
  $variables['form']['submit']['#value'] = 'Sign In';
  $variables['form']['name']['#important'] = true;
  $variables['form']['pass']['#important'] = true;
  #print_r($variables['form']);
  $variables['rendered'] = drupal_render($variables['form']);
}

function openshift_comment_form($form, $edit=array()) {
  global $user;
  if ($user->uid && (empty($edit['cid']) || !user_access('administer comments'))) {
    $form['_author'] = NULL;
  }
  return drupal_render($form);
}

function openshift_imagecache($presetname, $path, $alt = '', $title = '', $attributes = NULL, $getsize = TRUE) {
	/* Begin Override */
	// Don't display a user's email address in the ALT tag.
	$alt = '';
	/* End Override */
  // Check is_null() so people can intentionally pass an empty array of
  // to override the defaults completely.
  if (is_null($attributes)) {
    $attributes = array('class' => 'imagecache imagecache-'. $presetname);
  }
  if ($getsize && ($image = image_get_info(imagecache_create_path($presetname, $path)))) {
    $attributes['width'] = $image['width'];
    $attributes['height'] = $image['height'];
  }

  $attributes = drupal_attributes($attributes);
  $imagecache_url = imagecache_create_url($presetname, $path);
  return '<img src="'. $imagecache_url .'" alt="'. check_plain($alt) .'" title="'. check_plain($title) .'" '. $attributes .' />';
}


function openshift_preprocess_page(&$vars) {
  //menu_set_active_menu_name('community_navigation');
  //drupal_set_header('X-UA-Compatible', 'IE=edge,chrome=1');

  // Setup variables to display the correct banners on node/add/discussion pages.
  if (arg(0) == 'node' && arg(1) == 'add' && arg(2) == 'discussion') {
    switch (arg(3)) {
      case 'openshift':
        $vars['forum']['new-topic'] = TRUE;
        break;
      case 'flex':
        $vars['forum']['new-topic'] = TRUE;
        break;
      case 'news-and-announcements':
        $vars['forum']['new-topic'] = TRUE;
        break;
      default:
        $vars['forum']['new-topic'] = FALSE;
    }
  }
  // Hackish way to detect the forums but right now the page
  // vars aren't being set properly. 404s?
  if(in_array($vars['node']->type, array('discussion', 'group'))) {
    list($vars['product']) = explode(' ', trim($vars['section_title']));
  }

  // Work around http://drupal.org/node/279767 where admin_menu
  // overrides the link due to duplicate hooks
  $user_title = $user->uid == 0 ? 'Log In to the Community' : 'My Account';
  if (stripos($vars['head_title'],'icon_users.png')) {
    $vars['head_title'] = $user_title.' | ' . variable_get('site_name', '');
  }
  if (stripos($vars['title'],'icon_users.png')) {
    $vars['title'] = $user_title;
  }

  // surface the highest navigation node
  // FIXME replace with better integration with drupal site nav and taxonomies
  $vars['heading'] = _openshift_heading($vars);
  if ($vars['is_front']) {
    $vars['body_classes'] .= ' home2';
  }

  _openshift_whitelist_css($vars);

  #print "<!-- ";
  #print_r(menu_get_active_trail());
  #print_r($vars);
  #print " -->";
}

function _openshift_page_arguments($item) {
  $args = $item['page_arguments'];
  if ($args && $args[0]) {
    return $args[0];
  }
  return NULL;
}

/* whitelist */
function _openshift_whitelist_css(&$vars)
{
  drupal_add_css(drupal_get_path('module', 'vud') .'/widgets/updown/updown.css', 'module', 'all', FALSE);

  $css = drupal_add_css();
  foreach ( $css['all']['module'] as $stylesheet => $val ) {
    if (preg_match("/\/(defaults|system|system-menus)\\.css/", $stylesheet)) {
      unset($css['all']['module'][$stylesheet]);
    }
  }
  $vars['styles'] = drupal_get_css($css);

  $scripts = drupal_add_js();
  #print_r($scripts);
  unset($scripts['core']['misc/jquery.js']);
  /*drupal_add_js(drupal_get_path('theme', 'openshift') . '/js/flag.js', 'theme');
  unset($scripts['module']['sites/all/modules/contrib/flag/theme/flag.js']);*/
  $vars['scripts'] = drupal_get_js('header', $scripts);
}

function openshift_social_sharing($url, $title = NULL) {
  $share_url = preg_replace('%([^:])([/]{2,})%', '\\1/', url($url, array('absolute' => TRUE)));
  if (isset($title)) {
    $tweet_text = $title . ' ' . $share_url . ' by @openshift';
  } else {
    $tweet_text = $share_url . ' by @openshift';
  }
  $share_url = urlencode($share_url);
  $tweet_text = urlencode($tweet_text);
  return '<div class="social-sharing">'.
      '<a target="_blank" href="http://twitter.com/intent/tweet?text='. $tweet_text .'" aria-hidden="true" data-icon="&#xee04;" title="Post to Twitter"> </a>'.
      '<a target="_blank" href="http://www.facebook.com/sharer.php?u='. $share_url .'&t='. urlencode($title) .'" aria-hidden="true" data-icon="&#xee05;" title="Post to Facebook"> </a>'.
      '<a target="_blank" href="https://plus.google.com/share?url='. $share_url .'" aria-hidden="true" data-icon="&#xee06;" title="Post to Google+"> </a>'.
    '</div>';
}

function openshift_wrap_region($s) {
  $is_row = strpos($s, "<!--row-fluid-->"); 
  if ($is_row) { 
    print "<div class=\"row-fluid\">"; 
  } 
  print $s; 
  if ($is_row) { 
    print "</div>"; 
  } 
}

function openshift_pager($tags = array(), $limit = 10, $element = 0, $parameters = array(), $quantity = 9) {
  global $pager_page_array, $pager_total;

  // Calculate various markers within this pager piece:
  // Middle is used to "center" pages around the current page.
  $pager_middle = ceil($quantity / 2);
  // current is the page we are currently paged to
  $pager_current = $pager_page_array[$element] + 1;
  // first is the first page listed by this pager piece (re quantity)
  $pager_first = $pager_current - $pager_middle + 1;
  // last is the last page listed by this pager piece (re quantity)
  $pager_last = $pager_current + $quantity - $pager_middle;
  // max is the maximum page number
  $pager_max = $pager_total[$element];
  // End of marker calculations.

  // Prepare for generation loop.
  $i = $pager_first;
  if ($pager_last > $pager_max) {
    // Adjust "center" if at end of query.
    $i = $i + ($pager_max - $pager_last);
    $pager_last = $pager_max;
  }
  if ($i <= 0) {
    // Adjust "center" if at start of query.
    $pager_last = $pager_last + (1 - $i);
    $i = 1;
  }
  // End of generation loop preparation.

  $li_first = theme('pager_first', t('←'), $limit, $element, $parameters);
  $li_previous = theme('pager_previous', t('«'), $limit, $element, 1, $parameters);
  $li_next = theme('pager_next', t('»'), $limit, $element, 1, $parameters);
  $li_last = theme('pager_last', t('→'), $limit, $element, $parameters);

  if ($pager_total[$element] > 1) {
    if ($li_first) {
      $items[] = array(
        'data' => $li_first,
      );
    }
    if ($li_previous) {
      $items[] = array(
        'data' => $li_previous,
      );
    }

    // When there is more than one page, create the pager list.
    if ($i != $pager_max) {
      if ($i > 1) {
        $items[] = array(
          'class' => 'disabled', 
          'data' => '<a>...</a>',
        );
      }
      // Now generate the actual pager piece.
      for (; $i <= $pager_last && $i <= $pager_max; $i++) {
        if ($i < $pager_current) {
          $items[] = array(
            'data' => theme('pager_previous', $i, $limit, $element, ($pager_current - $i), $parameters),
          );
        }
        if ($i == $pager_current) {
          $items[] = array(
            'class' => 'active', 
            'data' => theme('pager_link', $i, $limit, $element, $i, $parameters),
          );
        }
        if ($i > $pager_current) {
          $items[] = array(
            'data' => theme('pager_next', $i, $limit, $element, ($i - $pager_current), $parameters),
          );
        }
      }
      if ($i < $pager_max) {
        $items[] = array(
          'class' => 'disabled', 
          'data' => '<a>...</a>',
        );
      }
    }
    // End generation.
    if ($li_next) {
      $items[] = array(
        'data' => $li_next,
      );
    }
    if ($li_last) {
      $items[] = array(
        'data' => $li_last,
      );
    }
    return '<div class="pagination">'. theme('item_list', $items, NULL, 'ul') . '</div>';
  }
}

/* FIXME Replace with a better site hierarchy concept which allows heading to be inferred from
 * the last left nav item (community navigation is not visible via get_active_trail because items
 * aren't parented).
 */
function _openshift_heading(&$vars) {
  global $user;
  $page_title = $vars['title'];
  $title = check_plain($page_title);
  $item = end(menu_get_active_trail());
  #print_r($item);
  if ($vars['forum']['new-topic']) {
    $type = 'discussion';
  }
  elseif ($item['path'] == 'node/%' && $item['page_arguments'] && $item['page_arguments'][0]) {
    $node = $item['page_arguments'][0];
    if ($node->nid == 9435) { // developers page
      $type = "developers";
      $title = check_plain($node->title);
    }
    else {
      $type = $node->type;
      $title = check_plain($node->title);
    }
  }
  elseif ($item['path'] == 'comment/reply/%' && $item['page_arguments'] && $item['page_arguments'][0]) {
    $node = $item['page_arguments'][0];
    $type = $node->type;
  }
  elseif ($item['link_path'] == 'user' && $user->uid == 0) {
    $title = '';
  }
  elseif ($item['module'] == 'book' && $vars['node'] && $vars['node']->type == 'book') {
    $node = $vars['node'];
    $data = menu_tree_all_data($item['menu_name']);
    $data = reset($data);
    $title = check_plain($data['link']['title']);
  }
  elseif ($item['link_path']) {
    $type = $item['link_path'];
    if (empty($title)) {
      $title = check_plain($item['title']);
    }
  }
  elseif ($item['path'] == 'developers') {
    $type = 'developers';
  }
  elseif ($item['page_callback'] == 'taxonomy_term_page') {
    if ($term = taxonomy_get_term($item['page_arguments'][0])) {
      if ($term->vid == 4) {
        $title = "QuickStarts Tagged with '". check_plain($term->name) ."'";
        $vars['head_title'] = $title;
      } else {
        $title = "Content Tagged with ". check_plain($term->name);
      }
    } else {
      $title = "Tagged Content";
    }
    $type = '';
  }
  switch ($type) {
  case 'home': $heading = "Overview"; break;
  case 'ideas': $heading = "Vote on Features"; break;
  case 'poll':
  case 'polls': $heading = "Polls"; break;
  case 'wikis': $heading = "Open Source Wiki"; break;
  case 'group':
  case 'groups': $heading = "Forum"; break;
  case 'developers': $heading = NULL; break;
  case 'calendar':
  default:
    $heading = $title;
  }
  return $heading;
}

function openshift_breadcrumb($breadcrumb) {
  if (!empty($breadcrumb) && count($breadcrumb) > 1) {
    #array_shift($breadcrumb);
    return '<div class="breadcrumb">' . implode('<span class="divider"> /</span>', $breadcrumb) . '</div>';
  }
}

function openshift_flat_menu_tree_output($tree) {
  $output = '';
  $items = array();
  foreach ($tree as $data) {
    if (!$data['link']['hidden'] && $data['link']['expanded'] && $data['link']['has_children']) {
      $items[] = $data;
    }
  }
  $num_items = count($items);
  $class = 'span' . (12 / $num_items);
  $output .= '<div class="row-fluid">';
  foreach ($items as $i => $data) {
    $output .= '<nav class="' . $class . '">' . '<header><h3>' . check_plain($data['link']['title']) . '</h3></header>';
    $output .= '<ul class="unstyled">';
    $children = $data['below'];
    foreach ($children as $child) {
      if ($child['link']['hidden']) { continue; }
      $link = $child['link'];
      $output .= '<li>' . l($link['title'], $link['href']) . '</li>';
    }
    $output .= '</ul></nav>';
  }
  $output .= '</div>';
  return $output;
}

function openshift_preprocess_node(&$vars) {
  $path = request_uri();
  $path_parts = explode('/', $path);
  $forum = $path_parts[2];

  switch ($forum) {
    case 'openshift':
      $vars['forum']['id'] = 'openshift';
      $vars['forum']['title'] = 'OpenShift Forum';
      break;
    case 'flex':
      $vars['forum']['id'] = 'flex';
      $vars['forum']['title'] = 'Flex Forum';
      break;
    case 'news-and-announcements':
      $vars['forum']['id'] = 'news-and-announcements';
      $vars['forum']['title'] = 'News and Announcements';
      break;
    default:
      $vars['forum'] = NULL;
  }

  // Allow node taxonomy theming
  if (arg(0) == 'taxonomy') {
     $suggestions = array(
       'node-taxonomy',
       'node-'.$vars['type'].'-taxonomy'
     );
     $vars['template_files'] = array_merge($vars['template_files'], $suggestions);
  }

  // Theme the links appended to each discussion node.
  _openshift_theme_subscription_links($vars['links']);
}

function _openshift_theme_subscription_links(&$links) {
  $links = str_replace('<em>', '', $links);
  $links = str_replace('</em>', '', $links);
  $links = str_replace('Subscribe to: This post', 'Subscribe to this', $links);
  $links = str_replace('Unsubscribe from: This post', 'Unsubscribe from this', $links);
  $links = str_replace('Subscribe to: Discussion posts in', 'Subscribe to ', $links);
  $links = str_replace('Unsubscribe from: Discussion posts in', 'Unsubscribe from ', $links);
  $links = str_replace('Subscribe to: Posts by ', 'Subscribe to ', $links);
  $links = str_replace('Unsubscribe from: Posts by ', 'Unsubscribe from ', $links);
}

function openshift_form_element($element, $value) {
  // This is also used in the installer, pre-database setup.
  $t = get_t();

  $output = '<div class="control-group';
  if (!empty($element['#important'])) {
    $output .= ' control-group-important';
  }
  $output .= '"';
  if (!empty($element['#id'])) {
    $output .= ' id="'. $element['#id'] .'-wrapper"';
  }
  $output .= ">\n";
  $required = !empty($element['#required']) ? '<span class="form-required" title="'. $t('This field is required.') .'">*</span>' : '';

  if (!empty($element['#title'])) {
    $title = $element['#title'];
    if (!empty($element['#id'])) {
      $output .= ' <label for="'. $element['#id'] .'">'. $t('!title: !required', array('!title' => filter_xss_admin($title), '!required' => $required)) ."</label>\n";
    }
    else {
      $output .= ' <label>'. $t('!title: !required', array('!title' => filter_xss_admin($title), '!required' => $required)) ."</label>\n";
    }
  }

  $output .= " <div class='controls'>";
  $output .= $value;

  if (!empty($element['#description'])) {
    $output .= ' <div class="help-block">'. $element['#description'] ."</div>\n";
  }
  if (!empty($element['#additional'])) {
    $output .= $element['#additional'];
  }
  
  $output .= "</div>";

  $output .= "</div>\n";

  return $output;
}

function openshift_server_url() {
  return redhat_sso_server_url();
}

function openshift_assets_url() {
  $url = variable_get('openshift_assets_url', '');
  if (empty($url)) {
    $asset_version = variable_get('openshift_assets_version', '');
    if (empty($asset_version)) {
      $url = openshift_server_url() . '/app/assets';
    } 
    else {
      $url = openshift_server_url() . '/app/assets-' . $asset_version;
    }
  }
  return $url;
}

function openshift_button($element) {
  // Make sure not to overwrite classes.
  $id = $element['#id'];
  $class = 'btn';
  if ($id) {
    if (openshift_ends_with($id, '-submit')) {
      $class .= ' btn-primary';
    }
    else if (openshift_ends_with($id, '-delete')) {
      $class .= ' btn-danger';
    }
  }
  if (isset($element['#attributes']['class'])) {
    $element['#attributes']['class'] = $class . ' form-'. $element['#button_type'] .' '. $element['#attributes']['class'];
  }
  else {
    $element['#attributes']['class'] = $class . ' form-'. $element['#button_type'];
  }

  return '<input type="submit" '. (empty($element['#name']) ? '' : 'name="'. $element['#name'] .'" ') .'id="'. $element['#id'] .'" value="'. check_plain($element['#value']) .'" '. drupal_attributes($element['#attributes']) ." />\n";
}

function openshift_radio($element) {
  _form_set_class($element, array('form-radio'));
  $output = '<input type="radio" ';
  $output .= 'id="'. $element['#id'] .'" ';
  $output .= 'name="'. $element['#name'] .'" ';
  $output .= 'value="'. $element['#return_value'] .'" ';
  $output .= (check_plain($element['#value']) == $element['#return_value']) ? ' checked="checked" ' : ' ';
  $output .= drupal_attributes($element['#attributes']) .' />';
  if (!is_null($element['#title'])) {
    $output = '<label class="radio" for="'. $element['#id'] .'">'. $output .' '. $element['#title'] .'</label>';
  }

  unset($element['#title']);
  return theme('form_element', $element, $output);
}

function openshift_checkbox($element) {
  _form_set_class($element, array('form-checkbox'));
  $checkbox = '<input ';
  $checkbox .= 'type="checkbox" ';
  $checkbox .= 'name="'. $element['#name'] .'" ';
  $checkbox .= 'id="'. $element['#id'] .'" ' ;
  $checkbox .= 'value="'. $element['#return_value'] .'" ';
  $checkbox .= $element['#value'] ? ' checked="checked" ' : ' ';
  $checkbox .= drupal_attributes($element['#attributes']) .' />';

  if (!is_null($element['#title'])) {
    $checkbox = '<label class="checkbox" for="'. $element['#id'] .'">'. $checkbox .' '. $element['#title'] .'</label>';
  }

  unset($element['#title']);
  return theme('form_element', $element, $checkbox);
}

function openshift_preprocess_search_block_form(&$vars) {
//  $vars['form']['text']['#class'] = 'input-small search-query';
//  $vars['search']['text'] = drupal_render($vars['form']['text']);

  $vars['form']['submit']['#class'] = 'btn';
  $vars['search']['submit'] = drupal_render($vars['form']['submit']);

  $vars['form']['search_block_form']['#attributes'] = array('class' => 'form-search');
  unset($vars['form']['search_block_form']['#title']);
  unset($vars['form']['search_block_form']['#printed']);
  $vars['search']['search_block_form'] = drupal_render($vars['form']['search_block_form']);

  // Collect all form elements to print entire form
  $vars['search_form'] = implode($vars['search']);
}

function openshift_user_guide_url() {
  return '/user-guide';
}

function openshift_search_form($form) {
  #print '<pre>'. check_plain(print_r($form, 1)) .'</pre>';
  $form['basic']['inline']['#suffix'] = '</div>'.
    '<div class="alert alert-info">Note: This search does not search the <a target="_blank" href="'.openshift_user_guide_url().'">OpenShift user guide</a></div>';
  $submit = drupal_render($form['basic']['inline']['submit']);
  unset($form['basic']['inline']['submit']);
  $form['basic']['inline']['keys']['#additional'] = ' '.$submit;
  return drupal_render($form);
}

function openshift_preprocess_search_result(&$vars) {
  if ($vars['type'] == 'user'){
    $vars['title'] = strip_email($vars['title']);
  }
}

function openshift_filter_tips($tips, $long = FALSE, $extra = '') {
	$output = '';
	if ($long) {
		$output .= '<bold>' . t('Syntax highlighting of source code can be enabled with the following tags:') . '</bold>';
		$output .= '<ul><li>' . t('Generic syntax highlighting tags: "<code>&ltcode&gt</code>", "<code>&ltblockcode&gt</code>".') . '</li></ul>';
		$output .= '<h4>' . t('For language specific syntax highlighting tags:') . '</h4>';
		$output .= '<table class="table table-bordered table-striped"><thead><tr>' . '<th>Code</th>' . '<th>Syntax</th>' . '</tr></thead>';
		$output .= '<tbody>' . '<tr><td><code>&ltc&gt</code></td>' . '<td>Used for C code</td></tr>';
		$output .= '<tr><td><code>&ltcpp&gt</code>' . '<td>Used for C++ code</td></tr>';
		$output .= '<tr><td><code>&ltdrupal5&gt</code>' . '<td>Used for Drupal 5 code</td></tr>';
		$output .= '<tr><td><code>&ltdrupal6&gt</code>' . '<td>Used for Drupal 6 code</td></tr>';
		$output .= '<tr><td><code>&ltjava&gt</code>' . '<td>Used for Java code</td></tr>';
		$output .= '<tr><td><code>&ltjavascript&gt</code>' . '<td>Used for Javascript code</td></tr>';
		$output .= '<tr><td><code>&ltphp&gt</code>' . '<td>Used for PHP code</td></tr>';
		$output .= '<tr><td><code>&ltpython&gt</code>' . '<td>Used for Python code</td></tr>';
		$output .= '<tr><td><code>&ltruby&gt</code>' . '<td>Used for Ruby code</td></tr>' . '</tbody></table>';

		$output .= '<p>' . t('The language for the generic syntax highlighting tags can be specified with one of the attribute(s):<em>type,lang,language,class</em>. The possible values are:') . '</p>';

		$output .= '<ul><li>' . t('"<code>c</code>" for C code') . '</li>';
		$output .= '<li>' . t('"<code>cpp</code>" for C++ code') . '</li>';
		$output .= '<li>' . t('"<code>drupal5</code>" for Drupal 5 code') . '</li>';
		$output .= '<li>' . t('"<code>drupal6</code>" for Drupal 6 code') . '</li>';
		$output .= '<li>' . t('"<code>java</code>" for Java code') . '</li>';
		$output .= '<li>' . t('"<code>javascript</code>" for javascript code') . '</li>';
		$output .= '<li>' . t('"<code>php</code>" for PHP code') . '</li>';
		$output .= '<li>' . t('"<code>python</code>" for Pyhton code') . '</li>';
		$output .= '<li>' . t('"<code>ruby</code>" for Ruby code') . '</li></ul>';

		$output .= '<h3>' . t('Options and Tips') . '</h3>';
		$output .= '<ul><li>' . t('The supported tag styles are <code>&ltfoo&gt</code>, <code>[foo]</code>') . '</li>';
		$output .= '<li>' .  t('Line numbering can be enabled/disabled with the attribute "linenumbers". Possible values are: "off" for no line numbers, "normal" for normal line numbers and "fancy" for fancy line numbers (every nth line number highlighted). The start line number can be specified with the attribute "start", which implicitly enables normal line numbering. For fancy line numbering the interval for the highlighted line numbers can be specified with the attribute "fancy", which implicitly enables fancy line numbering.') . '</li>';
		$output .= '<li>' . t('If the source code between the tags contains a newline (e.g. immediatly after the opening tag), the highlighted source code will be displayed as a code block. Otherwise it will be displayed inline.') . '</li>';
		$output .= '<li>' . t('A title can be added to a code block with the attribute "title".') . '</li></ul>';

		$output .= '<h3>' . t('Defaults') . '</h3>';
		$output .= '<ul><li>' . t('Default highlighting mode for generic syntax highlighting tags: when no language attribute is specified, no syntax highlighting will be done.');
		$output .= '<li>' . t('Default line numbering: no line numbers.') . '</li></ul>';

		$output .= '<h3>' . t('Examples') . '</h3>';
		$output .= '<table class="table table-bordered table-striped"><thead><tr>' . '<th>You Type</th>' . '<th>You Get</th>' . '</tr></thead>';
		$output .= '<tbody>' . '<tr><td><pre>&ltcode&gtfoo = "bar";&lt/code&gt</pre> ' . '<td>Inline code with the default synctax highlighting mode</td></tr>';
		$output .= '<tr><td><pre>&ltcode&gt;</br>foo = "bar"</br>baz = "foz";</br>&ltcode&gt</pre>' . '<td class="text-center">Code block with the default syntax highlighting mode.</td></tr>';
		$output .= '<tr><td><pre>&ltcode lang="c" linenumbers="normal"&gt</br>foo = "bar";</br>baz = "foz";&lt/code&gt</br></pre></td>' . '<td class="text-center">Code block with syntax highlighting for C source code and normal line numbers.</td></tr>';
		$output .= '<tr><td><pre>&ltcode language="java" start="23" fancy="7"&gt</br>foo = "bar"</br> baz = "foz";</br>&lt/code&gt</pre></td>' . '<td class="text-center">Code block with syntax highlighting for Java source code,line numbers starting from 23 and highlighted line numbers every 7th line.</td></tr>';
		$output .= '<tr><td><pre>&ltc&gt</br>foo = "bar";</br>baz = "foz";</br>&lt/c&gt</pre></td>' . '<td class="text-center">Code block with syntax highlighting for C source code.</td></tr>';
		$output .= '<tr><td><pre>&ltc start="23" fancy="7"&gt</br>foo = "bar";</br>baz = "foz";&ltc&gt</pre>' . '<td class="text-center">Code block with syntax highlighting for C source code,line numbers starting from 23 and highlighted line numbers every 7th line.' . '</tbody></table>';

		$output .= '<h3>' . t('Quick Tips') . '</h3>';
		$output .= '<ul><li>' . t('Two or more spaces at a line&#039s end = Line break.') . '</li>';
		$output .= '<li>' . t('*Single asterisks* or _single underscores_ = <em>Emphasis</em>.') . '</li>';
		$output .= '<li>' . t('**Double** or __double__ = <strong>Strong</strong>.') . '</li>';
		$output .= '<li>' . t('This is [a link](http://the.link.example.com "The optional title text")') . '</li></ul>';


		$output .= '<p>' . t('For complete details on the Markdown syntax, see the <a href="http://daringfireball.net/projects/markdown/syntax">Markdown Documentation</a> and <a href="http://michelf.com/projects/php-markdown/extra/">Markdown Extra Documentation</a> for tables, footnotes, and more. Web page addresses and e-mail addresses turn into links automatically.</br>Allowed HTML tags: &lta&gt &ltem&gt &ltstrong&gt &ltcite&gt &ltcode&gt &ltul&gt &ltol&gt &ltli&gt &ltdl&gt &ltdt&gt &ltdd&gt &ltp&gt &ltbr&gt &ltimg&gt &ltdiv&gt &ltblockcode&gt &ltpre&gt &lth1&gt &lth2&gt &lth3&gt &lth4&gt &lth5&gt &lth6&gt') . '</p>';
	}
	return $output;
}
// function openshift_filter_tips($tips, $long = FALSE, $extra = '') {
//   $output = '';

//   $multiple = count($tips) > 1;
//   if ($multiple) {
//     $output = '<h2>' . t('Input Formats') .':'. '</h2>';
//   }

//   if (count($tips)) {
//     if ($multiple) {
//       $output .= '<dl>';
//     }
//     foreach ($tips as $name => $tiplist) {
//       if ($multiple) {
//         $output .= '<li>';
//         $output .= '<strong>'. $name .'</strong>:<br />';
//       }

//       if (count($tiplist) > 0) {
//         $output .= '<ul class="tips unstyled">';
//         foreach ($tiplist as $tip) {
//           $output .= '<li'. ($long ? ' id="filter-'. str_replace("/", "-", $tip['id']) .'">' : '>') . $tip['tip'] .'</li>';
//         }
//         $output .= '</ul>';
//       }

//       if ($multiple) {
//         $output .= '</li>';
//       }
//     }
//     if ($multiple) {
//       $output .= '</ul>';
//     }
//   }

//   return $output;
// }

function openshift_links($links, $attributes = array('class' => 'links')) {
  
  // Begin Override
  // Remove the statistics counter on every node.
  if ($links['statistics_counter']) {
  	unset($links['statistics_counter']);
  }
  // End Override
	
  global $language;
  $output = '';

  if (count($links) > 0) {

    /*$attributes['class'] = 'btn-group ' . (isset($attributes['class']) ? $attributes['class'] : '');*/
    $output = '<div'. drupal_attributes($attributes) .'>';

    $num_links = count($links);
    $i = 1;

    foreach ($links as $key => $link) {
      $class = $key;

      // Add first, last and active classes to the list of links to help out themers.
      if ($i == 1) {
        $class .= ' first';
      }
      if ($i == $num_links) {
        $class .= ' last';
      }
      if (isset($link['href']) && (empty($link['language']) || $link['language']->language == $language->language)) {
        $class .= ' active';
      }
      //$output .= '<li'. drupal_attributes(array('class' => $class)) .'>';

      if (isset($link['href'])) {
        if (!isset($link['attributes'])) {
          $link['attributes'] = array();
        }
        $link_attributes = $link['attributes'];
        $link['attributes']['class'] = /*'btn '.*/$class;// . (isset($link_attributes['class']) ? $link_attributes['class'] : '');
        // Pass in $link as $options, they share the same keys.
        $output .= l($link['title'], $link['href'], $link);
      }
      else if (!empty($link['title'])) {
        // Some links are actually not links, but we wrap these in <span> for adding title and class attributes
        if (empty($link['html'])) {
          $link['title'] = check_plain($link['title']);
        }
        $span_attributes = '';
        if (isset($link['attributes'])) {
          $span_attributes = drupal_attributes($link['attributes']);
        }
        $output .= $link['title']; //.= '<span'. $span_attributes .'>'. $link['title'] .'</span>';
      }

      $i++;
      //$output .= "</li>\n";
    }

    $output .= '</div>';
  }

  return $output;
}


function openshift_status_messages($display = NULL) {
  $output = '';
  foreach (drupal_get_messages($display) as $type => $messages) {
    $output .= "<div class=\"messages $type\">\n";
    if (count($messages) > 1) {
      foreach ($messages as $message) {
        $output .= " <div class=\"alert alert-$type\">" . $message . "</div>";
      }
    }
    else {
      $output .= " <div class=\"alert alert-$type\">" . $messages[0] . "</div>";
    }
    $output .= "</div>\n";
  }
  return $output;
}

function openshift_menu_local_tasks() {
  $output = '';

  if ($primary = menu_primary_local_tasks()) {
    $output .= "<ul class=\"nav nav-pills primary\">\n". $primary ."</ul>\n";
  }
  if ($secondary = menu_secondary_local_tasks()) {
    $output .= "<ul class=\"nav nav-tabs secondary\">\n". $secondary ."</ul>\n";
  }

  return $output;
}

function openshift_preprocess_views_view(&$vars) {

  #if ($vars['view']->name === 'knowledge_base') {
  #  drupal_add_js(drupal_get_path('theme', 'redhat') .'/js/redhat.js', 'theme');
  #}
  
  // We are displaying a thread list from a group.
  if ($vars['view']->name === 'og_ghp_thread_list') {
    
 	// Pass forum information to the view.
    $path = arg(0) .'/'. arg(1);
    switch ($path) {
      case 'node/1':
      	$vars['forum']['nid'] = '1';
      	$vars['forum']['alias'] = 'openshift';
        $vars['forum']['heading'] = 'OpenShift';
        $vars['forum']['description'] = _openshift_get_group_description(arg(1));
        break;
      case 'node/2':
      	$vars['forum']['nid'] = '2';
      	$vars['forum']['alias'] = 'flex';
        $vars['forum']['heading'] = 'Flex';
        $vars['forum']['description'] = _openshift_get_group_description(arg(1));
        break;
      case 'node/3':
      	$vars['forum']['nid'] = '3';
      	$vars['forum']['alias'] = 'news-and-announcements';
        $vars['forum']['heading'] = 'News and Announcements';
        $vars['forum']['description'] = _openshift_get_group_description(arg(1));
        break;
      default:
        $vars['forum'] = NULL;
    }
    $feed = base_path() . 'forums/feeds/' . $vars['forum']['nid'];
    $vars['forum']['feed'] = theme_feed_icon($feed, 'Subscribe to the RSS feed for this forum');
  }
}

function _openshift_get_group_description($node_id) {
  $group_description = db_result(db_query("SELECT og_description FROM {og} as d
    WHERE d.nid = %d", array($node_id)));
  return $group_description;
}

function openshift_preprocess_user_profile(&$vars) {

  global $user;
  $sid = db_result(db_query("SELECT n.sid FROM {notifications} as n
    LEFT JOIN {notifications_fields} AS nf ON (n.sid = nf.sid)
    WHERE n.type = 'author' AND n.uid = %d AND nf.value = %d", array($user->uid, $vars['account']->uid)));
  $vars['sid'] = $sid;
}

function strip_email($username) {
  return $username;
}

function readabledate($enterdate) {
  $newdate = date("l, F j, Y", $enterdate);
  return $newdate;
}

function openshift_date_all_day_label() {
    return '';
}

function openshift_starts_with($s, $substr)
{
    $length = strlen($substr);
    return (substr($s, 0, $length) === $substr);
}

function openshift_ends_with($s, $substr)
{
    $length = strlen($substr);
    $start  = -1 * $length;
    return (substr($s, $start) === $substr);
}

function openshift_primary_link_custom_block($path) {
  $menuMap = variable_get("megamenu_custom_blocks", array());
  $block = array();
  if(is_array($menuMap) && $menuMap[$path]) {
    $mockedBlock = (object)array('module'=>'block', 'delta'=>$menuMap[$path], 'cache'=>BLOCK_CACHE_GLOBAL);
    if(($cid = _block_get_cache_id($mockedBlock)) && ($cache = cache_get($cid, 'cache_block'))) {
      $block = $cache->data;
    }
    else {
      $block = module_invoke($mockedBlock->module, 'block', 'view', $mockedBlock->delta);
      if (isset($cid)) {
        cache_set($cid, $block, 'cache_block', CACHE_TEMPORARY);
      }
    }
  }
  return $block;
}

function openshift_primary_link_megamenu($link, $visibleChildren) {
  $path = url($link['href']);
  $block = openshift_primary_link_custom_block($path);
  if($block['content']) {
    return $block['content'];
  }
  else if(!empty($visibleChildren)){
    $content = '<div class="dropdown-menu dropdown-menu-mega"><ul class="nav nav-list">';
    foreach( $visibleChildren as $key=>$child) {
      $sublink = $child["link"];                                 
      $sublink['options']['html'] = TRUE;
      unset($sublink['options']['attributes']['title']);
      $content .= '<li>' . l($sublink['title'], $sublink['href'], $sublink['options']) . '</li>';
    }
    return $content . '</ul></div>';
  }
}

/*
 * Source: http://drupalcode.org/project/menu_block.git/blob_plain/refs/heads/6.x-2.x:/menu_block.module
 * function menu_tree_build($config)
 */
function openshift_menu_tree_build($config) {
  // Retrieve the active menu item from the database.
  if ($config['menu_name'] == MENU_TREE__CURRENT_PAGE_MENU) {
    // Retrieve the list of available menus.
    $menu_order = variable_get('menu_block_menu_order', array('primary-links' => '', 'secondary-links' => ''));

    // Check for regular expressions as menu keys.
    $patterns = array();
    foreach (array_keys($menu_order) as $pattern) {
      if ($pattern[0] == '/') {
        $patterns[$pattern] = NULL;
      }
    }

    // Retrieve all the menus containing a link to the current page.
    $result = db_query("SELECT menu_name FROM {menu_links} WHERE link_path = '%s'", $_GET['q'] ? $_GET['q'] : '<front>');
    while ($item = db_fetch_array($result)) {
      // Check if the menu is in the list of available menus.
      if (isset($menu_order[$item['menu_name']])) {
        // Mark the menu.
        $menu_order[$item['menu_name']] = MENU_TREE__CURRENT_PAGE_MENU;
      }
      else {
        // Check if the menu matches one of the available patterns.
        foreach (array_keys($patterns) as $pattern) {
          if (preg_match($pattern, $item['menu_name'])) {
            // Mark the menu.
            $menu_order[$pattern] = MENU_TREE__CURRENT_PAGE_MENU;
            // Store the actual menu name.
            $patterns[$pattern] = $item['menu_name'];
          }
        }
      }
    }
    // Find the first marked menu.
    $config['menu_name'] = array_search(MENU_TREE__CURRENT_PAGE_MENU, $menu_order);
    // If a pattern was matched, use the actual menu name instead of the pattern.
    if (!empty($patterns[$config['menu_name']])) {
      $config['menu_name'] = $patterns[$config['menu_name']];
    }
    $config['parent_mlid'] = 0;

    // If no menu link was found, don't display the block.
    if (empty($config['menu_name'])) {
      return array();
    }
  }

  // Get the default block name.
  $menu_names = menu_block_get_all_menus();
  menu_block_set_title(t($menu_names[$config['menu_name']]));

  if ($config['expanded'] || $config['parent_mlid']) {
    // Get the full, un-pruned tree.
    $tree = menu_tree_all_data($config['menu_name']);
    // And add the active trail data back to the full tree.
    menu_tree_add_active_path($tree);

    // ADDED
    if ($config['require_active_trail']) {
      $found_active_trail = FALSE;
      foreach (array_keys($tree) as $key) {
        if ($tree[$key]['link']['in_active_trail']) {
          $found_active_trail = TRUE;
          break;
        }
      }
      if (!$found_active_trail) {
        return NULL;
      }
    }
    // END ADDED  
  }
  else {
    // Get the tree pruned for just the active trail.
    $tree = menu_tree_page_data($config['menu_name']);
  }

  // Allow other modules to alter the tree before we begin operations on it.
  $alter_data = &$tree;
  // Also allow modules to alter the config.
  $alter_data['__drupal_alter_by_ref'] = array(&$config);
  drupal_alter('menu_block_tree', $alter_data);

  // Localize the tree.
  if (module_exists('i18nmenu')) {
    i18nmenu_localize_tree($tree);
  }

  // Prune the tree along the active trail to the specified level.
  if ($config['level'] > 1 || $config['parent_mlid']) {
    if ($config['parent_mlid']) {
      $parent_item = menu_link_load($config['parent_mlid']);
      menu_tree_prune_tree($tree, $config['level'], $parent_item);
    }
    else {
      menu_tree_prune_tree($tree, $config['level']);
    }
  }

  // Prune the tree to the active menu item.
  if ($config['follow']) {
    menu_tree_prune_active_tree($tree, $config['follow']);
  }

  // If the menu-item-based tree is not "expanded", trim the tree to the active path.
  if ($config['parent_mlid'] && !$config['expanded']) {
    menu_tree_trim_active_path($tree);
  }

  // Trim the branches that extend beyond the specified depth.
  if ($config['depth'] > 0) {
    menu_tree_depth_trim($tree, $config['depth']);
  }

  // Sort the active path to the top of the tree.
  if ($config['sort']) {
    menu_tree_sort_active_path($tree);
  }

  return $tree;
}

function openshift_menu_tree_block_output($tree, $config) {
  // Render the tree.
  $data = array();
  $data['subject'] = menu_block_get_title($config['title_link'], $config);
  $data['content'] = openshift_menu_block_tree_output($tree, $config);
  if ($data['content']) {
    $hooks = array();
    $hooks[] = 'menu_block_wrapper__' . str_replace('-', '_', $config['delta']);
    $hooks[] = 'menu_block_wrapper__' . str_replace('-', '_', $config['menu_name']);
    $hooks[] = 'menu_block_wrapper';
    $data['content'] = theme($hooks, $data['content'], $config, $config['delta']);
  }

  return $data;
}


function openshift_menu_block_tree_output(&$tree, $config = array(), $nested = 0, $parent = NULL) {
  $output = '';

  // Create context if no config was provided.
  if (empty($config)) {
    $config['delta'] = 0;
    // Grab any menu item to find the menu_name for this tree.
    $menu_item = current($tree);
    $config['menu_name'] = $menu_item['link']['menu_name'];
  }

  $hook_delta = str_replace('-', '_', $config['delta']);
  $hook_menu_name = str_replace('-', '_', $config['menu_name']);

  $items = array();
  foreach (array_keys($tree) as $key) {
    $item = $tree[$key];
    if (!$item['link']['hidden']) {
      $items[$key] = array(
        'link' => $item['link'],
        'below' => !empty($item['below']) ? openshift_menu_block_tree_output($item['below'], $config, $nested + 1, $item) : '',
      );
    }
  }

  $is_drupal_front = drupal_is_front_page();
  $get_q = $_GET['q'];

  $num_items = count($items);

  $i = 1;
  foreach (array_keys($items) as $key) {
    // Render the link.
    $link_class = array();
    $item = $items[$key];
    $link = $item['link'];

    $active = $link['href'] == $get_q || ($link['href'] == '<front>' && $is_drupal_front);
    $in_active_trail = $link['in_active_trail'] || $active;
    $collapsible = $item['below'] && $config['collapsible']['from_depth'] && $link['depth'] >= ($config['collapsible']['from_depth'] + 1);

    if (!empty($link['localized_options']['attributes']['class'])) {
      $link_class[] = $link['localized_options']['attributes']['class'];
    }
    if (!empty($link_class)) {
      $link['localized_options']['attributes']['class'] = implode(' ', $link_class);
    }
    if ($config['hide_titles']) {
      unset($link['localized_options']['attributes']['title']);
    }

    $link = l($link['title'], $link['href'], $link['localized_options']);

    // Render the menu item.
    $extra_class = array();
    if (!empty($link['leaf_has_children'])) {
      $extra_class[] = 'has-children';
    }

    if ($active || $in_active_trail && $config['highlight_active_trail']) { 
      $extra_class[] = 'active';
    }

    if ($collapsible) {
      $extra_class[] = 'collapsible';
      $link = '<a data-target="#m'. $item['link']['mlid'] .'" data-toggle="collapse" class="'. ($in_active_trail ? 'in' : '') .'">Toggle</a>' . $link;
    }

    $output .= '<li class="'. implode(' ', $extra_class).'">' . $link . $item['below'] . '</li>';

    $i++;
  }

  if (!$output) {  
    return ''; 
  }

  $render_classes = ($nested > 0 ? $config['sub_menu_class'] : $config['menu_class']);
  if ($render_classes) {
    $in_active_trail = $parent['link']['in_active_trail'];
    $collapsible = $parent['link']['mlid'] && $nested >= $config['collapsible']['from_depth'];
    if ($collapsible && $in_active_trail) {
      $render_classes = $render_classes . " " . $config['collapsible']['expanded_menu_class'];
    } elseif ($collapsible) {
      $render_classes = $render_classes . " " . $config['collapsible']['collapse_menu_class'];
    }
    return '<ul ' . ($collapsible ? 'id="m'. $parent['link']['mlid'] .'" ' : '') . 'class="'. $render_classes .'">' . $output . '</ul>';
  }

  $hooks = array();
  $hooks[] = 'menu_tree__menu_block__' . $hook_delta;
  $hooks[] = 'menu_tree__menu_block__' . $hook_menu_name;
  $hooks[] = 'menu_tree__menu_block';
  $hooks[] = 'menu_tree';
  return theme($hooks, $output);
}
