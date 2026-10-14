<?php

namespace App\Controllers;

use App\Models\Announcement;

/**
 * AnnouncementController - Web Controller (PHP Blueprint)
 */
class AnnouncementController
{
    public function index(): string
    {
        $announcements = Announcement::findAll();
        return "announcements/index";
    }

    public function show(int $id): string
    {
        $announcement = Announcement::findById($id);
        return $announcement ? "announcements/show" : "errors/404";
    }

    public function create(): string
    {
        return "announcements/create";
    }

    public function store(array $data): string
    {
        Announcement::create($data);
        return "announcements/index";
    }

    public function edit(int $id): string
    {
        $announcement = Announcement::findById($id);
        return $announcement ? "announcements/edit" : "errors/404";
    }

    public function update(int $id, array $data): string
    {
        Announcement::update($id, $data);
        return "announcements/show";
    }

    public function destroy(int $id): string
    {
        Announcement::delete($id);
        return "announcements/index";
    }
}
