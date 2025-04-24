<?php
$db = new SQLite3('/opt/edgemap-persist/callsigns.db');

// Create table if it doesn't exist
$db->exec('CREATE TABLE IF NOT EXISTS callsigns (radio_id TEXT PRIMARY KEY, call_sign TEXT)');

$radio_id = $_POST['radio_id'] ?? '';
$call_sign = $_POST['call_sign'] ?? '';

if ($radio_id && $call_sign) {
    $stmt = $db->prepare('REPLACE INTO callsigns (radio_id, call_sign) VALUES (:radio_id, :call_sign)');
    $stmt->bindValue(':radio_id', $radio_id, SQLITE3_TEXT);
    $stmt->bindValue(':call_sign', $call_sign, SQLITE3_TEXT);
    $stmt->execute();
    echo json_encode(['status' => 'ok']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Missing parameters']);
}
