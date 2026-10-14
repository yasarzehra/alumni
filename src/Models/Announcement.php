<?php

namespace App\Models;

/**
 * Announcement Model - MVC Architecture
 * In-memory repository representation for Announcements.
 */
class Announcement
{
    private static array $db = [];
    private static int $currentId = 1;

    public static function create(array $data): array
    {
        $id = self::$currentId++;
        $record = [
            'id'        => $id,
            'title'     => $data['title'] ?? '',
            'content'   => $data['content'] ?? '',
            'category'  => $data['category'] ?? 'Genel',
            'author'    => $data['author'] ?? 'Alumni Koordinatörlüğü',
            'status'    => $data['status'] ?? 'Aktif',
            'createdAt' => date('c'),
        ];
        self::$db[] = $record;
        return $record;
    }

    public static function findAll(): array
    {
        return array_reverse(self::$db);
    }

    public static function findById(int $id): ?array
    {
        foreach (self::$db as $item) {
            if ($item['id'] === $id) {
                return $item;
            }
        }
        return null;
    }

    public static function update(int $id, array $data, bool $partial = false): ?array
    {
        foreach (self::$db as &$item) {
            if ($item['id'] === $id) {
                if (isset($data['title'])) $item['title'] = $data['title'];
                if (isset($data['content'])) $item['content'] = $data['content'];
                if (isset($data['category'])) $item['category'] = $data['category'];
                if (isset($data['author'])) $item['author'] = $data['author'];
                if (isset($data['status'])) $item['status'] = $data['status'];
                $item['updatedAt'] = date('c');
                return $item;
            }
        }
        return null;
    }

    public static function delete(int $id): bool
    {
        foreach (self::$db as $key => $item) {
            if ($item['id'] === $id) {
                array_splice(self::$db, $key, 1);
                return true;
            }
        }
        return false;
    }
}
