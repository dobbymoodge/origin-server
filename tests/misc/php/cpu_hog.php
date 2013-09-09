<?php

function do_something_not_particularly_efficient() {    
    $x = "useless";
    $x = "something".$x;
    $x = "doing".$x;
    return $x;
}

function inefficient_infinite_loop() {
    // Adding a couple loops to not hit recursive stack limit any time soon
    for ($i = 0; $i <= PHP_INT_MAX; $i++) {
        for ($j = 0; $j <= PHP_INT_MAX; $j++) {     
            do_something_not_particularly_efficient();
        }
    }
    inefficient_infinite_loop();
}

// Start up 4 processes (including the one already running) for good measure
$pid = pcntl_fork();
$pid = pcntl_fork();
inefficient_infinite_loop();

?>
