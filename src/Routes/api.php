<?php

namespace App\Routes;

use App\Controllers\ApiUserController;

/**
 * API Routes Definition (/api/users)
 * Maps REST endpoints to ApiUserController actions.
 */
return [
    'GET /api/users'          => [ApiUserController::class, 'index'],
    'GET /api/users/{id}'     => [ApiUserController::class, 'show'],
    'POST /api/users'         => [ApiUserController::class, 'store'],
    'PUT /api/users/{id}'     => [ApiUserController::class, 'update'],
    'PATCH /api/users/{id}'   => [ApiUserController::class, 'update'],
    'DELETE /api/users/{id}'  => [ApiUserController::class, 'destroy'],
];
