<?php

/**
 * Expose current active contexts as a context condition, but ensure that
 * the operation is IF no negative contexts && zero or more positive conditions
 */
class context_condition_context_active extends context_condition {

  function condition_values() {
    return array();
  }

  /**
   * Condition form.
   */
  function condition_form($context) {
    $form = parent::condition_form($context);
    unset($form['#options']);

    $form['#type'] = 'textarea';
    $form['#default_value'] = implode("\n", $this->fetch_from_context($context, 'values'));
    return $form;
  }

  /**
   * Condition form submit handler.
   */
  function condition_form_submit($values) {
    $parsed = array();
    $items = explode("\n", $values);
    if (!empty($items)) {
      foreach ($items as $v) {
        $v = trim($v);
        if (!empty($v)) {
          $parsed[$v] = $v;
        }
      }
    }
    return $parsed;
  }  

  function execute() {
    if ($this->condition_used()) {
      $active_contexts = array_keys(context_active_contexts());
      foreach ($this->get_contexts() as $context) {
        if (!in_array($context->name, $active_contexts, TRUE) && $values = $this->fetch_from_context($context, 'values')) {
          $match = FALSE;
          foreach ($values as $pattern) {
            if (strpos($pattern, '~') === 0) {
              if (in_array(ltrim($pattern, '~'), $active_contexts, TRUE)) {
                $match = FALSE;
                break;
              }
              $match = TRUE;
            }
            else {
              if (in_array($pattern, $active_contexts, TRUE)) {
                $match = TRUE;
                break;
              }
            }
          }
          if ($match) {
            array_push($active_contexts, $context->name);
            $this->condition_met($context);
          }
        }
      }
    }
  }
}
