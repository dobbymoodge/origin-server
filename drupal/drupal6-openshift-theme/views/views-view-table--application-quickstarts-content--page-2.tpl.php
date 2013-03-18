<?php
/**
 * @file views-view-table.tpl.php
 * Template to display a view as a table.
 *
 * - $title : The title of this group of rows.  May be empty.
 * - $header: An array of header labels keyed by field id.
 * - $fields: An array of CSS IDs to use for each field id.
 * - $class: A class or classes to apply to the table, based on settings.
 * - $row_classes: An array of classes to apply to each row, indexed by row
 *   number. This matches the index in $rows.
 * - $rows: An array of row items. Each row is an array of content.
 *   $rows are keyed by row number, fields within rows are keyed by field ID.
 * @ingroup views_templates
 */
?>
<table class="table <?php print $class; ?>"<?php print $attributes; ?>>
  <?php if (!empty($title)) : ?>
    <caption><?php print $title; ?></caption>
  <?php endif; ?>
  <?php 
    $hasHeader = false;
    foreach ($header as $field => $label) {
      $label = trim($label);
      if (!empty($label)) {
        $hasHeader = true;
        break;
      }
    }
    if ($hasHeader) { ?>
  <thead>
    <tr>
      <?php foreach ($header as $field => $label): 
        if ($field == 'markup'){ continue; }
        ?>
        <th class="views-field views-field-<?php print $fields[$field]; ?>"><?php print $label; ?></th>
      <?php endforeach; ?>
    </tr>
  </thead>
  <?php } ?>
  <tbody>
    <?php foreach ($rows as $count => $row): ?>
      <tr class="<?php print implode(' ', $row_classes[$count]); ?>">
        <?php foreach ($row as $field => $content): 
          if ($field == 'markup') { continue; } ?>
          <td class="views-field views-field-<?php print $fields[$field]; ?>"><?php print $content; ?></td>
        <?php endforeach; ?>
      </tr>
      <?php 
        $field = 'markup';
        if (array_key_exists($field, $row)) { 
          $content = $row[$field]; ?>
        <tr class="<?php print implode(' ', $row_classes[$count]); ?> views-row-extra">
          <td colspan="<?php print(count($row) - 1); ?>" class="views-field views-field-<?php print $fields[$field]; ?>"><?php print $content; ?></td>
        </tr>
      <?php } ?>
    <?php endforeach; ?>
  </tbody>
</table>

