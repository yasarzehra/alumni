"""
API Routes - RESTful API
Maps API requests to REST Controllers returning JSON payloads.

Includes:
1. User API Routes (/api/users)
2. Announcement API Routes (/api/announcements)
"""
from routes.router import Router
from controllers.api_user_controller import ApiUserController
from controllers.api_announcement_controller import ApiAnnouncementController


def register_api_routes(router: Router) -> Router:
    """Register all RESTful API routes on the provided router."""

    # =========================================================================
    # User API Routes (/api/users)
    # =========================================================================
    router.get('/api/users', lambda params, body=None: ApiUserController.index())
    router.get('/api/users/{id}', lambda params, body=None: ApiUserController.show(params['id']))
    router.post('/api/users', lambda params, body=None: ApiUserController.store(body or {}))
    router.put('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=False))
    router.patch('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=True))
    router.delete('/api/users/{id}', lambda params, body=None: ApiUserController.destroy(params['id']))

    # =========================================================================
    # Announcement API Routes (/api/announcements)
    # =========================================================================
    router.get('/api/announcements', lambda params, body=None: ApiAnnouncementController.index())
    router.get('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.show(params['id']))
    router.post('/api/announcements', lambda params, body=None: ApiAnnouncementController.store(body or {}))
    router.put('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.update(params['id'], body or {}, partial=False))
    router.patch('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.update(params['id'], body or {}, partial=True))
    router.delete('/api/announcements/{id}', lambda params, body=None: ApiAnnouncementController.destroy(params['id']))

    return router
