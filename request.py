"""
    Module for the request and request related things   
"""

from starlette.types import Scope

class Request:
    """
        Request object that can be used in the routes
    """
    def __init__(self,  scope: Scope):
        self.method = scope["method"]
        self.path = scope["path"]
        