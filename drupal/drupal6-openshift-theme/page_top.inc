<div id="top" class="section-top">
  <?php 
    $mission = variable_get('site_mission', '');
    if (!empty($mission)) {
      print $mission;
    }
  ?>
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
    <div>
      <div class="text">
        <a href="/blogs">Blog</a>
        <a class="icon-social" href="http://twitter.com/openshift"><span aria-hidden="true" data-icon="&#xee04;" title="Follow us on Twitter"> </span></a><a class="icon-social" href="http://facebook.com/openshift"><span aria-hidden="true" data-icon="&#xee05;" title="Like us on Facebook"> </span></a><a class="icon-social" href="http://plus.google.com/openshift"><span aria-hidden="true" data-icon="&#xee06;" title="Visit us on Google+"> </span></a>
      </div>
    </div>
  </div>
</div>
