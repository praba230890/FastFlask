from typing import Any, Dict
import json

from starlette.types import Send, Scope

class Request:
    def __init__(self,  scope: Scope):
        self.method = scope["method"]
        self.path = scope["path"]
        