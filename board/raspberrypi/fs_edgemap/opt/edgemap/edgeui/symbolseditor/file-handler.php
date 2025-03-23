<?php
$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $fileName = $input['file'] ?? '';
    $content = $input['content'] ?? '';

    if (!$fileName) {
        http_response_code(400);
        echo "Missing file name.";
        exit;
    }

    $baseDir = "/opt/edgemap-persist"; // Storage directory
    $filePath = realpath($baseDir) . '/' . basename($fileName); // Secure path

    if (file_put_contents($filePath, $content) === false) {
        http_response_code(500);
        echo "Failed to save file.";
        exit;
    }

    echo "File saved successfully at: $filePath";
} elseif ($method === 'GET') {
    $fileName = $_GET['file'] ?? '';

    if (!$fileName) {
        http_response_code(400);
        echo "Missing file name.";
        exit;
    }

    $baseDir = "/opt/edgemap-persist"; // Storage directory
    $filePath = realpath($baseDir) . '/' . basename($fileName); // Secure path

    if (!file_exists($filePath)) {
        http_response_code(404);
        echo "File not found.";
        exit;
    }

    echo file_get_contents($filePath);
} else {
    http_response_code(405);
    echo "Method not allowed.";
}
?>
