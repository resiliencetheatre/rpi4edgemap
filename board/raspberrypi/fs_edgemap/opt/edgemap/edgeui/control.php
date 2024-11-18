<?php
    //
    // NOTE: You better harden this in your design, this is just a demo!
    // 
    
    $action=$_GET['id'];
    if ( $action == "poweroff" )
    {
        // chmod u+s /sbin/poweroff
        $output = shell_exec('/opt/edgemap/scripts/poweroff.sh 2>&1');
        echo "Executing poweroff: ".$output;
    }
    if ( $action == "distress" )
    {
        echo "Executing distress";
    }
    if ( $action == "wipe" )
    {
        echo "Executing wipe";
    }
    if ( $action == "pos_off" )
    {
        echo "Periodic position send:<br> OFF";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh off 2>&1');
    }
    if ( $action == "pos_2" )
    {
        echo "Periodic position send:<br> 2 minutes";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh 2 2>&1');
    }
    if ( $action == "pos_4" )
    {
        echo "Periodic position send:<br> 4 minutes";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh 4 2>&1');
    }
    if ( $action == "pos_10" )
    {
        echo "Periodic position send:<br> 10 minutes";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh 10 2>&1');
    }
    if ( $action == "pos_manual" )
    {
        echo "Periodic position send:<br> manual only";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh manual 2>&1');
    }
    if ( $action == "pos_random" )
    {
        echo "Periodic position send:<br> randomly";
        $output = shell_exec('/opt/edgemap/scripts/set_pos_interval.sh random 2>&1');
    }
    
    
    

    
    

?>
