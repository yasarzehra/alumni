<?php

namespace App\Routes;

use App\Controllers\UserController;
use App\Controllers\AnnouncementController;

/**
 * Web Routes Definition (/users & /announcements) - Full CRUD Mapping
 */
return [
    // Users
    'GET /users'                      => [UserController::class, 'index'],
    'GET /users/{id}'                 => [UserController::class, 'show'],
    'GET /users/create'               => [UserController::class, 'create'],
    'POST /users'                     => [UserController::class, 'store'],
    'GET /users/{id}/edit'            => [UserController::class, 'edit'],
    'POST /users/{id}'                => [UserController::class, 'update'],
    'PUT /users/{id}'                 => [UserController::class, 'update'],
    'PATCH /users/{id}'               => [UserController::class, 'update'],
    'POST /users/{id}/delete'         => [UserController::class, 'destroy'],
    'DELETE /users/{id}'              => [UserController::class, 'destroy'],

    // Announcements
    'GET /announcements'              => [AnnouncementController::class, 'index'],
    'GET /announcements/{id}'         => [AnnouncementController::class, 'show'],
    'GET /announcements/create'       => [AnnouncementController::class, 'create'],
    'POST /announcements'             => [AnnouncementController::class, 'store'],
    'GET /announcements/{id}/edit'    => [AnnouncementController::class, 'edit'],
    'POST /announcements/{id}'        => [AnnouncementController::class, 'update'],
    'PUT /announcements/{id}'         => [AnnouncementController::class, 'update'],
    'PATCH /announcements/{id}'       => [AnnouncementController::class, 'update'],
    'POST /announcements/{id}/delete' => [AnnouncementController::class, 'destroy'],
    'DELETE /announcements/{id}'      => [AnnouncementController::class, 'destroy'],
];
