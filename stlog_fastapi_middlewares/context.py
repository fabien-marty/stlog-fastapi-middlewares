from dataclasses import field, dataclass
import os
from typing import Any
from starlette.applications import ASGIApp
from starlette.types import Receive, Scope, Send
import stlog
import uuid


@dataclass(kw_only=True)
class LogContextMiddleware:
    app: ASGIApp
    add_request_id: bool = True
    add_pid: bool = False
    add_kvs: dict[str, Any] = field(default_factory=dict)
    headers_to_kvs: dict[str, str] = field(default_factory=dict)
    envs_to_kvs: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.headers_to_kvs.items():
            self.headers_to_kvs[key.lower()] = value
        for key, value in self.envs_to_kvs.items():
            self.envs_to_kvs[key.upper()] = value

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return None
        kwargs: dict[str, Any] = {}
        if self.add_request_id:
            kwargs["request_id"] = str(uuid.uuid4()).replace("-", "")
        if self.add_pid:
            kwargs["pid"] = os.getpid()
        if self.add_kvs:
            kwargs.update(self.add_kvs)
        for k, v in self.envs_to_kvs.items():
            if k in os.environ:
                kwargs[v] = os.environ[k]
        headers = scope.get("headers", [])
        for name, value in headers:
            if name.lower() in self.headers_to_kvs:
                kwargs[self.headers_to_kvs[name.lower()]] = value.decode("utf-8")
        with stlog.LogContext.bind(**kwargs):
            await self.app(scope, receive, send)
