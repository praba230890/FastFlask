"""
    Module for the request and request related things   
"""
from contextvars import ContextVar

from starlette.types import Scope

class Request:
    """
        Request object that can be used in the routes
    """
    def __init__(self,  scope: Scope):
        self.method = scope["method"]
        self.path = scope["path"]

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

request = RequestProxy()
