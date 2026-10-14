<?php
/**
 * View: src/Views/pages/users/edit.php
 * Edit User Form View
 */
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kullanıcıyı Düzenle - Alumni MVC</title>
</head>
<body>
    <h1>Kullanıcı Düzenle #<?= htmlspecialchars($user['id']) ?></h1>
    <form action="/users/<?= htmlspecialchars($user['id']) ?>" method="POST">
        <label>Ad Soyad: <input type="text" name="name" value="<?= htmlspecialchars($user['name']) ?>" required></label><br>
        <label>E-posta: <input type="email" name="email" value="<?= htmlspecialchars($user['email']) ?>" required></label><br>
        <button type="submit">Güncelle</button>
        <a href="/users/<?= htmlspecialchars($user['id']) ?>">İptal</a>
    </form>
</body>
</html>
