<?php

namespace App\Routes;

use App\Controllers\ApiUserController;
use App\Controllers\ApiAnnouncementController;

/**
 * API Routes Definition (/api/users & /api/announcements)
 */
return [
    // User API
    'GET /api/users'                 => [ApiUserController::class, 'index'],
    'GET /api/users/{id}'            => [ApiUserController::class, 'show'],
    'POST /api/users'                => [ApiUserController::class, 'store'],
    'PUT /api/users/{id}'            => [ApiUserController::class, 'update'],
    'PATCH /api/users/{id}'          => [ApiUserController::class, 'update'],
    'DELETE /api/users/{id}'         => [ApiUserController::class, 'destroy'],

    // Announcement API
    'GET /api/announcements'         => [ApiAnnouncementController::class, 'index'],
    'GET /api/announcements/{id}'    => [ApiAnnouncementController::class, 'show'],
    'POST /api/announcements'        => [ApiAnnouncementController::class, 'store'],
    'PUT /api/announcements/{id}'    => [ApiAnnouncementController::class, 'update'],
    'PATCH /api/announcements/{id}'  => [ApiAnnouncementController::class, 'update'],
    'DELETE /api/announcements/{id}' => [ApiAnnouncementController::class, 'destroy'],
];
