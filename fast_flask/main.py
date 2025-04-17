"""
    Module that has the main class for creating the application object - FastFlask 
"""

from typing import Callable, Dict
from collections import UserList

import uvicorn
from starlette.types import Receive, Scope, Send

from fast_flask.response import Response
from fast_flask.request import Request, current_request
from fast_flask.router import Router

class FastFlask:
    """
        The main class to create the app object.
        This app object is what will be fed into the uvicorn as an interface to the ASGI server
    """
    def __init__(self):
        self.router = Router()

    def route(self, 
                path: str,
                methods: UserList[str]=("GET", "POST", "PUT", "DELETE", "UPDATE", "OPTION")):
        """Decorator to register a route."""
        def decorator(func: Callable):
            self.router.add_route(path, func, methods)
            return func
        return decorator

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """ASGI entry point."""
        assert scope["type"] == "http"
        path = scope["path"]
        handler, params = self.router.match(path, scope["method"])
        if not handler:
            handler = self.default_response
        current_request.set(Request.from_scope(scope))
        response = Response()
        result = await handler(response, **params)
        if not isinstance(result, Response):
            response.body = result
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
