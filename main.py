"""
   Module that has the main class for creating the application object - FastFlask 
"""

from typing import Callable, Dict
from collections import UserList
from contextvars import ContextVar

import uvicorn
from starlette.types import Receive, Scope, Send

from response import Response
from request import Request

current_request: ContextVar[Request] = ContextVar("current_request")

class RequestProxy:
    """
        A proxy class to handle request object attribute access
    """
    def __getattr__(self, name):
        request = current_request.get(None)
        if request is None:
            raise RuntimeError(
                "Request object is not set. Make sure you're inside a request context."
                )
        return getattr(request, name)

class FastFlask:
    """
        The main class to create the app object.
        This app object is what will be fed into the uvicorn as an interface to the ASGI server
    """
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable | UserList[str]]] = {}

    def route(self, 
                path: str,
                methods: UserList[str]=("GET", "POST", "PUT", "DELETE", "UPDATE", "OPTION")):
        """Decorator to register a route."""
        def decorator(func: Callable):
            self.routes[path] = {}
            self.routes[path]["handler"] = func
            self.routes[path]["methods"] = methods
            return func
        return decorator

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """ASGI entry point."""
        assert scope["type"] == "http"
        path = scope["path"]
        if self.routes.get(path) and scope["method"] in self.routes.get(path)["methods"]:
            handler = self.routes.get(path)["handler"] 
        else:
            handler = self.default_response
        current_request.set(Request(scope))
        response = Response()
        result = await handler(response)
        if isinstance(result, dict):
            response.set_json(result)
        elif isinstance(result, str):
            response.body = result.encode()
        await response.send(send)

    async def default_response(self, response: Response):
        """
            handler to send a 404 response if no route if found for a request
        """
        response.status = 404
        response.body = b"404 Not Found"
        return response

def run_server(app: FastFlask, host="127.0.0.1", port=8000):
    """
    the function to start the user application

    Args:
        app (FastFlask): _description_
        host (str, optional): _description_. Defaults to "127.0.0.1".
        port (int, optional): _description_. Defaults to 8000.
    """
    uvicorn.run(app, host=host, port=port)

request = RequestProxy()
