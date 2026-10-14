"""
Router - MVC Routing System
Matches incoming HTTP requests (Method + URL Pattern) to Controller action methods.
Supports dynamic path parameters like {id}.
"""
import re
from typing import Callable, Dict, List, Tuple, Optional, Any


class Route:
    def __init__(self, method: str, pattern: str, handler: Callable):
        self.method = method.upper()
        self.pattern = pattern
        self.handler = handler
        # Convert pattern with {param} to named regex groups
        def _param_to_regex(m):
            param_name = m.group(1)
            if param_name == 'id' or param_name.endswith('_id'):
                return f'(?P<{param_name}>\\d+)'
            return f'(?P<{param_name}>[^/]+)'

        regex_pattern = re.sub(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', _param_to_regex, pattern)
        self.regex = re.compile(f'^{regex_pattern}/?$')

    def match(self, method: str, path: str) -> Optional[Dict[str, Any]]:
        if self.method != method.upper():
            return None
        match = self.regex.match(path)
        if match:
            params = match.groupdict()
            # Convert numeric parameter values to integers
            for k, v in params.items():
                if v.isdigit():
                    params[k] = int(v)
            return params
        return None


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add(self, method: str, pattern: str, handler: Callable):
        self.routes.append(Route(method, pattern, handler))

    def get(self, pattern: str, handler: Callable):
        self.add("GET", pattern, handler)

    def post(self, pattern: str, handler: Callable):
        self.add("POST", pattern, handler)

    def put(self, pattern: str, handler: Callable):
        self.add("PUT", pattern, handler)

    def patch(self, pattern: str, handler: Callable):
        self.add("PATCH", pattern, handler)

    def delete(self, pattern: str, handler: Callable):
        self.add("DELETE", pattern, handler)

    def dispatch(self, method: str, path: str) -> Optional[Tuple[Callable, Dict[str, Any]]]:
        """
        Dispatches method and path to the matching handler.
        Returns (handler, params_dict) or None if not found.
        """
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None
