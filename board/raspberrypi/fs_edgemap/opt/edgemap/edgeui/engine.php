<?php
if (isset($_GET['code']) && isset($_GET['read'])) {
    $read = $_GET['read'];
    $code = $_GET['code'];
    $code = htmlspecialchars($code, ENT_QUOTES, 'UTF-8');
    $read = htmlspecialchars($read, ENT_QUOTES, 'UTF-8');
    
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
    }
    
    // We want to read some result from listener.sh 
    if ( $read == 1 ) 
    {
        // echo "Received read code: " . $code;
        
        // Write first
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
        
        sleep(1);
        
        // Read result
        
        $fifo = "/tmp/fromengine";

        // Ensure the FIFO exists
        if (!file_exists($fifo)) {
            posix_mkfifo($fifo, 0666);
        }

        // Open the FIFO in read mode
        $fp = fopen($fifo, 'r');
        if (!$fp) {
            die("Failed to open FIFO for reading.");
        }

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

