"""
Web Routes - /users (MVC Presentation Layer)
Maps browser HTTP requests to UserController methods connected to the View Layer.

Full CRUD Operations on User Resource:
1. [R]ead Listing:   GET    /users              -> UserController.index()   -> View (Index Table)
2. [C]reate Form:    GET    /users/create       -> UserController.create()  -> View (Create Form)
3. [C]reate Action:  POST   /users              -> UserController.store()   -> Model + View
4. [R]ead Detail:    GET    /users/{id}         -> UserController.show()    -> View (Profile Card)
5. [U]pdate Form:    GET    /users/{id}/edit    -> UserController.edit()    -> View (Edit Form)
6. [U]pdate Action:  POST   /users/{id}         -> UserController.update()  -> Model + View
                     PUT    /users/{id}         -> UserController.update()  -> Model + View
                     PATCH  /users/{id}         -> UserController.update()  -> Model + View
7. [D]elete Action:  POST   /users/{id}/delete  -> UserController.destroy() -> Model + View
                     DELETE /users/{id}         -> UserController.destroy() -> Model + View
"""
from routes.router import Router
from controllers.user_controller import UserController


def register_web_routes(router: Router) -> Router:
    """Register all Web browser CRUD routes with the View Layer."""

    # 1. [C]reate Routes
    router.get('/users/create', lambda params, body=None: UserController.create())
    router.post('/users', lambda params, body=None: UserController.store(body or {}))

    # 2. [R]ead Routes
    router.get('/users', lambda params, body=None: UserController.index())
    router.get('/users/{id}', lambda params, body=None: UserController.show(params['id']))

    # 3. [U]pdate Routes
    router.get('/users/{id}/edit', lambda params, body=None: UserController.edit(params['id']))
    router.post('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=False))
    router.put('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=False))
    router.patch('/users/{id}', lambda params, body=None: UserController.update(params['id'], body or {}, partial=True))

    # 4. [D]elete Routes
    router.post('/users/{id}/delete', lambda params, body=None: UserController.destroy(params['id']))
    router.delete('/users/{id}', lambda params, body=None: UserController.destroy(params['id']))

    return router
