"""
API Routes - /api/users
Maps API requests to ApiUserController methods.
"""
from routes.router import Router
from controllers.api_user_controller import ApiUserController


def register_api_routes(router: Router) -> Router:
    """Register all RESTful API routes on the provided router."""
    # List all users
    router.get('/api/users', lambda params, body=None: ApiUserController.index())
    
    # Get single user by ID
    router.get('/api/users/{id}', lambda params, body=None: ApiUserController.show(params['id']))
    
    # Create new user
    router.post('/api/users', lambda params, body=None: ApiUserController.store(body or {}))
    
    # Full update user (PUT)
    router.put('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=False))
    
    # Partial update user (PATCH)
    router.patch('/api/users/{id}', lambda params, body=None: ApiUserController.update(params['id'], body or {}, partial=True))
    
    # Delete user
    router.delete('/api/users/{id}', lambda params, body=None: ApiUserController.destroy(params['id']))
    
    return router
