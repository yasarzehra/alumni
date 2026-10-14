<?php
/**
 * View: src/Views/pages/users/index.php
 * Listing (R) and Creating (C) View Layer Template for Alumni Platform.
 * 
 * Variables:
 * @var array $users
 * @var int $count
 * @var string|null $error
 * @var string|null $success
 */
?>
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kullanıcılar - Alumni MVC View Layer</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f1f5f9; color: #0f172a; padding: 40px 20px; }
        .wrapper { max-width: 980px; margin: 0 auto; }
        .card { background: #ffffff; border-radius: 16px; padding: 32px; border: 1px solid #e2e8f0; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background: #f8fafc; font-size: 0.8rem; color: #475569; text-transform: uppercase; }
        .btn-submit { padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <div class="wrapper">
        <!-- 1. GET /users -> Listing (R) -->
        <div class="card">
            <h1>Kullanıcı Listesi (Listing - Read)</h1>
            <p>Route: <code>GET /users</code> &rarr; Controller: <code>UserController::index()</code></p>
            <table>
                <thead>
                    <tr><th>ID</th><th>İsim</th><th>E-posta</th><th>Tarih</th></tr>
                </thead>
                <tbody>
                    <?php if (!empty($users)): ?>
                        <?php foreach ($users as $user): ?>
                            <tr>
                                <td><strong>#<?= htmlspecialchars($user['id']) ?></strong></td>
                                <td><?= htmlspecialchars($user['name']) ?></td>
                                <td><code><?= htmlspecialchars($user['email']) ?></code></td>
                                <td><?= htmlspecialchars($user['createdAt'] ?? '-') ?></td>
                            </tr>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <tr><td colspan="4">Henüz kayıtlı kullanıcı bulunmamaktadır.</td></tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>

        <!-- 2. POST /users -> Creating (C) -->
        <div class="card">
            <h2>Yeni Kullanıcı Ekle (Creating - Create)</h2>
            <p>Route: <code>POST /users</code> &rarr; Controller: <code>UserController::store()</code></p>
            <form action="/users" method="POST">
                <input type="text" name="name" placeholder="Ad Soyad" required>
                <input type="email" name="email" placeholder="E-posta" required>
                <button type="submit" class="btn-submit">+ Kullanıcı Ekle</button>
            </form>
        </div>
    </div>
</body>
</html>
