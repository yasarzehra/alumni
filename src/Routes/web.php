<?php

namespace App\Routes;

use App\Controllers\UserController;

/**
 * Web Routes Definition (/users) - Full CRUD Mapping
 * Maps Web UI endpoints to UserController actions with View Layer.
 */
return [
    // [R]ead
    'GET /users'              => [UserController::class, 'index'],
    'GET /users/{id}'         => [UserController::class, 'show'],

    // [C]reate
    'GET /users/create'       => [UserController::class, 'create'],
    'POST /users'             => [UserController::class, 'store'],

    // [U]pdate
    'GET /users/{id}/edit'    => [UserController::class, 'edit'],
    'POST /users/{id}'        => [UserController::class, 'update'],
    'PUT /users/{id}'         => [UserController::class, 'update'],
    'PATCH /users/{id}'       => [UserController::class, 'update'],

    // [D]elete
    'POST /users/{id}/delete' => [UserController::class, 'destroy'],
    'DELETE /users/{id}'      => [UserController::class, 'destroy'],
];
