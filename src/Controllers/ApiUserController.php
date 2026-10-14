<?php

namespace App\Controllers;

use App\Models\User;

/**
 * ApiUserController - RESTful API Controller (MVC)
 * Handles JSON API requests and returns JSON payloads with HTTP status codes.
 */
class ApiUserController
{
    /**
     * GET /api/users
     * [R]ead: Get all users as JSON
     */
    public function index(): array
    {
        $users = User::findAll();
        return [
            'status' => 200,
            'body' => [
                'success' => true,
                'count' => count($users),
                'data' => $users
            ]
        ];
    }

    /**
     * GET /api/users/{id}
     * [R]ead: Get single user by ID
     */
    public function show(int $id): array
    {
        $user = User::findById($id);
        if (!$user) {
            return [
                'status' => 404,
                'body' => [
                    'error' => 'NotFound',
                    'message' => "{$id} ID'li kullanıcı bulunamadı"
                ]
            ];
        }
        return [
            'status' => 200,
            'body' => [
                'success' => true,
                'data' => $user
            ]
        ];
    }

    /**
     * POST /api/users
     * [C]reate: Create user from JSON payload
     */
    public function store(array $data): array
    {
        if (empty($data['name']) || empty($data['email'])) {
            return [
                'status' => 400,
                'body' => [
                    'error' => 'BadRequest',
                    'message' => 'name ve email alanları zorunludur'
                ]
            ];
        }

        try {
            $newUser = User::create($data);
            return [
                'status' => 201,
                'body' => [
                    'success' => true,
                    'message' => 'Kullanıcı başarıyla oluşturuldu',
                    'data' => $newUser
                ]
            ];
        } catch (\InvalidArgumentException $e) {
            return [
                'status' => 409,
                'body' => [
                    'error' => 'Conflict',
                    'message' => $e->getMessage()
                ]
            ];
        }
    }

    /**
     * PUT /api/users/{id} or PATCH /api/users/{id}
     * [U]pdate: Update user
     */
    public function update(int $id, array $data, bool $partial = false): array
    {
        if (!User::findById($id)) {
            return [
                'status' => 404,
                'body' => [
                    'error' => 'NotFound',
                    'message' => "{$id} ID'li kullanıcı bulunamadı"
                ]
            ];
        }

        if (empty($data)) {
            return [
                'status' => 400,
                'body' => [
                    'error' => 'BadRequest',
                    'message' => 'Güncellenecek en az bir alan gönderilmelidir'
                ]
            ];
        }

        if (!$partial && (empty($data['name']) || empty($data['email']))) {
            return [
                'status' => 400,
                'body' => [
                    'error' => 'BadRequest',
                    'message' => 'PUT isteğinde name ve email alanları zorunludur'
                ]
            ];
        }

        try {
            $updatedUser = User::update($id, $data, $partial);
            $action = $partial ? 'kısmen güncellendi' : 'güncellendi';
            return [
                'status' => 200,
                'body' => [
                    'success' => true,
                    'message' => "Kullanıcı başarıyla {$action}",
                    'data' => $updatedUser
                ]
            ];
        } catch (\InvalidArgumentException $e) {
            return [
                'status' => 409,
                'body' => [
                    'error' => 'Conflict',
                    'message' => $e->getMessage()
                ]
            ];
        }
    }

    /**
     * DELETE /api/users/{id}
     * [D]elete: Remove user
     */
    public function destroy(int $id): array
    {
        $deleted = User::delete($id);
        if (!$deleted) {
            return [
                'status' => 404,
                'body' => [
                    'error' => 'NotFound',
                    'message' => "{$id} ID'li kullanıcı bulunamadı"
                ]
            ];
        }

        return [
            'status' => 200,
            'body' => [
                'success' => true,
                'message' => "{$id} ID'li kullanıcı başarıyla silindi"
            ]
        ];
    }
}
