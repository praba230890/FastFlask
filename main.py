from typing import Callable, Dict

import uvicorn
from starlette.types import Receive, Scope, Send

from response import Response
class FastFlask:
    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def route(self, path: str):
        """Decorator to register a route."""
        def decorator(func: Callable):
            self.routes[path] = func
            return func
        return decorator

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """ASGI entry point."""
        assert scope["type"] == "http"
        path = scope["path"]
        handler = self.routes.get(path, self.default_response)
        response = Response()
        result = await handler(response)  # Pass Response object
        
        if isinstance(result, dict):  # Auto-wrap dicts as JSON
            response.set_json(result)
        elif isinstance(result, str):  # Auto-wrap strings
            response.body = result.encode()
        
        await response.send(send)
    
    async def default_response(self, response: Response):
        response.status = 404
        response.body = b"404 Not Found"
        return response

def run_server(app: FastFlask, host="127.0.0.1", port=8000):
    uvicorn.run(app, host=host, port=port)

