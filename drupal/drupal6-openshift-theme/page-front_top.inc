    <div id="top" class="section-top">
      <?php $block = module_invoke('block', 'block', 'view', '8'); print $block['content']; ?>
      <div class="container">
        <a title="Track open issues on the OpenShift status page" style="display:none;" id="outage" class="btn btn-small btn-warning" href="<?php print $openshift_server_url; ?>/app/status">Status</a>
          <div class="pull-right login">

          <form action="/search/node" method="get" id="search-top">
             <input name="keys" class="search-query" type="text" placeholder="SEARCH">
             <button type="submit" class="search" value="Search"></button>
             <?php print $search['hidden']; ?>
          </form>

            <?php
            global $user;

            print '<a class="btn btn-small" href="'.$openshift_server_url.'/app/console">My Apps</a> ';
            if ($user->uid == 0) {
              print '<a class="btn btn-small" href="'.redhat_sso_register_url().'">Sign Up</a> ';
            } else {
              print '<a class="btn btn-small" href="/logout">Sign Out</a> ';
            }
            ?>
          </div>
          <div class=""><a href="/blogs">Blog</a></div>
        </div>
      </div>
    </div>