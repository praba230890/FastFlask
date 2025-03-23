"""
    Module for the response and response related things   
"""

from typing import Any, Dict
import json

from starlette.types import Send


class Response:
    """
        The class for creating a response object
        
        Args:
            body
            status
            headers
        
    """
    def __init__(self, body: Any = "", status: int = 200, headers: Dict[bytes, bytes] = None):
        self.body = body if isinstance(body, bytes) else str(body).encode()
        self.status = status
        self.headers = {b"content-type": b"text/plain"}
        if headers:
            self.headers.update(headers)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, result):
        if isinstance(result, dict):
            self.set_json(result)
        elif isinstance(result, str):
            self._body = result.encode()

    def set_json(self, data: Dict[Any, Any]):
        """Set response body as JSON"""
        self._body = json.dumps(data).encode()
        self.headers[b"content-type"] = b"application/json"

    async def send(self, send: Send):
        """

        Args:
            send (Send): _description_
        """
        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": list(self.headers.items()),
        })
        await send({
            "type": "http.response.body",
            "body": self._body,
        })
