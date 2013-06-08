      <div id="nav" class="section-nav lift-counter">
        <div class="navbar">
          <div class="container">
            <div class="brand">
              <a href="/">
                <div class="brand-image"></div>
                <div class="brand-text"><strong>Open</strong>Shift</div>
              </a>
            </div>
            <ul class="nav nav-primary">
                <?php foreach( menu_tree_page_data('primary-links') as $key=>$item) {
                $link = $item["link"];
                if (!$link['hidden']) {
                  $link['options']['html'] = TRUE;
                  unset($link['options']['attributes']['title']);

                  $visibleChildren = array();
                  if ($item['below']) {
                    foreach($item['below'] as $childkey=>$child) {
                      if(!$child['link']['hidden']) {
                        $visibleChildren[$childkey] = $child;
                      }
                    }
                  }
                  $hasChildren = !empty($visibleChildren);
                    ?>
                    <li class="<?php print $hasChildren ? "dropdown dropdown-toggle " : ""; ?><?php print $link['in_active_trail'] ? "active" : ""; ?>"><?php print l("<span>" . $link['title'] . "</span>", $link['href'], $link['options']); ?>
                      <?php print openshift_primary_link_megamenu($link, $visibleChildren); ?>
                    </li>
              <?php }} ?>
            </ul>
          </div>
        </div>

        <?php print $messaging; ?>
      </div>
