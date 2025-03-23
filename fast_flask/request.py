"""
    Module for the request and request related things   
"""
from typing import Dict, Self
from contextvars import ContextVar

from starlette.types import Scope

class Request:
    """
        Request object that can be used in the routes
    """
    def __init__(self,  method: str, path: str, headers: Dict[str, str], cookies: Dict[str, str]):
        self.method = method
        self.path = path
        self.headers = headers
        self.cookies = cookies

    @classmethod
    def from_scope(cls, scope: Scope) -> Self:
        """

        Args:
            scope (Scope): uvicorn scope that has the request data

        Returns:
            the Request object that was created from the data derived from the uvicorn Scope 
        """
        method = scope["method"]
        path = scope["path"]
        headers = scope["headers"]
        print(headers)
        cookies = {}
        # https://datatracker.ietf.org/doc/html/rfc6265 
        for header in headers:
            if header[0] == b"cookie":
                print(header[0])
                _cookies = header[1].decode()
                for cookie in _cookies.split(";"):
                    print(cookie)
                    cookies[cookie.split('=', maxsplit=1)[0]] = cookie.split('=')[1]
        return cls(method, path, headers, cookies)

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
