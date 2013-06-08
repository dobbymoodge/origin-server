<?php
//echo '<pre>';
//print_r($node->uid);
//$user->uid;
//echo '</pre>';
$do = og_comment_perms_do();
?>

<section id="node-<?php print $node->nid; ?>" class="<?php if ($sticky) { print ' sticky'; } ?><?php if (!$status) { print ' node-unpublished'; } ?>">

<div class="events-post node node-events">
  <div class="metadata">
    <?php if (strlen($node->field_event_logo[0]["view"]) > 0): ?>
        <figure class="pull-right related-block">
            <div class="related-logo">
                <?php print $node->field_event_logo[0]["view"] ?>
            </div>
        </figure>
    <?php endif; ?> 

    <p class="event-dates">
      <?php print $node->field_event_start_date[0]["view"] ?>
        <?php if (strlen($node->field_event_timezone[0]["view"]) > 0): ?>
            (<?php print $node->field_event_timezone[0]["view"] ?>)
        <?php endif; ?> 
      <!--<a href="" class="add-calendar">Add to calendar</a>-->
    </p>
    
    <?php if (strlen($node->field_event_venue[0]["view"]) > 0): ?>
        <h4><?php print $node->field_event_venue[0]["view"] ?></h4>
    <?php endif; ?> 

    <?php print $node->field_event_city[0]["view"] ?><?php if (strlen($node->field_event_city[0]["view"]) > 0 && strlen($node->field_event_state[0]["view"]) > 0) echo ", " ?> 
    <?php print $node->field_event_state[0]["view"] ?> 
    <?php if ((strlen($node->field_event_city[0]["view"]) > 0 || strlen($node->field_event_state[0]["view"]) > 0) && strlen($node->field_event_country[0]["view"]) > 0) echo " - " ?> 
    <?php print $node->field_event_country[0]["view"] ?>
    
    <?php if (strlen($node->field_event_url[0]["view"]) > 0) echo "<br />" ?> 
    <?php print $node->field_event_url[0]["view"] ?><br />
  </div>

  <?php if (strlen($node->content["body"]["#value"]) > 0): ?> 
      <p>
        <?php print $node->content["body"]["#value"] ?>
      </p>
  <?php endif; ?> 

  <?php if (strlen($node->field_event_categories[0]["view"]) > 0): ?> 
    <div class="terms">Tags: <?php print $node->field_event_categories[0]["view"] ?></div>
  <?php endif; ?>

  <?php print openshift_social_sharing($node_url, $title); ?>    
</div>  
</section>
