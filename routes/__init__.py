"""
Routes Package Initialization
Creates and registers web and API routers.
"""
from .router import Router
from .api import register_api_routes
from .web import register_web_routes


def get_configured_router() -> Router:
    """Build and return a unified Router configured with both Web and API routes."""
    router = Router()
    register_web_routes(router)
    register_api_routes(router)
    return router


__all__ = ["Router", "register_api_routes", "register_web_routes", "get_configured_router"]
