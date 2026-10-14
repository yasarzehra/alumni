<?php

namespace App\Models;

/**
 * User Model - MVC Architecture
 * In-memory repository implementation of User entity without database connection.
 * Provides complete CRUD operations.
 */
class User
{
    private static array $db = [];
    private static int $currentId = 1;

    /**
     * [C]reate: Add a new user to the in-memory store
     */
    public static function create(array $data): array
    {
        $name = trim($data['name'] ?? '');
        $email = trim($data['email'] ?? '');

        if (empty($name) || empty($email)) {
            throw new \InvalidArgumentException("name and email fields are required");
        }

        if (self::findByEmail($email) !== null) {
            throw new \InvalidArgumentException("Email '{$email}' is already registered");
        }

        $id = self::$currentId++;
        $now = (new \DateTime('now', new \DateTimeZone('UTC')))->format(\DateTime::ATOM);

        $record = array_merge([
            'id' => $id,
            'name' => $name,
            'email' => $email,
            'createdAt' => $now
        ], $data);

        self::$db[] = $record;
        return $record;
    }

    /**
     * [R]ead: Get all users
     */
    public static function findAll(): array
    {
        return self::$db;
    }

    /**
     * [R]ead: Find user by ID
     */
    public static function findById(int $id): ?array
    {
        foreach (self::$db as $user) {
            if ($user['id'] === $id) {
                return $user;
            }
        }
        return null;
    }

    /**
     * [R]ead: Find user by email (case-insensitive)
     */
    public static function findByEmail(string $email): ?array
    {
        foreach (self::$db as $user) {
            if (strcasecmp($user['email'], $email) === 0) {
                return $user;
            }
        }
        return null;
    }

    /**
     * [U]pdate: Update user (full or partial)
     */
    public static function update(int $id, array $data, bool $partial = false): ?array
    {
        foreach (self::$db as &$user) {
            if ($user['id'] === $id) {
                if (isset($data['email']) && strcasecmp($data['email'], $user['email']) !== 0) {
                    $conflict = self::findByEmail($data['email']);
                    if ($conflict && $conflict['id'] !== $id) {
                        throw new \InvalidArgumentException("Email '{$data['email']}' is already in use");
                    }
                }

                if (!$partial) {
                    if (empty($data['name']) || empty($data['email'])) {
                        throw new \InvalidArgumentException("name and email fields are required for full update");
                    }
                    $user['name'] = $data['name'];
                    $user['email'] = $data['email'];
                } else {
                    if (isset($data['name'])) $user['name'] = $data['name'];
                    if (isset($data['email'])) $user['email'] = $data['email'];
                }

                foreach ($data as $k => $v) {
                    if (!in_array($k, ['id', 'createdAt'])) {
                        $user[$k] = $v;
                    }
                }

                $user['updatedAt'] = (new \DateTime('now', new \DateTimeZone('UTC')))->format(\DateTime::ATOM);
                return $user;
            }
        }
        return null;
    }

    /**
     * [D]elete: Remove user by ID
     */
    public static function delete(int $id): bool
    {
        $count = count(self::$db);
        self::$db = array_values(array_filter(self::$db, fn($u) => $u['id'] !== $id));
        return count(self::$db) < $count;
    }

    /**
     * Reset in-memory database (testing helper)
     */
    public static function clear(): void
    {
        self::$db = [];
        self::$currentId = 1;
    }
}
