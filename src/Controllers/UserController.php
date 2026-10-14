<?php

namespace App\Controllers;

use App\Models\User;

/**
 * UserController - Web Controller (MVC)
 * Manages web browser views, forms, and redirects for the User entity.
 */
class UserController
{
    /**
     * [R]ead: Display all users on web interface
     */
    public function index(): array
    {
        $users = User::findAll();
        return [
            'view' => 'users/index.php',
            'users' => $users,
            'count' => count($users)
        ];
    }

    /**
     * [R]ead: Display a single user's detail profile
     */
    public function show(int $id): array
    {
        $user = User::findById($id);
        if (!$user) {
            return [
                'view' => 'errors/404.php',
                'error' => "User {$id} not found"
            ];
        }
        return [
            'view' => 'users/show.php',
            'user' => $user
        ];
    }

    /**
     * [C]reate: Handle form submission to create a user
     */
    public function store(array $data): array
    {
        try {
            $user = User::create($data);
            return [
                'redirect' => "/users/{$user['id']}",
                'success' => true,
                'user' => $user
            ];
        } catch (\InvalidArgumentException $e) {
            return [
                'view' => 'users/create.php',
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * [U]pdate: Handle form submission to update a user
     */
    public function update(int $id, array $data, bool $partial = false): array
    {
        try {
            $user = User::update($id, $data, $partial);
            if (!$user) {
                return [
                    'view' => 'errors/404.php',
                    'error' => "User {$id} not found"
                ];
            }
            return [
                'redirect' => "/users/{$user['id']}",
                'success' => true,
                'user' => $user
            ];
        } catch (\InvalidArgumentException $e) {
            return [
                'view' => 'users/edit.php',
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * [D]elete: Remove user
     */
    public function destroy(int $id): array
    {
        $deleted = User::delete($id);
        if (!$deleted) {
            return [
                'view' => 'errors/404.php',
                'error' => "User {$id} not found"
            ];
        }
        return [
            'redirect' => '/users',
            'success' => true
        ];
    }
}
