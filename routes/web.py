"""
Web Routes - Presentation Layer
Maps browser HTTP requests to Web Controllers connected to the View Layer.
Organized into Direct (Top-level) and Nested (Hierarchical / Relational) Routes.

Includes:
1. Direct Routes:
   - Users: /users
   - Announcements: /announcements
   - Job Postings: /jobs & /job-postings
2. Nested Relational Routes:
   - User Jobs: /users/{user_id}/jobs
   - User Announcements: /users/{user_id}/announcements
"""
from routes.router import Router
from controllers.user_controller import UserController
from controllers.announcement_controller import AnnouncementController
from controllers.job_controller import JobController


def register_web_routes(router: Router) -> Router:
    """Register all Web browser CRUD routes with the View Layer."""

    # =========================================================================
    # 1. DIRECT ROUTES (Resource-Level CRUD)
    # =========================================================================

    # 1.1 User Web Routes (/users)
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

    # 1.2 Announcement Web Routes (/announcements)
    router.get('/announcements/create', lambda params, body=None: AnnouncementController.create())
    router.post('/announcements', lambda params, body=None: AnnouncementController.store(body or {}))
    router.get('/announcements', lambda params, body=None: AnnouncementController.index())
    router.get('/announcements/{id}', lambda params, body=None: AnnouncementController.show(params['id']))
    router.get('/announcements/{id}/edit', lambda params, body=None: AnnouncementController.edit(params['id']))
    router.post('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=False))
    router.put('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=False))
    router.patch('/announcements/{id}', lambda params, body=None: AnnouncementController.update(params['id'], body or {}, partial=True))
    router.post('/announcements/{id}/delete', lambda params, body=None: AnnouncementController.destroy(params['id']))
    router.delete('/announcements/{id}', lambda params, body=None: AnnouncementController.destroy(params['id']))

    # 1.3 Job Postings Web Routes (/jobs & /job-postings)
    for prefix in ['/jobs', '/job-postings']:
        router.get(f'{prefix}/create', lambda params, body=None: JobController.create())
        router.post(f'{prefix}', lambda params, body=None: JobController.store(body or {}))
        router.get(f'{prefix}', lambda params, body=None: JobController.index())
        router.get(f'{prefix}/{{id}}', lambda params, body=None: JobController.show(params['id']))
        router.get(f'{prefix}/{{id}}/edit', lambda params, body=None: JobController.show(params['id']))
        router.post(f'{prefix}/{{id}}', lambda params, body=None: JobController.update(params['id'], body or {}, partial=False))
        router.put(f'{prefix}/{{id}}', lambda params, body=None: JobController.update(params['id'], body or {}, partial=False))
        router.patch(f'{prefix}/{{id}}', lambda params, body=None: JobController.update(params['id'], body or {}, partial=True))
        router.post(f'{prefix}/{{id}}/delete', lambda params, body=None: JobController.destroy(params['id']))
        router.delete(f'{prefix}/{{id}}', lambda params, body=None: JobController.destroy(params['id']))

    # =========================================================================
    # 2. NESTED ROUTES (Hierarchical Parent-Child Relationships)
    # =========================================================================

    # 2.1 User's Job Postings: GET /users/{user_id}/jobs
    router.get('/users/{user_id}/jobs', lambda params, body=None: JobController.index(filter_user_id=params['user_id']))

    # 2.2 User's Announcements: GET /users/{user_id}/announcements
    router.get('/users/{user_id}/announcements', lambda params, body=None: AnnouncementController.index())

    return router
