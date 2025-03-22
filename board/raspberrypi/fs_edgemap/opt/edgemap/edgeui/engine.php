<?php
if (isset($_GET['code'])) {
    $code = $_GET['code'];
    $code = htmlspecialchars($code, ENT_QUOTES, 'UTF-8');
    echo "Received code: " . $code;
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
} else {
    echo "";
}
?>

