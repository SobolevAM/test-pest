from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_response

from typing import Any, Optional


def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        })


def error_json_response(htt_status: int, status: str = "error", message: Optional[str] = None,
                        data: Optional[dict] = None):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=htt_status,
        data={
            "status": status,
            "message": str(message),
            "data": data,
        })