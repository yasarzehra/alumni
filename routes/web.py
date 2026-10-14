"""
Web Routes - Presentation Layer
Maps browser HTTP requests to Web Controllers connected to the View Layer.

Includes:
1. User Routes (/users)
2. Announcement Routes (/announcements) with full Management Interface (CRUD)
"""
from routes.router import Router
from controllers.user_controller import UserController
from controllers.announcement_controller import AnnouncementController


def register_web_routes(router: Router) -> Router:
    """Register all Web browser CRUD routes with the View Layer."""

    # =========================================================================
    # User Web Routes (/users)
    # =========================================================================
    router.get('/users/create', lambda params, body=None: UserController.create())
    router.post('/users', lambda params, body=None: UserController.store(body or {}))
    router.get('/users', lambda params, body=None: UserController.index())
    router.get('/users/{id}', lambda params, body=None: UserController.show(params['id']))
    router.get('/users/{id}/edit', lambda params, body=None: UserController.edit(params['id']))
    router.post('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=False))
    router.put('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=False))
    router.patch('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=True))
    router.post('/users/{id}/delete', lambda params, body=None: UserController.destroy(params['id']))
    router.delete('/users/{id}', lambda params, body=None: UserController.destroy(params['id']))

    # =========================================================================
    # Announcement Web Routes (/announcements) - Management Interface
    # =========================================================================
    # 1. [C]reate
    router.get('/announcements/create', lambda params, body=None: AnnouncementController.create())
    router.post('/announcements', lambda params, body=None: AnnouncementController.store(body or {}))

    # 2. [R]ead
    router.get('/announcements', lambda params, body=None: AnnouncementController.index())
    router.get('/announcements/{id}', lambda params, body=None: AnnouncementController.show(params['id']))

    # 3. [U]pdate
    router.get('/announcements/{id}/edit', lambda params, body=None: AnnouncementController.edit(params['id']))
    router.post('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=False))
    router.put('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=False))
    router.patch('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=True))

    # 4. [D]elete
    router.post('/announcements/{id}/delete', lambda params, body=None: AnnouncementController.destroy(params['id']))
    router.delete('/announcements/{id}', lambda params, body=None: AnnouncementController.destroy(params['id']))

    return router
