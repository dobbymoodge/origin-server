<?php

/**
 * Implementation of hook_taxonomy_default_vocabularies().
 */
function blogs_taxonomy_default_vocabularies() {
  return array(
    'tags' => array(
      'name' => 'Tags',
      'description' => 'Tags for this content',
      'help' => '',
      'relations' => '1',
      'hierarchy' => '0',
      'multiple' => '0',
      'required' => '0',
      'tags' => '1',
      'module' => 'features_tags',
      'weight' => '0',
      'nodes' => array(
        'blog' => 'blog',
        'event' => 'event',
        'knowledge_base' => 'knowledge_base',
        'page' => 'page',
        'video' => 'video',
      ),
    ),
  );
}
