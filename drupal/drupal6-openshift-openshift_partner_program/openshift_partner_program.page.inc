<?php

/**
 * @file
 * Page callback functions, validators and submit functions.
 */

/**
 * Callback function for the partner agreement page.
 */
function _openshift_partner_program_tc() {
  drupal_set_title(t('Openshift Partner Program'));
  require 'includes/openshift_partner_program_agreement.inc';
  drupal_add_css(drupal_get_path('module', 'openshift_partner_program') . '/css/openshift_partner_program.css', 'module', 'all', FALSE);
  $form['tc'] = array(
    '#prefix' => '<p>' . t('Please sign the partner agreement to complete your application to the Openshift by Red Hat Partner Program.') . '</p>',
    '#type' => 'textarea',
    '#disabled' => TRUE,
    '#rows' => 20,
    '#default_value' => $openshift_partner_program_agreement,
  );
  $form['control']['print'] = array(
    '#value' => l(t('Print PDF'), drupal_get_path('module', 'openshift_partner_program') . '/includes/RHOpenShift_Certified_Program_20130531_click-through.pdf', array('attributes' => array('target' => 'tc'))),
  );
  $form['control']['ack'] = array(
    '#type' => 'checkbox',
    '#title' => t('Check box to agree to Partner Agreement.'),
    '#required' => TRUE,
  );
  $form['questions'] = array(
    '#value' => '<p>' . t('Questions? Email ') . l(t('openshift-partners@redhat.com'), 'mailto:openshift-partners@redhat.com') . '</p>',
  );
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}

/**
 * Validation function for partner agreement page.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_tc_validate($form, &$form_state) {
  if (!$form_state['values']['ack']) {
    form_set_error('ack', t('You must accept the partner agreement to continue.'));
  }
}

/**
 * Submit function for partner agreement page.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_tc_submit($form, &$form_state) {
  global $user;
  $edit['profile_user_state'] = 'Active partner';
  $edit['profile_partner_level'] = 'Ready Partner';
  profile_save_profile($edit, $user, 'Partner Program');
  $params['customer_name'] = $user->profile_first_name . ' ' . $user->profile_last_name;
  if ($params['customer_name'] == ' ') {
    $params['customer_name'] = $user->profile_display_name;
  }
  if ($params['customer_name'] == ' ') {
    $params['customer_name'] = $user->name;
  }
  watchdog('openshift_partner_program', '@user has accepted the partner agreement', array('@user' => $user->name), WATCHDOG_NOTICE);
  drupal_mail('openshift_partner_program', 'openshift_partner_program_tc', 'openshift-partners@redhat.com', 0, $params);
  drupal_goto('partner/portal');
}

/**
 * Callback function for Self Service Portal.
 *
 * @param string $content
 *   Content to prepend to result.
 *
 * @return mixed
 *   The content to display.
 */
function _openshift_partner_program_portal($content = NULL) {
  global $user;
  profile_load_profile($user);
  drupal_add_css(drupal_get_path('module', 'openshift_partner_program') . '/css/openshift_partner_program.css', 'module', 'all', FALSE);
  drupal_set_title(t('Openshift Partner Program Portal'));
  $partner_level = $user->profile_partner_level;
  $result = theme('openshift_partner_program_portal', array('partner_level' => $partner_level));
  return $result;
}

/**
 * Validate function for partner program upgrade request.
 */
function _openshift_partner_program_portal_upgrade() {
  drupal_set_title(t('Openshift Partner Program'));
  $form['#attributes'] = array('enctype' => "multipart/form-data");
  $form['subtitle'] = array(
    '#value' => '<h2>' . t('UPGRADE PARTNER LEVEL') . '</h2>',
  );
  $form['documentation_paste'] = array(
    '#type' => 'textarea',
    '#title' => t('Tell us why you want to become an OpenShift by Red Hat Advance Partner.'),
    '#description' => t('After submitting your information, the OpenShift Partnership Team will evaluate your request.'),
  );
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}

/**
 * Submit function for partner program upgrade request.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_portal_upgrade_submit($form, &$form_state) {
  global $user;
  global $base_url;
  $paste = '';
  if ($form_state['values']['documentation_paste']) {
    $paste = $form_state['values']['documentation_paste'];
  }
  $params['name'] = $user->name;
  $params['documentation'] = $paste;
  drupal_mail('openshift_partner_program', 'openshift_partner_program_partner_upgrade', 'openshift-partners@redhat.com', 0, $params);
  drupal_set_message(t('Partner level upgrade request submitted.'));
  drupal_goto('partner/portal');
}

/**
 * Callback function for partner program customer story request.
 */
function _openshift_partner_program_portal_customer_story() {
  global $user;
  profile_load_profile($user);
  drupal_set_title(t('Openshift Partner Program'));
  $form['#attributes'] = array('enctype' => "multipart/form-data");
  $form['subtitle'] = array(
    '#value' => '<h2>' . t('SUBMIT CUSTOMER SUCCESS STORY') . '</h2>',
  );
  $form['instructions'] = array(
    '#value' => '<h3>' . t('Have a great success story?  Let us help you develop and share it!') . '</h3>',
  );
  $form['customer']['customer_name'] = array(
    '#type' => 'textfield',
    '#title' => t('Customer'),
    '#required' => TRUE,
  );
  $form['customer']['customer_contact_name'] = array(
    '#type' => 'textfield',
    '#title' => t('Customer Contact Name'),
    '#required' => FALSE,
  );
  $form['self']['name'] = array(
    '#type' => 'textfield',
    '#title' => t('Your Name'),
    '#required' => TRUE,
    '#default_value' => $user->profile_display_name,
  );
  $form['self']['phone'] = array(
    '#type' => 'textfield',
    '#title' => t('Your Preferred Contact Number'),
    '#required' => FALSE,
  );
  $form['self']['email'] = array(
    '#type' => 'textfield',
    '#title' => t('Your Email'),
    '#required' => TRUE,
    '#default_value' => $user->mail,
  );
  $form['questions']['agree'] = array(
    '#type' => 'radios',
    '#title' => t('Has customer agreed to participate in a public success story?'),
    '#options' => array(
      'yes' => t('Yes'),
      'no' => t('No'),
    ),
  );
  $form['questions']['approach'] = array(
    '#type' => 'radios',
    '#title' => t('If no, have you approached the customer to participate in a public success story?'),
    '#options' => array(
      'yes' => t('Yes'),
      'no' => t('No'),
    ),
  );
  $form['description'] = array(
    '#type' => 'textarea',
    '#title' => t('Insert brief description of success story'),
  );
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}

/**
 * Submit function for partner program customer story request.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_portal_customer_story_submit($form, &$form_state) {
  $params['customer'] = $form_state['values']['customer_name'];
  $params['customer_contact_name'] = $form_state['values']['customer_contact_name'];
  $params['name'] = $form_state['values']['name'];
  $params['phone'] = $form_state['values']['phone'];
  $params['email'] = $form_state['values']['email'];
  $params['customer_agree'] = $form_state['values']['agree'];
  $params['customer_approached'] = $form_state['values']['approach'];
  $params['story_description'] = $form_state['values']['description'];
  drupal_mail('openshift_partner_program', 'openshift_partner_program_customer_story', 'openshift-partners@redhat.com', 0, $params);
  drupal_set_message(t('Customer Story request submitted.'));
  drupal_goto('partner/portal');
}

/**
 * Callback function for partner program assistance request.
 */
function _openshift_partner_program_portal_request_assistance() {
  global $user;
  profile_load_profile($user);
  drupal_set_title(t('Openshift Partner Program'));
  $form['#attributes'] = array('enctype' => "multipart/form-data");
  $form['subtitle'] = array(
    '#value' => '<h2>' . t('REQUEST ASSISTANCE') . '</h2>',
  );
  $form['instructions'] = array(
    '#value' => '<h3>' . t('Have a question?  Want to request marketing assistance?  Please complete the form below and we will reach out to you to get more information.') . '</h3>',
  );
  $form['name']['first'] = array(
    '#type' => 'textfield',
    '#title' => t('First Name'),
    '#default_value' => $user->profile_first_name,
    '#required' => TRUE,
  );
  $form['name']['last'] = array(
    '#type' => 'textfield',
    '#title' => t('Last Name'),
    '#default_value' => $user->profile_last_name,
    '#required' => TRUE,
  );
  $form['name']['company'] = array(
    '#type' => 'textfield',
    '#title' => t('Company'),
    '#default_value' => $user->profile_company,
    '#required' => TRUE,
  );
  $form['contact']['phone'] = array(
    '#type' => 'textfield',
    '#title' => t('Preferred Contact Number'),
    '#required' => FALSE,
  );
  $form['contact']['email'] = array(
    '#type' => 'textfield',
    '#title' => t('Email Address'),
    '#default_value' => $user->mail,
    '#required' => TRUE,
  );
  $form['questions']['related'] = array(
    '#type' => 'checkboxes',
    '#title' => t('Is your request related to'),
    '#options' => array(
      'general' => t('General Question'),
      'marketing' => t('Marketing'),
      'technical' => t('Technical'),
    ),
  );
  $form['description'] = array(
    '#type' => 'textarea',
    '#title' => t('Insert brief description of request'),
    '#required' => TRUE,
  );
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}

/**
 * Submit function for partner program assistance request.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_portal_request_assistance_submit($form, &$form_state) {
  $params['first_name'] = $form_state['values']['first'];
  $params['last_name'] = $form_state['values']['last'];
  $params['company_name'] = $form_state['values']['company'];
  $params['phone'] = $form_state['values']['phone'];
  $params['email'] = $form_state['values']['email'];
  $params['request_related_to'] = '';
  $related = $form_state['values']['related'];
  foreach ($related as $category) {
    if ($category) {
      $params['request_related_to'] .= "$category ";
    }
  }
  $params['description'] = $form_state['values']['description'];
  drupal_mail('openshift_partner_program', 'openshift_partner_program_request_assistance', 'openshift-partners@redhat.com', 0, $params);
  drupal_set_message(t('Request for assistance submitted.'));
  drupal_goto('partner/portal');
}

/**
 * Callback function for partner program company info upload.
 */
function _openshift_partner_program_portal_company_info() {
  global $user;
  $info = openshift_partner_program_partner_info();
  $company = ($info) ? $info['company'] : '';
  $company_description = ($info) ? $info['company_description'] : '';

  drupal_set_title(t('Openshift Partner Program'));
  $form['#attributes'] = array('enctype' => "multipart/form-data");
  $form['subtitle'] = array(
    '#value' => '<h2>' . t('UPLOAD COMPANY INFO') . '</h2>',
  );
  $form['instructions'] = array(
    '#value' => '<h3>' . t('Please provide the following information for your listing on the OpenShift Partner pages on openshift.com')  . '</h3>',
  );
  $form['company_name'] = array(
    '#type' => 'textfield',
    '#title' => t('Company Name'),
    '#default_value' => $company,
  );
  $form['company_description'] = array(
    '#type' => 'textarea',
    '#title' => t('Company Description'),
    '#default_value' => $company_description,
  );
  $form['logo'] = array(
    '#type' => 'file',
    '#title' => t('Upload logo'),
  );
  $form['expertise_tags'] = array(
    '#type' => 'select',
    '#multiple' => TRUE,
    '#options' => _openshift_partner_program_get_expertise_tags(),
    '#title' => t('Expertise Tags'),
    '#default_value' => _openshift_partner_program_get_selected_expertise_tags(),
  );
  $form['submit'] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}

/**
 * Submit function for partner program company upload info page.
 *
 * @param mixed $form
 *   The form.
 *
 * @param mixed $form_state
 *   The form state.
 */
function _openshift_partner_program_portal_company_info_submit($form, &$form_state) {
  global $user;
  $uid = $user->uid;
  $logo = '';
  if (count($_FILES)) {
    $file = file_save_upload('logo', array(), file_directory_path() . '/partner/logos', FILE_EXISTS_RENAME);
    $logo = $file->destination;
  }
  $company = $form_state['values']['company_name'];
  $company_description = $form_state['values']['company_description'];

  $expertise_tags = $form_state['values']['expertise_tags'];
  $expertise_tags = implode(',', $expertise_tags);

  $result = openshift_partner_program_partner_info_upsert_node($uid, $company, $company_description, $logo, $expertise_tags);

  if ($result) {
    drupal_set_message(t('Company info has been saved.'));
  }
  else {
    drupal_set_message(t('Failed to save company info.', 'error'));
  }

  drupal_goto('partner/portal');
}

/**
 * Returns the total possible expertise tags.
 *
 * @return mixed
 *   The expertise tags.
 */
function _openshift_partner_program_get_expertise_tags() {
  $vocab = reset(taxonomy_get_vocabularies('Partner'));
  $result = db_query("SELECT name FROM {term_data} where vid = %d order by name ASC", $vocab->vid);
  $tags = array();
  while ($row = db_fetch_array($result)) {
    $tags[$row['name']] = t($row['name']);
  }
  return $tags;
}

/**
 * Returns the selected expertise tags for the current user's profile.
 *
 * @return mixed
 *   The keys for the selected expertise tags.
 */
function _openshift_partner_program_get_selected_expertise_tags() {
  global $user;
  $node = node_load(array('uid' => $user->uid, 'type' => 'partner'));
  $tags = array();
  foreach ($node->taxonomy as $tag) {
    $tags[] = $tag->name;
  }
  return $tags;
}
