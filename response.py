from typing import Any, Dict
import json

from starlette.types import Send


class Response:
    def __init__(self, body: Any = "", status: int = 200, headers: Dict[bytes, bytes] = None):
        self.body = body if isinstance(body, bytes) else str(body).encode()
        self.status = status
        self.headers = {b"content-type": b"text/plain"}
        if headers:
            self.headers.update(headers)

    def set_json(self, data: Dict[Any, Any]):
        """Set response body as JSON"""
        self.body = json.dumps(data).encode()
        self.headers[b"content-type"] = b"application/json"

    async def send(self, send: Send):
        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": list(self.headers.items()),
        })
        await send({
            "type": "http.response.body",
            "body": self.body,
        })