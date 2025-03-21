from typing import Callable, Dict

import uvicorn
from starlette.types import Receive, Scope, Send

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
        response = await handler()
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")]
        })
        await send({
            "type": "http.response.body",
            "body": response.encode()
        })
    
    async def default_response(self):
        return "404 Not Found"

def run_server(app: FastFlask, host="127.0.0.1", port=8000):
    uvicorn.run(app, host=host, port=port)

