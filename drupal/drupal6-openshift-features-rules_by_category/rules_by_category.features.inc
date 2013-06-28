<?php

/**
 * Implementation of hook_rules_defaults().
 */
function rules_by_category_rules_defaults() {
  return array(
    'rules' => array(
      'rules_comment_on_faq_or_kb' => array(
        '#type' => 'rule',
        '#set' => 'event_comment_insert',
        '#label' => 'Comment on FAQ or KB',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'comment',
          '1' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Commented content is FAQ or Knowledge Base',
              'arguments' => array(
                'node' => array(
                  'type' => 'node',
                  'label' => 'Content',
                ),
              ),
              'module' => 'Node',
            ),
            '#name' => 'rules_condition_content_is_type',
            '#settings' => array(
              'type' => array(
                'faq' => 'faq',
                'knowledge_base' => 'knowledge_base',
              ),
              '#argument map' => array(
                'node' => 'node',
              ),
            ),
            '#type' => 'condition',
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'to' => 'nduong@redhat.com,sannam@redhat.com',
              'from' => '',
              'subject' => 'New comment posted on a [node:type-name] Content type',
              'message' => 'Hello, 

A user has posted the following comment to the [node:type-name] titled [node:title].  

[comment:comment-body]',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'subject' => array(
                    '0' => 'node',
                    '1' => ':global',
                  ),
                  'message' => array(
                    '0' => 'comment',
                    '1' => 'node',
                    '2' => ':global',
                  ),
                  'from' => array(
                    '0' => ':global',
                  ),
                  'to' => array(
                    '0' => ':global',
                  ),
                ),
              ),
            ),
            '#name' => 'rules_action_mail',
            '#info' => array(
              'label' => 'Send a mail to an arbitrary mail address',
              'module' => 'System',
              'eval input' => array(
                '0' => 'subject',
                '1' => 'message',
                '2' => 'from',
                '3' => 'to',
              ),
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_email_when_comment_deleted' => array(
        '#type' => 'rule',
        '#set' => 'event_comment_delete',
        '#label' => 'Email when comment deleted',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'delete',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Send a mail to an arbitrary mail address',
              'module' => 'System',
              'eval input' => array(
                '0' => 'subject',
                '1' => 'message',
                '2' => 'from',
                '3' => 'to',
              ),
            ),
            '#name' => 'rules_action_mail',
            '#settings' => array(
              'to' => 'nduong@redhat.com,sannam@redhat.com',
              'from' => '',
              'subject' => 'Comment deleted from openshift community site',
              'message' => 'A user with the email [:global:user-mail] has deleted the following comment from node [node:nid] :

[comment:comment-body]',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'subject' => array(
                    '0' => ':global',
                  ),
                  'message' => array(
                    '0' => 'comment',
                    '1' => 'node',
                    '2' => ':global',
                  ),
                  'from' => array(
                    '0' => ':global',
                  ),
                  'to' => array(
                    '0' => ':global',
                  ),
                ),
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_email_when_node_deleted' => array(
        '#type' => 'rule',
        '#set' => 'event_node_delete',
        '#label' => 'Email when node deleted',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'delete',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'to' => 'nduong@redhat.com,sannam@redhat.com',
              'from' => '',
              'subject' => 'Node deleted from Openshift Community',
              'message' => 'Node [node:nid] with title [node:title] has been deleted from the Openshift community site by [user:mail]

[node:node-body]',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'subject' => array(
                    '0' => ':global',
                  ),
                  'message' => array(
                    '0' => 'node',
                    '1' => 'user',
                    '2' => ':global',
                  ),
                  'from' => array(
                    '0' => ':global',
                  ),
                  'to' => array(
                    '0' => ':global',
                  ),
                ),
              ),
            ),
            '#name' => 'rules_action_mail',
            '#info' => array(
              'label' => 'Send a mail to an arbitrary mail address',
              'module' => 'System',
              'eval input' => array(
                '0' => 'subject',
                '1' => 'message',
                '2' => 'from',
                '3' => 'to',
              ),
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_feature_completed' => array(
        '#type' => 'rule',
        '#set' => 'event_node_update',
        '#label' => 'Feature Completed',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'Completed Feature',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Updated content\'s field \'field_state\' has been changed',
              'arguments' => array(
                'node' => array(
                  'type' => 'node',
                  'label' => 'Content containing changes',
                ),
                'node_unchanged' => array(
                  'type' => 'node',
                  'label' => 'Content not containing changes',
                ),
              ),
              'module' => 'CCK',
            ),
            '#name' => 'content_rules_field_changed',
            '#settings' => array(
              'field_name' => 'field_state',
              '#argument map' => array(
                'node' => 'node',
                'node_unchanged' => 'node_unchanged',
              ),
            ),
            '#type' => 'condition',
          ),
          '1' => array(
            '#type' => 'condition',
            '#settings' => array(
              'field_name' => 'field_state',
              '#argument map' => array(
                'node' => 'node',
              ),
              'value' => array(
                '0' => array(
                  'value' => 'Completed',
                ),
              ),
              'code' => '',
              'vars' => array(),
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'code' => array(
                    '0' => ':global',
                  ),
                  'value|0|value' => array(
                    '0' => ':global',
                  ),
                ),
              ),
            ),
            '#name' => 'content_rules_field_has_value',
            '#info' => array(
              'label' => 'Updated content\'s field \'field_state\' has value',
              'arguments' => array(
                'node' => array(
                  'type' => 'node',
                  'label' => 'Content',
                ),
              ),
              'eval input' => array(
                '0' => 'code',
                '1' => 'value|0|value',
              ),
              'module' => 'CCK',
            ),
            '#weight' => 0,
          ),
        ),
        '#actions' => array(),
        '#version' => 6003,
      ),
      'rules_flag_inappropriate_discussion_topic' => array(
        '#type' => 'rule',
        '#set' => 'event_flag_flagged_abuse_node',
        '#label' => 'Flag - Inappropriate Discussion Topic',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'Flag',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Flagging count >= 3, for flagged content, under "Node Abuse"',
              'base' => 'flag_rules_condition_threshold',
              'label callback' => 'flag_rules_condition_threshold_label',
              'arguments' => array(
                'flag' => array(
                  'type' => 'flag',
                  'label' => 'Flag',
                  'flag_type' => 'node',
                ),
                'object' => array(
                  'type' => 'node',
                  'label' => 'Flagged content',
                ),
                'number' => array(
                  'type' => 'number',
                  'label' => 'Number',
                  'description' => 'The number against which to test the number of times the object is flagged. For example, if you type "3" here, and choose "Greater than" for the operator, then this condition will return TRUE if the object is flagged more than three times.',
                ),
              ),
              'module' => 'Flag',
            ),
            '#name' => 'flag_rules_condition_threshold_node',
            '#settings' => array(
              'flag' => 'abuse_node',
              'number' => '3',
              'operator' => '>=',
              '#argument map' => array(
                'object' => 'node',
              ),
            ),
            '#type' => 'condition',
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'recipients' => array(
                '0' => 3,
              ),
              'from' => '',
              'subject' => 'Discussion Topic Flagged as Inappropriate 3 Times',
              'message' => 'A discussion topic on openshift.redhat.com has been flagged as inappropriate at least three times.

To view the discussion topic, visit [node:node-url].',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'message' => array(
                    '0' => 'node',
                  ),
                ),
              ),
            ),
            '#name' => 'rules_action_mail_to_users_of_role',
            '#info' => array(
              'label' => 'Send a mail to all users of a role',
              'module' => 'System',
              'eval input' => array(
                '0' => 'subject',
                '1' => 'message',
                '2' => 'from',
              ),
            ),
          ),
          '1' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Log to watchdog',
              'module' => 'System',
              'eval input' => array(
                '0' => 'type',
                '1' => 'message',
                '2' => 'link',
              ),
            ),
            '#name' => 'rules_action_watchdog',
            '#settings' => array(
              'severity' => '5',
              'type' => 'rules',
              'message' => 'The node [node:node-path] was flagged as inappropriate',
              'link' => '[node:node-path]',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'message' => array(
                    '0' => 'node',
                  ),
                  'link' => array(
                    '0' => 'node',
                  ),
                ),
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_badges_community_member' => array(
        '#type' => 'rule',
        '#set' => 'event_userpoints_event_points_awarded',
        '#label' => 'User Badges - Community Member',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'badges',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#type' => 'condition',
            '#settings' => array(
              'type' => '0',
              'amount' => '20',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'userpoints_rules_amount',
            '#info' => array(
              'label' => 'Compare current Userpoints',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'amount',
              ),
            ),
            '#weight' => 0,
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'module' => 'User',
              'arguments' => array(
                'user' => array(
                  'label' => 'User',
                  'type' => 'user',
                ),
              ),
              'label' => 'Add badge',
              'base' => 'rules_core_action_execute',
              'action_name' => 'user_badges_add_badge_action',
              'configurable' => TRUE,
            ),
            '#name' => 'rules_core_user_badges_add_badge_action',
            '#settings' => array(
              'badges' => array(
                '4' => 4,
              ),
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_badges_expert' => array(
        '#type' => 'rule',
        '#set' => 'event_userpoints_event_points_awarded',
        '#label' => 'User Badges - Expert',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'badges',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#info' => array(
              'label' => 'Compare current Userpoints',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'amount',
              ),
            ),
            '#name' => 'userpoints_rules_amount',
            '#settings' => array(
              'type' => '0',
              'amount' => '800',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'condition',
            '#weight' => 0,
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'badges' => array(
                '1' => 1,
              ),
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'rules_core_user_badges_add_badge_action',
            '#info' => array(
              'module' => 'User',
              'arguments' => array(
                'user' => array(
                  'label' => 'User',
                  'type' => 'user',
                ),
              ),
              'label' => 'Add badge',
              'base' => 'rules_core_action_execute',
              'action_name' => 'user_badges_add_badge_action',
              'configurable' => TRUE,
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_badges_newbie' => array(
        '#type' => 'rule',
        '#set' => 'event_userpoints_event_points_awarded',
        '#label' => 'User Badges - Newbie',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'badges',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#type' => 'condition',
            '#settings' => array(
              'type' => '0',
              'amount' => '0',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'userpoints_rules_amount',
            '#info' => array(
              'label' => 'Compare current Userpoints',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'amount',
              ),
            ),
            '#weight' => 0,
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'module' => 'User',
              'arguments' => array(
                'user' => array(
                  'label' => 'User',
                  'type' => 'user',
                ),
              ),
              'label' => 'Add badge',
              'base' => 'rules_core_action_execute',
              'action_name' => 'user_badges_add_badge_action',
              'configurable' => TRUE,
            ),
            '#name' => 'rules_core_user_badges_add_badge_action',
            '#settings' => array(
              'badges' => array(
                '5' => 5,
              ),
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_badges_pro' => array(
        '#type' => 'rule',
        '#set' => 'event_userpoints_event_points_awarded',
        '#label' => 'User Badges - Pro',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'badges',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#info' => array(
              'label' => 'Compare current Userpoints',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'amount',
              ),
            ),
            '#name' => 'userpoints_rules_amount',
            '#settings' => array(
              'type' => '0',
              'amount' => '400',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'condition',
            '#weight' => 0,
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'badges' => array(
                '2' => 2,
              ),
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'rules_core_user_badges_add_badge_action',
            '#info' => array(
              'module' => 'User',
              'arguments' => array(
                'user' => array(
                  'label' => 'User',
                  'type' => 'user',
                ),
              ),
              'label' => 'Add badge',
              'base' => 'rules_core_action_execute',
              'action_name' => 'user_badges_add_badge_action',
              'configurable' => TRUE,
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_new_user' => array(
        '#type' => 'rule',
        '#set' => 'event_user_insert',
        '#label' => 'User Points - New User',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'points' => '5',
              'description' => '',
              'operation' => 'New User',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'account',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_join_a_group' => array(
        '#type' => 'rule',
        '#set' => 'event_og_user_insert',
        '#label' => 'User Points - Join a Group',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          '1' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#settings' => array(
              'points' => '10',
              'description' => '',
              'operation' => '',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_leave_a_group' => array(
        '#type' => 'rule',
        '#set' => 'event_og_user_delete',
        '#label' => 'User Points - Leave a Group',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          '1' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'points' => '-10',
              'description' => '',
              'operation' => '',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_new_account_creation' => array(
        '#type' => 'rule',
        '#set' => 'event_user_insert',
        '#label' => 'User Points - New Account Creation',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          '1' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#settings' => array(
              'points' => '5',
              'description' => '',
              'operation' => '',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'action',
          ),
        ),
        '#version' => 6003,
      ),
      'rules_flag_inappropriate_comment' => array(
        '#type' => 'rule',
        '#set' => 'event_flag_flagged_abuse_comment',
        '#label' => 'Flag - Inappropriate Comment',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'Flag',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Flagging count >= 3, for flagged comment, under "Comment Abuse"',
              'base' => 'flag_rules_condition_threshold',
              'label callback' => 'flag_rules_condition_threshold_label',
              'arguments' => array(
                'flag' => array(
                  'type' => 'flag',
                  'label' => 'Flag',
                  'flag_type' => 'comment',
                ),
                'object' => array(
                  'type' => 'comment',
                  'label' => 'Flagged comment',
                ),
                'number' => array(
                  'type' => 'number',
                  'label' => 'Number',
                  'description' => 'The number against which to test the number of times the object is flagged. For example, if you type "3" here, and choose "Greater than" for the operator, then this condition will return TRUE if the object is flagged more than three times.',
                ),
              ),
              'module' => 'Flag',
            ),
            '#name' => 'flag_rules_condition_threshold_comment',
            '#settings' => array(
              'flag' => 'abuse_comment',
              'number' => '3',
              'operator' => '>=',
              '#argument map' => array(
                'object' => 'comment',
              ),
            ),
            '#type' => 'condition',
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#weight' => 0,
            '#type' => 'action',
            '#settings' => array(
              'recipients' => array(
                '0' => 3,
              ),
              'from' => '',
              'subject' => 'Comment Flagged as Inappropriate 3 Times',
              'message' => 'A comment on openshift.redhat.com has been flagged as inappropriate at least three times.

To view the comment, visit [comment:comment-url].',
              '#eval input' => array(
                'token_rules_input_evaluator' => array(
                  'message' => array(
                    '0' => 'comment',
                  ),
                ),
              ),
            ),
            '#name' => 'rules_action_mail_to_users_of_role',
            '#info' => array(
              'label' => 'Send a mail to all users of a role',
              'module' => 'System',
              'eval input' => array(
                '0' => 'subject',
                '1' => 'message',
                '2' => 'from',
              ),
            ),
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_badges_accomplished' => array(
        '#type' => 'rule',
        '#set' => 'event_userpoints_event_points_awarded',
        '#label' => 'User Badges - Active Contributor',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'badges',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Compare current Userpoints',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'amount',
              ),
            ),
            '#name' => 'userpoints_rules_amount',
            '#settings' => array(
              'type' => '0',
              'amount' => '100',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'condition',
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#type' => 'action',
            '#settings' => array(
              'badges' => array(
                '3' => 3,
              ),
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'rules_core_user_badges_add_badge_action',
            '#info' => array(
              'module' => 'User',
              'arguments' => array(
                'user' => array(
                  'label' => 'User',
                  'type' => 'user',
                ),
              ),
              'label' => 'Add badge',
              'base' => 'rules_core_action_execute',
              'action_name' => 'user_badges_add_badge_action',
              'configurable' => TRUE,
            ),
            '#weight' => 0,
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_new_discussion_topic' => array(
        '#type' => 'rule',
        '#set' => 'event_node_insert',
        '#label' => 'User Points - New Discussion Topic',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(
          '0' => array(
            '#weight' => 0,
            '#info' => array(
              'label' => 'Content is a group post',
              'arguments' => array(
                'group' => array(
                  'type' => 'node',
                  'label' => 'Group post',
                ),
              ),
              'module' => 'Organic groups',
            ),
            '#name' => 'og_rules_condition_content_is_group_post',
            '#settings' => array(
              '#argument map' => array(
                'group' => 'node',
              ),
            ),
            '#type' => 'condition',
          ),
        ),
        '#actions' => array(
          '0' => array(
            '#type' => 'action',
            '#settings' => array(
              'points' => '5',
              'description' => '',
              'operation' => 'New Discussion Topic',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
            '#weight' => 0,
          ),
        ),
        '#version' => 6003,
      ),
      'rules_user_points_post_a_comment' => array(
        '#type' => 'rule',
        '#set' => 'event_comment_publish',
        '#label' => 'User Points - Post a Comment',
        '#active' => 1,
        '#weight' => '0',
        '#categories' => array(
          '0' => 'points',
          'rules_by_category' => 'rules_by_category',
        ),
        '#status' => 'default',
        '#conditions' => array(),
        '#actions' => array(
          '0' => array(
            '#info' => array(
              'label' => 'Grant points to a user',
              'arguments' => array(
                'user' => array(
                  'type' => 'user',
                  'label' => 'User',
                ),
              ),
              'module' => 'Userpoints',
              'eval input' => array(
                '0' => 'points',
                '1' => 'entity_id',
              ),
            ),
            '#name' => 'userpoints_action_grant_points',
            '#settings' => array(
              'points' => '5',
              'description' => '',
              'operation' => 'Post a Comment',
              'entity_type' => '',
              'entity_id' => '',
              'tid' => '',
              '#argument map' => array(
                'user' => 'user',
              ),
            ),
            '#type' => 'action',
            '#weight' => 0,
          ),
        ),
        '#version' => 6003,
      ),
    ),
  );
}
