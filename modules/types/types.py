from typing import TypedDict


class ErrorResponse(TypedDict):
    code: int
    message: str


class Response(TypedDict):
    error: None | ErrorResponse
    isSuccess: bool


class Account(TypedDict):
    api_id: int
    api_hash: str
    phone_number: str