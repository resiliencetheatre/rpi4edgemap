<?php
/* 
 * This is engine for interacting with system from UI. 
 * - UI post data to this script and gets output this produces
 * - When UI wants to do something, this script will either just write
 *   or read/write FIFO's. 
 * - FIFO's are read at system side by listener.sh script, run by
 *   engine.service
 * 
 */
if (isset($_GET['code']) && isset($_GET['read'])) {
    $read = $_GET['read'];
    $code = $_GET['code'];
    $code = htmlspecialchars($code, ENT_QUOTES, 'UTF-8');
    $read = htmlspecialchars($read, ENT_QUOTES, 'UTF-8');
    
    // This only writes FIFO (eg. set interval, shutdown etc)
    if ( $read == 0 ) 
    {
        echo "Received write code: " . $code;
        $fifo = "/tmp/engine";        
        // Open the FIFO in write mode
        $fp = fopen($fifo, 'w');
        if (!$fp) {
            die("Failed to open FIFO for writing.");
        }
        $message = $code . "\n";
        fwrite($fp, $message);
        fflush($fp); 
        sleep(1); 
        fclose($fp);
        exit();
    }
    
    // We want to read some result from listener.sh
    // So first we write to FIFO and then we read result to web UI 
    if ( $read == 1 ) 
    {        
        // Write FIFO command first
        $fifo = "/tmp/engine";        
        $fp = fopen($fifo, 'w');
        if (!$fp) {
            die("Failed to open FIFO for writing.");
        }
        $message = $code . "\n";
        fwrite($fp, $message);
        fflush($fp); 
        sleep(1); 
        fclose($fp);
        sleep(1);
        
        // Read result from FIFO which listener.sh has written (hopefully)
        $fifo = "/tmp/fromengine";

        // Ensure the FIFO exists (check this)
        if (!file_exists($fifo)) {
            posix_mkfifo($fifo, 0666);
        }

        // Open the FIFO in read mode
        $fp = fopen($fifo, 'r');
        if (!$fp) {
            die("Failed to open FIFO for reading.");
        }

        // Loop until we have something from FIFO
        // TODO: Timeout would be nice
        $loop_exit=true;
        while ($loop_exit) {
            $line = fgets($fp);
            if ($line !== false) {
                echo $line;
                $loop_exit = false;
            } else {
                // Optional: sleep to avoid 100% CPU usage if you're not expecting frequent messages
                usleep(100000); // 100 ms
            }
        }

        fclose($fp);

        
    }
    
} else {
    echo "";
}
?>

