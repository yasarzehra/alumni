<?php
/**
 * View: src/Views/pages/users/create.php
 * Create User Form View
 */
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Yeni Kullanıcı Oluştur - Alumni MVC</title>
</head>
<body>
    <h1>Yeni Kullanıcı Oluştur (Create Form)</h1>
    <form action="/users" method="POST">
        <label>Ad Soyad: <input type="text" name="name" required></label><br>
        <label>E-posta: <input type="email" name="email" required></label><br>
        <button type="submit">Kaydet</button>
        <a href="/users">İptal</a>
    </form>
</body>
</html>
