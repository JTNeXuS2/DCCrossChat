<?php

// Проверяем наличие GET параметра 'public_key'
if (!isset($_GET['public_key']) || empty($_GET['public_key'])) {
    header('Content-Type: application/json');
    // Выводим ошибку и завершаем выполнение скрипта
    http_response_code(400); // Устанавливаем код ответа 400 Bad Request
    echo '400 Bad Request'; // Выводим сообщение об ошибке
    exit(); // Завершаем выполнение скрипта
}else{
	$public_key = isset($_GET['public_key']) ? $_GET['public_key'] : '';
}

$ip = $_SERVER['REMOTE_ADDR'];
$filename = 'ip_log.txt';
$dates = date("[D H:i:s d.m.y]");
if (!empty($public_key) || $ip != '192.168.0.10') {
    $data = $dates . ' ' . $ip;
    if (!empty($public_key)) {
        $data .= ' key: ' . $public_key;
    }
    $data .= PHP_EOL;
    file_put_contents($filename, $data, FILE_APPEND | LOCK_EX);
}

$seed = "PRIVATESEED";
$pubseed = "PUBLICSEED";

// Генерация приватного ключа
$private_key = hash('sha256', $seed);

// Генерация и проверка публичных ключей
$public_keys = [];
for ($i = 0; $i < 1000; $i++) {  // Генерация 5 публичных ключей
    $generated_public_key = hash('sha256', $private_key . ':' . $i);
    $is_valid = check_public_key_validity($generated_public_key, $seed, $private_key);
    if ($is_valid) {
        $public_keys[] = $generated_public_key;
    }
}

// Функция проверки валидности публичного ключа
function check_public_key_validity($public_key, $seed, $private_key) {
    $generated_private_key = hash('sha256', $seed);
    for ($i = 0; $i < 1000; $i++) {
        $generated_public_key = hash('sha256', $generated_private_key . ':' . $i);
        if ($generated_public_key === $public_key) {
            return true;
        }
    }
    return false;
}

//echo "Приватный ключ: " . $private_key . "\n";
//echo "Публичные ключи: " . implode(", ", $public_keys) . "\n";

// Проверяем, что получен публичный ключ через GET-запрос
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Получаем публичный ключ из параметра 'public_key'
    //$public_key = isset($_GET['public_key']) ? $_GET['public_key'] : '';
	
    // Устанавливаем заголовок для ответа в формате JSON
    header('Content-Type: application/json');
    
    // Проверяем валидность публичного ключа
    $result = check_public_key_validity($public_key, $seed, $private_key);
    $secret = hash('sha256', $pubseed);

    // Создаем ассоциативный массив с данными

// Создаем ассоциативный массив с данными
if ($result) {
    $response = array(
        'transmitted key' => $public_key,
        'VALIDATE' => $result,
        'secret' => $secret
    );
} else {
    $response = array(
        'transmitted key' => $public_key,
        'VALIDATE' => $result,
        'secret' => $result
    );
}
		
    // Отправляем ответ клиенту в формате JSON
    echo json_encode($response);
    header('Connection: close');
}
?>
