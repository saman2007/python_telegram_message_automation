from typing import TypedDict, Any


class ErrorResponse(TypedDict):
    code: int
    message: str


class Response(TypedDict):
    error: None | ErrorResponse
    isSuccess: bool
