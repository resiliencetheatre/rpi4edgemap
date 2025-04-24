<?php
$db = new SQLite3('/opt/edgemap-persist/callsigns.db');

$radio_id = $_GET['radio_id'] ?? '';

if ($radio_id) {
    $stmt = $db->prepare('SELECT call_sign FROM callsigns WHERE radio_id = :radio_id');
    $stmt->bindValue(':radio_id', $radio_id, SQLITE3_TEXT);
    $result = $stmt->execute();
    $row = $result->fetchArray(SQLITE3_ASSOC);
    if ($row) {
        echo json_encode(['status' => 'ok', 'call_sign' => $row['call_sign']]);
    } else {
        echo json_encode(['status' => 'not_found']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Missing radio_id']);
}
